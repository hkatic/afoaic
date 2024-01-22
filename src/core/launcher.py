import wx
import sys
import os
from platform_utils import blackhole, paths
os.chdir(paths.app_path())
from .logger import logger as logging
from . import application, config, i18n, output, sound

stdout=sys.stdout
stderr=sys.stderr
sys.stdout = open(os.path.join(os.getenv("temp"), "stdout.log"), "w")
sys.stderr = open(os.path.join(os.getenv("temp"), "stderr.log"), "w")

def start(main_frame):
	try:
		config.setup()
		i18n.setup()
	except:
		logging.exception("Error in startup process.")
		#i18n isn't setup yet so we can't localize this error message.
		return
	try:
		output.setup()
		sound.setup()
		main_frame(None)
	except:
		logging.exception("Error in startup process.")
		return
	logging.info("Startup sequence complete.")
	wx_app.MainLoop()

def startup(main_frame):
	try:
		start(main_frame)
	except:
		logging.exception("Uncaught exception")

wx_app = wx.App()
