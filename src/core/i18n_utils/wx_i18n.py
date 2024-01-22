import core
import wx
from typing import Any

def set_wx_language(lang: str, locale_path: str) -> Any:
	wx_locale = wx.Locale()
	wx_locale.AddCatalogLookupPathPrefix(locale_path)
	if '_' in lang:
		wx_lang = lang.split('_')[0]
	else:
		wx_lang = lang
	try:
		wx_locale.Init(lang, wx_lang)
	except Exception as e:
		pass
