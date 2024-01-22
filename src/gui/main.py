import wx
import os
import sys
import threading
import chat
import sounds
from .dialogs import options

class MainFrame(wx.Frame):

	def __init__(self, *args, **kwargs):
		super(MainFrame, self).__init__(title=_("AFOAIC"), size=(600, 600), *args, **kwargs)
		self.chat = chat.Chat()
		self.sounds = sounds.Sounds(os.path.join(os.getcwd(), "sounds"))
		self.SetupMenuBar()
		self.InitUI()
		self.Show(True)

	def SetupMenuBar(self):
		menu_bar = wx.MenuBar()
		chat_menu = wx.Menu()
		new_chat_menu_item = chat_menu.Append(wx.ID_ANY, _("New chat\tCtrl+N"))
		chat_history_menu_item = chat_menu.Append(wx.ID_ANY, _("Chat history...\tCtrl+H"))
		options_menu_item = chat_menu.Append(wx.ID_ANY, _("Options...\tCtrl+Shift+O"))
		chat_menu.Append(wx.ID_EXIT, _("Exit\tAlt+F4"))
		menu_bar.Append(chat_menu, _("&Chat"))
		self.SetMenuBar(menu_bar)
		self.Bind(wx.EVT_MENU, self.OnNewChatMenuItem, new_chat_menu_item)
		self.Bind(wx.EVT_MENU, self.OnChatHistoryMenuItem, chat_history_menu_item)
		self.Bind(wx.EVT_MENU, self.OnOptionsMenuItem, options_menu_item)
		self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)

	def InitUI(self):
		self.Center()
		panel = wx.Panel(self)
		main_sizer = wx.BoxSizer(wx.VERTICAL)
		font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		panel.SetFont(font)
		output_label = wx.StaticText(panel, label=_("&Message content"))
		self.message_content = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_RICH | wx.TE_READONLY | wx.TE_WORDWRAP)
		message_label = wx.StaticText(panel, label=_("&Conversation"))
		self.message_list = wx.ListBox(panel, style=wx.LB_SINGLE)
		input_label = wx.StaticText(panel, label=_("Enter your &message here."))
		self.user_input_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_WORDWRAP | wx.TE_PROCESS_ENTER)
		main_sizer.Add(output_label, flag=wx.LEFT | wx.TOP, border=10)
		main_sizer.Add(self.message_content, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		main_sizer.AddSpacer(10)
		main_sizer.Add(message_label, flag=wx.LEFT, border=10)
		main_sizer.Add(self.message_list, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		main_sizer.AddSpacer(10)
		main_sizer.Add(input_label, flag=wx.LEFT, border=10)
		main_sizer.Add(self.user_input_text, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
		panel.SetSizer(main_sizer)
		self.SetMinSize(main_sizer.GetMinSize())
		self.BindEvents()

	def BindEvents(self):
		self.user_input_text.Bind(wx.EVT_TEXT_ENTER, self.OnEnterKeyPressed)
		self.user_input_text.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		self.user_input_text.SetFocus()
		self.message_list.Bind(wx.EVT_LISTBOX, self.OnMessageListItemChange)
		self.Bind(wx.EVT_CLOSE, self.OnClose)

	def OnEnterKeyPressed(self, event):
		text_chat_thread = threading.Thread(target=self.handle_chat)
		text_chat_thread.start()

	def OnKeyDown(self, event):
		key_code = event.GetKeyCode()
		ctrl_down = event.ControlDown()
		shift_down = event.ShiftDown()
		if key_code == wx.WXK_RETURN:
			if ctrl_down:
				self.user_input_text.AppendText("\n\n")
			elif shift_down:
				self.user_input_text.AppendText("\n")
			else:
				self.OnEnterKeyPressed(event)
		else:
			event.Skip()

	def OnMessageListItemChange(self, event):
		self.message_content.SetValue(self.message_list.GetString(self.message_list.GetSelection()))

	def OnClose(self, evt):
		self.sounds.shutdown()
		self.Destroy()
		self.Close(True)
		wx.Exit()
		sys.exit(0)

	def handle_chat(self):
		msg_user = _("user:")
		msg_assistant = _("assistant:")
		text = self.user_input_text.GetValue()
		if text.strip():
			user_message = f"{msg_user}\n{text}"
			self.message_list.Append(user_message)
			self.focus_last_message()
			self.message_content.SetValue(user_message)
			self.sounds.play_message_sent()
			snd_waiting = self.sounds.play_waiting()
			try:
				response = self.chat.get_response(text)
				self.user_input_text.Clear()
				self.chat.save_chat_history()
			except Exception as e:
				snd_waiting.stop()
				wx.MessageBox(_(f"API call Error. Details:\n{e}"), _("Error"))
				return
			assistant_message = f"{msg_assistant}\n{response}"
			self.message_list.Append(assistant_message)
			self.focus_last_message()
			self.message_content.SetValue(assistant_message)
			snd_waiting.stop()
			self.sounds.play_message_received()
			self.chat.save_chat_history()

	def focus_last_message(self):
		last_message_index = self.message_list.GetCount() - 1
		self.message_list.SetSelection(last_message_index)

	def OnNewChatMenuItem(self, evt):
		self.chat.clear_chat_history()
		self.user_input_text.Clear()
		self.message_content.Clear()
		self.message_list.Clear()

	def OnChatHistoryMenuItem(self, evt):
		file_list = self.chat.get_chat_history()
		if file_list:
			dialog = wx.SingleChoiceDialog(self, _("Select saved chat to load."), _("Chat History"), [f[1] for f in file_list])
			if dialog.ShowModal() == wx.ID_OK:
				selected_file = file_list[dialog.GetSelection()][0]
				try:
					chat_history = self.chat.load_chat_history(selected_file)
					messages = [f"{x["role"]}:\n{x["content"]}" for x in chat_history if x["role"] != "system"]
					self.message_list.SetItems(messages)
					self.message_list.SetSelection(0)
				except:
					wx.MessageBox(_("Error loading chat from history."), _("Error"))
			dialog.Destroy()
		else:
			wx.MessageBox(_("Chat history is empty."), _("Information"))

	def OnOptionsMenuItem(self, evt):
		dlg = options.OptionsDialog(self)
		dlg.ShowModal()
