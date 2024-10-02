from .logger import logger
logging = logger.getChild('core.config')
from io import StringIO
from . import application
from .configuration import Configuration, ConfigurationResetException
from .paths import app_path, data_path

CONFIG_FILE_NAME = f"{application.name}.ini"
CONFIG_SPEC = StringIO("""[options]
key=string(default="")
model=string(default="gpt-4o")

[transcribeAudio]
fromLanguage=string(default="auto")
translateToEnglish=boolean(default=False)
""")

conf = None

def setup():
	global conf
	try:
		conf = Configuration(data_path(CONFIG_FILE_NAME), CONFIG_SPEC)
	except ConfigurationResetException:
		import output
		output.speak("Unable to load configuration file. Loading default configuration instead.", 0)
