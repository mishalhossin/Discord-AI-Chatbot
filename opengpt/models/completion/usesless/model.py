from typing import Dict, Optional, Generator
from .tools.typing.response import UseslessResponse
import requests
import json

class Model:
	@classmethod
	def __init__(self: type, model: Optional[str] = "gpt-3.5-turbo", temperature: Optional[int] = 1) -> None:
		self.__session: requests.Session = requests.Session()
		self.__JSON: Dict[str, str] = {"openaiKey": "", "prompt": "", "options": self.__SetOptions(model=model, 
			temperature=temperature, presence_penalty=0.8)}

		self.__HEADERS: Dict[str, str] = {
			"Authority": "ai.usesless.com",
			"Accept": "*/*",
			"Accept-Language": "pt-BR,en-US,en;q=0;5",
			"Origin": "https://ai.usesless.com",
			"Referer": "https://ai.usesless.com/chat",
			"Cache-Control": "no-cache",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0"
		}

	@classmethod
	def __SetOptions(self: type, **kwargs) -> Dict[str, str]:
		return {"completionParams": kwargs, "systemMessage": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."}

	@classmethod
	def SetupConversation(self: type, prompt: str) -> None:
		self.__JSON["prompt"] = prompt

	@classmethod
	def SendConversation(self: type) -> Generator[UseslessResponse, None, None]:
		for chunk in self.__session.post("https://ai.usesless.com/api/chat-process", headers=self.__HEADERS, json=self.__JSON, stream=True).iter_lines():
			data = json.loads(chunk.decode("utf-8"))
			yield UseslessResponse(**data["detail"])