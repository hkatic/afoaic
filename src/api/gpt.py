from openai import OpenAI
from core import config

def chat_completion(messages):
	client = OpenAI(organization="org-ci3MLdOaByOV90JX71sRA9yv", api_key=config.conf["options"]["key"])
	response = client.chat.completions.create(
	model=config.conf["options"]["model"],
	messages=messages,
	max_tokens=4096,
	n=1,
	)
	return response.choices[0].message

def transcribe_audio(audio_file_path):
	client = OpenAI(organization="org-ci3MLdOaByOV90JX71sRA9yv", api_key=config.conf["options"]["key"])
	with open(audio_file_path, "rb") as audio_file:
		transcript = client.audio.transcriptions.create(
			model = "whisper-1",
			file = audio_file,
			response_format="text",
			language=config.conf["transcribeAudio"]["fromLanguage"]
		)
	return transcript

def translate_audio(audio_file_path):
	client = OpenAI(organization="org-ci3MLdOaByOV90JX71sRA9yv", api_key=config.conf["options"]["key"])
	with open(audio_file_path, "rb") as audio_file:
		translation = client.audio.translations.create(
			model = "whisper-1",
			file = audio_file,
			response_format="text"
		)
	return translation
