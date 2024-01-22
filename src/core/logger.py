import os
import logging
import logging.handlers
from . import application
from . import paths
import sys
from typing import Union

class ApplicationFileHandler(logging.handlers.RotatingFileHandler):
	"""
	This class inherits from logging.handlers.RotatingFileHandler and customizes
	the behavior for handling log file rollovers.
	"""

	def __init__(self, filename: str, mode: str = 'a', maxBytes: int = 102400, encoding: str = 'utf-8', delay: int = 0):
		"""
		Initializes the ApplicationFileHandler class.
		:param filename: The name of the file to open.
		:param mode: The mode to open the file ('a' for append, 'w' for write).
		:param maxBytes: The maximum file size before it rolls over.
		:param encoding: The file encoding.
		:param delay: If True, then file opening is deferred until the first call to emit().
		"""
		super().__init__(filename, mode, maxBytes, 0, encoding, delay)

	def doRollover(self) -> None:
		"""
		Handles the rollover of log files when the maxBytes limit is reached.
		"""
		if self.stream:
			self.stream.close()
		dfn = self.baseFilename + ".1"
		if os.path.exists(dfn):
			os.remove(dfn)
		os.rename(self.baseFilename, dfn)
		os.remove(dfn)
		self.mode = 'w'
		self.stream = self._open()

# Log file names
APP_LOG_FILE = f"{application.name}.log"
ERROR_LOG_FILE = "error.log"

# Log message and date formats
MESSAGE_FORMAT = "%(asctime)s %(name)s %(levelname)s: %(message)s"
DATE_FORMAT = "%a %b %d, %Y %H:%M:%S"

# Create a formatter
formatter = logging.Formatter(MESSAGE_FORMAT, datefmt=DATE_FORMAT)

# Configure loggers
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)
oauthlib_log = logging.getLogger("oauthlib")
oauthlib_log.setLevel(logging.WARNING)
server_log = logging.getLogger("BaseHTTPServer")
server_log.setLevel(logging.WARNING)

# Main logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Handlers
app_handler = ApplicationFileHandler(paths.data_path(APP_LOG_FILE), "w", 102400)
app_handler.setFormatter(formatter)
app_handler.setLevel(logging.DEBUG)
logger.addHandler(app_handler)

error_handler = ApplicationFileHandler(paths.data_path(ERROR_LOG_FILE), "w", 102400)
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.WARNING)
logger.addHandler(error_handler)

# If not a frozen application, log errors to the console as well
if not hasattr(sys, 'frozen'):
	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.ERROR)
	console_handler.setFormatter(formatter)
	logger.addHandler(console_handler)
