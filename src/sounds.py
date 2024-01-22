import os
from core.sound import sound

class Sounds(object):

	def __init__(self, sound_directory):
		self.sound_directory = sound_directory
		self.sound_pool = list()
		sound.setup_sound()

	def play_message_sent(self):
		snd_message_sent = self.play_sound("message_sent.ogg")
		self.sound_pool.append(snd_message_sent)
		return snd_message_sent

	def play_waiting(self, loop=True):
		snd_waiting = self.play_sound("waiting.ogg", loop)
		self.sound_pool.append(snd_waiting)
		return snd_waiting

	def play_message_received(self):
		snd_message_received = self.play_sound("message_received.ogg")
		self.sound_pool.append(snd_message_received)
		return snd_message_received

	def play_sound(self, filename, loop=False):
		return sound.play(os.path.join(self.sound_directory, filename), loop)

	def shutdown(self):
		self.sound_pool.clear()
		sound.shutdown()
