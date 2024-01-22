import ctypes
import gettext
import locale
import os
from typing import Dict, List

# Windows locale constants
LOCALE_SLANGUAGE = 0x2
LOCALE_SLANGDISPLAYNAME = 0x6f
BUFFSIZE = 1024

def locale_name_to_LCID(locale_name: str) -> int:
	locale_name = locale.normalize(locale_name)
	if '.' in locale_name:
		locale_name = locale_name.split('.')[0]
	func_locale_nameToLCID = getattr(ctypes.windll.kernel32, 'LocaleNameToLCID', None)
	if func_locale_nameToLCID:
		locale_name = locale_name.replace('_', '-')
		LCID = func_locale_nameToLCID(locale_name, 0)
	else:
		LCList = [x[0] for x in locale.windows_locale.items() if x[1] == locale_name]
		LCID = LCList[0] if LCList else 0
	return LCID

def language_description(language: str) -> str:
	LCID = locale_name_to_LCID(language)
	if LCID == 0:
		return None
	buffer = ctypes.create_unicode_buffer(BUFFSIZE)
	res = ctypes.windll.kernel32.GetLocaleInfoW(LCID, LOCALE_SLANGDISPLAYNAME, buffer, BUFFSIZE)
	if res == 0:
		res = ctypes.windll.kernel32.GetLocaleInfoW(LCID, LOCALE_SLANGUAGE, buffer, BUFFSIZE)
	return buffer.value

def available_languages(locale_dir: str, app_name: str) -> Dict[str, Dict]:
	dirs = [i for i in os.listdir(locale_dir) if not i.startswith('.')]
	langs = sorted(['en'] + [i for i in dirs if os.path.isfile(os.path.join(locale_dir, f'{i}/LC_MESSAGES/{app_name}.mo'))])
	result = {}
	for l in langs:
		result[l] = {'LCID': locale_name_to_LCID(l)}
		description = language_description(l)
		result[l]['language'] = description if description else l
	if 'Windows' not in result:
		result['Windows'] = {'language': "User default, Windows"}
	return result

def set_active_language(app_name: str, locale_dir: str, lang: str) -> bool:
	try:
		if lang == "Windows":
			LCID = ctypes.windll.kernel32.GetUserDefaultUILanguage()
			lang = locale.windows_locale[LCID]
		translation = gettext.translation(app_name, localedir=locale_dir, languages=[lang])
		translation.install(names=['ngettext'])
		locale.setlocale(locale.LC_ALL, lang)
		LCID = locale_name_to_LCID(lang)
		ctypes.windll.kernel32.SetThreadLocale(LCID)
		return True
	except IOError:
		gettext.install(app_name, names=['ngettext'])
