from openai import OpenAI
from core import config

def chat_completion(messages):
	client = OpenAI(organization="org-ci3MLdOaByOV90JX71sRA9yv", api_key=config.conf["options"]["key"])
	try:
		response = client.chat.completions.create(
		model=config.conf["options"]["model"],
		messages=messages,
		max_tokens=4096,
		n=1,
		)
		return response.choices[0].message
	except Exception as e:
		raise Exception("An error occurred with the OpenAI chat completion API call.") from e
