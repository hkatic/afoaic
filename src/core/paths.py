from platform_utils import paths
from . import application
import os
import sys
from typing import Optional
from functools import wraps

def merge_paths(func):
	@wraps(func)
	def merge_paths_wrapper(*a):
		return os.path.join(func(), *a)
	return merge_paths_wrapper

@merge_paths
def app_path() -> str:
	return paths.app_path()

@merge_paths
def data_path() -> str:
	dataPathExists = os.path.exists(paths.app_data_path(application.name))
	if application.installed:
		paths.prepare_app_data_path(application.name)
	if not application.installed and dataPathExists or application.installed and dataPathExists:
		return paths.app_data_path(application.name)
	else:
		if not os.path.exists(app_path("data")):
			os.mkdir(app_path("data"))
		return app_path("data")

@merge_paths
def locale_path() -> str:
	return app_path("locale")

@merge_paths
def chats_path() -> str:
	if not os.path.exists(data_path("chatlogs")):
		os.mkdir(data_path("chatlogs"))
	return data_path("chatlogs")

def get_doc_file_path(fileName: str, localized: bool = True) -> Optional[str]:
	import config
	if not get_doc_file_path.rootPath:
		if hasattr(sys, "frozen"):
			get_doc_file_path.rootPath = app_path("help")
		else:
			get_doc_file_path.rootPath = os.path.abspath(os.path.join("..", "help"))
	if localized:
		lang = config.conf["general"]["language"]
		tryLangs = [lang]
		if "_" in lang:
			tryLangs.append(lang.split("_")[0])
		tryLangs.append("en")
		fileName, fileExt = os.path.splitext(fileName)
		for tryLang in tryLangs:
			tryDir = os.path.join(get_doc_file_path.rootPath, tryLang)
			if not os.path.isdir(tryDir):
				continue
			for tryExt in ("html", "txt"):
				tryPath = os.path.join(tryDir, f"{fileName}.{tryExt}")
				if os.path.isfile(tryPath):
					return tryPath
	else:
		if not hasattr(sys, "frozen") and fileName in ("license.txt", "contributors.txt"):
			return os.path.join(paths.app_path(), "..", fileName)
		else:
			return os.path.join(get_doc_file_path.rootPath, "..", fileName)

get_doc_file_path.rootPath = None
