import os
import pickle
from datetime import datetime
from core.paths import chats_path
from api import gpt

class Chat(object):

	def __init__(self):
		self.clear_chat_history()

	def get_response(self, text):
		self.chat_history.append({"role": "user", "content": text})
		response = gpt.chat_completion(self.chat_history).content
		self.chat_history.append({"role": "assistant", "content": response})
		return response

	def save_chat_history(self):
		if not self.filename:
			self.filename = f"chat_{datetime.now().strftime('%d%m%Y_%H%M%S')}.pkl"
		try:
			with open(chats_path(self.filename), 'wb') as file:
				pickle.dump(self.chat_history, file)
		except Exception as e:
			print(f"Error saving chat history: {e}")

	def load_chat_history(self, filename):
		try:
			with open(chats_path(filename), 'rb') as file:
				self.chat_history = pickle.load(file)
				self.filename = filename
				return self.chat_history
		except FileNotFoundError:
			print(f"File {filename} not found.")
		except Exception as e:
			print(f"Error loading chat history: {e}")
			return []

	def get_chat_history(self):
		history = []
		file_list = [f for f in os.listdir(chats_path()) if f.endswith('.pkl')]
		for filename in file_list:
			try:
				with open(chats_path(filename), 'rb') as file:
					history.append((filename, pickle.load(file)[1]["content"]))
			except:
				history.append((filename, "New Chat"))
		return history

	def clear_chat_history(self):
		self.chat_history = [{"role": "system", "content": "You are a helpfull assistant who knows everything about linguistics, math, history, geography, software development and technical support."}]
		self.filename = None
