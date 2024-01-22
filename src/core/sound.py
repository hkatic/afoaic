import logging
logging = logging.getLogger('core.sound')

from . import config
from sound_lib.main import BassError
from sound_lib import input as sound_input, output as sound_output, recording, stream

class Sound(object):

	MAX_OUTPUT_RESETS = 2 #How many times do we let the play method reset the output if sounds won't play to pickup soundcard changes?

	def setup_sound(self, forced=False):
		if forced or not getattr(self, 'sound_output', None):
			logging.debug("Initializing sound subsystem.")
			if hasattr(self, 'sound_output') and self.sound_output:
				self.sound_output.free()
			try:
				self.sound_output = sound_output.Output()
				self.sound_input = sound_input.Input()
				self.sound_output.volume = config.conf['sounds']['volume']
			except:
				self.sound_output = None
				self.sound_input = None
		if hasattr(self, 'sound_output') and 'sounds' in config.conf and 'defaultSound' in config.conf['sounds']:
			self.default_sound = self.config['sounds']['defaultSound']

	def play(self, file, loop=False, this_retry=0):
		try:
			snd = stream.FileStream(file=file)
			snd.looping = loop
			snd.play()
		except BassError as e:
			if this_retry < self.MAX_OUTPUT_RESETS:
				self.setup_sound(forced=True)
				return self.play(file, this_retry=this_retry+1)
			raise e
		return snd

	def play_stream (self, url):
		try:
			snd = stream.URLStream(url=url)
		except BassError as e:
			if e.code == 32:
				output.speak(_("No internet connection could be opened."), True)
			else:
				logging.exception("Unable to play stream")
				output.speak(_("Unable to play audio."), True)
			raise e
		snd.play()
		return snd

	def record_sound(self, filename):
		try:
			rec = recording.WaveRecording(filename=filename)
		except BassError as e:
			self.sound_input = sound_input.Input()
			rec = recording.WaveRecording(filename=filename)
		return rec

	def get_volume (self):
		return self.sound_output.volume

	def set_volume (self, volume):
		if volume <= 0:
			volume = 0
		config.conf['sounds']['volume'] = volume
		self.sound_output.volume = volume
		config.conf.write()

	volume = property(get_volume, set_volume)

	def shutdown(self):
		try: self.sound_output.free()
		except: pass
		try: self.sound_input.free()
		except: pass

def setup():
	sound.setup_sound()

def shutdown():
	sound.shutdown()

sound = Sound()
