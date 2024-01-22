from .logger import logger
logging = logger.getChild('core.output')
from accessible_output2 import outputs
import sys
import win32clipboard

speaker = None

def speak(text: str, interrupt: int = 0) -> None:
	global speaker
	if not speaker:
		setup()
	speaker.speak(text, interrupt)

def Copy(text: str) -> bool:
	win32clipboard.OpenClipboard()
	win32clipboard.EmptyClipboard()
	win32clipboard.SetClipboardText(text)
	win32clipboard.CloseClipboard()
	return True

def setup() -> None:
	global speaker
	logging.debug("Initializing output subsystem.")
	try:
		speaker = outputs.auto.Auto()
	except Exception as e:
		logging.exception("Output: Error during initialization.")
		return
