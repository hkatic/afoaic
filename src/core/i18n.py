from .logger import logger
logging = logger.getChild("core.i18n")
from typing import List, Dict
from . import application
from . import config
from .i18n_utils import core, wx_i18n
from . import paths

def setup():
	logging.info("Initializing the i18n subsystem.")
	core.set_active_language(application.name, paths.locale_path(), "windows")

def available_languages() -> Dict[str, Dict]:
	return core.available_languages(paths.locale_path(), application.name)

def printable_lang(lang: Dict) -> str:
	return lang['language']

def printable_available_languages() -> List[str]:
	langs = available_languages()
	return [printable_lang(langs[i]) for i in langs]

def lang_from_printable_language(language: str) -> str:
	langs = available_languages()
	for i in langs:
		if langs[i]['language'] == language:
			return i # I know it's just the key
