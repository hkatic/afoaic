import os
import threading
import time
import random
import wx
from api import gpt
from core import config
from core.paths import transcriptions_path
from mappers import lang_code_name_mapper

class TranscribeAudioDialog(wx.Dialog):

	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, id=wx.ID_ANY, title=_("Transcribe Audio"), pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE, *args, **kwargs)
		self.transcription_result = ""
		self.initUI()
		self.Centre(wx.BOTH)

	def initUI(self):
		dialogSizer = wx.BoxSizer(wx.VERTICAL)

		# Language selection controls
		languageSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.languageLabel = wx.StaticText(self, label=_("Source &language:"))
		self.languageChoice = wx.Choice(self, choices=lang_code_name_mapper.get_language_names())
		self.languageChoice.SetStringSelection(lang_code_name_mapper.map_language_code_name(config.conf["transcribeAudio"]["fromLanguage"]))
		languageSizer.Add(self.languageLabel, 0, wx.ALL, 5)
		languageSizer.Add(self.languageChoice, 1, wx.EXPAND | wx.ALL, 5)

		# Audio file path controls
		audioFilePathSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.audioFilePathLabel = wx.StaticText(self, label=_("Audio &file path:"))
		self.audioFilePathEdit = wx.TextCtrl(self)
		self.audioFilePathEdit.SetValue(config.conf["transcribeAudio"]["audioFilePath"])
		self.browseButton = wx.Button(self, label=_("&Browse"))
		self.browseButton.Bind(wx.EVT_BUTTON, self.OnBrowse)
		audioFilePathSizer.Add(self.audioFilePathLabel, 0, wx.ALL, 5)
		audioFilePathSizer.Add(self.audioFilePathEdit, 1, wx.EXPAND | wx.ALL, 5)
		audioFilePathSizer.Add(self.browseButton, 0, wx.ALL, 5)

		# Progress bar
		self.progressBar = wx.Gauge(self, range=100, style=wx.GA_HORIZONTAL)
		self.progressBar.Hide()

		# Standard button sizer
		buttonSizer = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
		self.FindWindowById(wx.ID_OK).SetLabel(_("&Transcribe"))
		self.Bind(wx.EVT_BUTTON, self.OnTranscribe, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)

		dialogSizer.Add(languageSizer, 0, wx.EXPAND | wx.ALL, 10)
		dialogSizer.Add(audioFilePathSizer, 0, wx.EXPAND | wx.ALL, 10)
		dialogSizer.Add(self.progressBar, 0, wx.EXPAND | wx.ALL, 10)
		dialogSizer.Add(buttonSizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		self.SetSizer(dialogSizer)
		self.languageChoice.SetFocus()

	def OnBrowse(self, evt):
		wildcard = "Audio files (*.mp3;*.mp4;*.mpeg;*.mpga;*.m4a;*.wav;*.webm)|*.mp3;*.mp4;*.mpeg;*.mpga;*.m4a;*.wav;*.webm"
		dialog = wx.FileDialog(self, _("Choose an audio file"), wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		if dialog.ShowModal() == wx.ID_OK:
			self.audioFilePathEdit.SetValue(dialog.GetPath())
		dialog.Destroy()

	def OnTranscribe(self, evt):
		audio_file_path = self.audioFilePathEdit.GetValue()
		if not os.path.exists(audio_file_path) and not os.path.isfile(audio_file_path):
			wx.MessageBox(_("The specified audio file does not exist. Please check the file path."), _("Error"), wx.OK | wx.ICON_ERROR)
			return
		config.conf["transcribeAudio"]["fromLanguage"] = lang_code_name_mapper.map_language_code_name(self.languageChoice.GetStringSelection())
		config.conf["transcribeAudio"]["audioFilePath"] = self.audioFilePathEdit.GetValue()
		config.conf.write()
		self.progressBar.Show()
		self.progressBar.SetValue(0)
		self.FindWindowById(wx.ID_OK).Disable()
		self.FindWindowById(wx.ID_CANCEL).Enable()
		self.transcription_thread = threading.Thread(target=self.TranscribeAudio, daemon=True)
		self.transcription_thread.start()
		self.progress_thread = threading.Thread(target=self.UpdateProgress, daemon=True)
		self.progress_thread.start()

	def TranscribeAudio(self):
		try:
			self.transcription_result = gpt.transcribe_audio(self.audioFilePathEdit.GetValue())
			self.SaveTranscriptionToFile(self.transcription_result)
			wx.CallAfter(self.TranscriptionComplete)
		except Exception as e:
			wx.CallAfter(self.TranscriptionError, e)

	def SaveTranscriptionToFile(self, transcription_text):
		source_dir, source_filename = os.path.split(self.audioFilePathEdit.GetValue())
		output_filename = f"{os.path.splitext(source_filename)[0]}.txt"
		file_path = os.path.join(transcriptions_path(), output_filename)
		with open(file_path, 'w', encoding='utf-8') as f:
			f.write(transcription_text)
		return file_path

	def UpdateProgress(self):
		progress = 0
		while progress < 100 and self.transcription_thread.is_alive():
			if progress < 90:
				# Move quickly to 90%
				progress += random.randint(1, 5)
			else:
				# Slow down as we approach 100%
				progress += 0.1
			progress = min(progress, 99)  # Ensure we don't exceed 99%
			wx.CallAfter(self.progressBar.SetValue, int(progress))
			time.sleep(0.1)  # Update every 100ms

	def TranscriptionComplete(self):
		wx.CallAfter(self.progressBar.SetValue, 100)
		time.sleep(0.5)
		self.Destroy()
		wx.MessageBox(_("Transcription complete!"), _("Success"), wx.OK | wx.ICON_INFORMATION)

	def TranscriptionError(self, e):
		wx.CallAfter(self.progressBar.SetValue, 100)
		time.sleep(0.5)
		self.Destroy()
		wx.MessageBox(_(f"API call Error. Details:\n{e}"), _("Error"))

	def OnCancel(self, evt):
		self.Destroy()

	def GetResult(self):
		return self.transcription_result
