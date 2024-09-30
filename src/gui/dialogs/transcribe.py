import wx
from core import config

class TranscribeAudioDialog(wx.Dialog):

	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, id=wx.ID_ANY, title=_("Transcribe Audio"), pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE, *args, **kwargs)
		self.initUI()
		self.Centre(wx.BOTH)

	def initUI(self):
		dialogSizer = wx.BoxSizer(wx.VERTICAL)

		# Language selection controls
		languageSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.languageLabel = wx.StaticText(self, label=_("Source &language:"))
		self.languageChoice = wx.Choice(self, choices=[])
		self.languageChoice.SetStringSelection(config.conf["transcribeAudio"]["fromLanguage"])
		languageSizer.Add(self.languageLabel, 0, wx.ALL, 5)
		languageSizer.Add(self.languageChoice, 1, wx.EXPAND | wx.ALL, 5)

		# Audio file path controls
		audioFilePathSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.audioFilePathLabel = wx.StaticText(self, label=_("Audio &file path:"))
		self.audioFilePathEdit = wx.TextCtrl(self)
		self.audioFilePathEdit.SetValue(config.conf["transcribeAudio"]["audioFilePath"])
		audioFilePathSizer.Add(self.audioFilePathLabel, 0, wx.ALL, 5)
		audioFilePathSizer.Add(self.audioFilePathEdit, 1, wx.EXPAND | wx.ALL, 5)

		# Standard button sizer
		buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		self.Bind(wx.EVT_BUTTON, self.OnOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
		dialogSizer.Add(languageSizer, 0, wx.EXPAND | wx.ALL, 10)
		dialogSizer.Add(audioFilePathSizer, 0, wx.EXPAND | wx.ALL, 10)
		dialogSizer.Add(buttonSizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		self.SetSizer(dialogSizer)
		self.languageChoice.SetFocus()

	def OnOk(self, evt):
		config.conf["transcribeAudio"]["fromLanguage"] = self.languageChoice.GetStringSelection()
		config.conf["transcribeAudio"]["audioFilePath"] = self.audioFilePathEdit.GetValue()
		config.conf.write()
		self.Destroy()

	def OnCancel(self, evt):
		self.Destroy()
