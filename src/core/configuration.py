from collections import UserDict
from configobj import ConfigObj, ParseError
from validate import Validator, VdtValueError
import os

class ConfigurationResetException(Exception):
	pass

class Configuration(UserDict):
	"""Manage application configurations using ConfigObj."""

	def __init__(self, file=None, spec=None, *args, **kwargs):
		"""Initialize the Configuration object."""
		self.file = file
		self.spec = spec
		self.validator = Validator()
		self.setup_config(file=file, spec=spec)
		self.validated = self.config.validate(self.validator, copy=True)
		if self.validated:
			self.write()
		super().__init__(self.config)

	def setup_config(self, file, spec):
		"""Set up configurations using ConfigObj."""
		spec = ConfigObj(spec, list_values=False)
		try:
			self.config = ConfigObj(infile=file, configspec=spec, create_empty=True, stringify=True)
		except ParseError:
			os.remove(file)
			self.config = ConfigObj(infile=file, configspec=spec, create_empty=True, stringify=True)
			raise ConfigurationResetException

	def __getitem__(self, key):
		"""Get an item from the configuration."""
		return self.config[key]

	def __setitem__(self, key, value):
		"""Set an item in the configuration."""
		self.config[key] = value
		self.data[key] = value

	def write(self):
		"""Write the configuration to disk."""
		if hasattr(self.config, 'write'):
			self.config.write()
