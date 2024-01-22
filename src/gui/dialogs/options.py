import wx
import constants
from core import config

class OptionsDialog(wx.Dialog):

	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, id=wx.ID_ANY, title=_("Options"), pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE, *args, **kwargs)
		self.initUI()
		self.Centre(wx.BOTH)

	def initUI(self):
		dialogSizer = wx.BoxSizer(wx.VERTICAL)

		# API Key controls
		apiKeySizer = wx.BoxSizer(wx.HORIZONTAL)
		self.apiKeyLabel = wx.StaticText(self, label=_("API &key:"))
		self.apiKeyEdit = wx.TextCtrl(self)
		self.apiKeyEdit.SetValue(config.conf["options"]["key"])
		apiKeySizer.Add(self.apiKeyLabel, 0, wx.ALL, 5)
		apiKeySizer.Add(self.apiKeyEdit, 1, wx.EXPAND | wx.ALL, 5)

		# Model selection controls
		modelSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.modelLabel = wx.StaticText(self, label=_("&Model:"))
		self.modelChoice = wx.Choice(self, choices=constants.GPT_MODELS)
		self.modelChoice.SetStringSelection(config.conf["options"]["model"])
		modelSizer.Add(self.modelLabel, 0, wx.ALL, 5)
		modelSizer.Add(self.modelChoice, 1, wx.EXPAND | wx.ALL, 5)

		# Standard button sizer
		buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		self.Bind(wx.EVT_BUTTON, self.OnOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
		dialogSizer.Add(apiKeySizer, 0, wx.EXPAND | wx.ALL, 10)
		dialogSizer.Add(modelSizer, 0, wx.EXPAND | wx.ALL, 10)
		dialogSizer.Add(buttonSizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		self.SetSizer(dialogSizer)
		self.apiKeyEdit.SetFocus()

	def OnOk(self, evt):
		config.conf["options"]["key"] = self.apiKeyEdit.GetValue()
		config.conf["options"]["model"] = self.modelChoice.GetStringSelection()
		config.conf.write()
		self.Destroy()

	def OnCancel(self, evt):
		self.Destroy()
