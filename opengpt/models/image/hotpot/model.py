from typing import Dict, Text, Optional, Generator, Any, Tuple
from .tools.system.id import UniqueID
from .tools.typing.response import ModelResponse
from ....libraries.colorama import init, Fore, Style
import yaml
import requests
import fake_useragent
import logging
import os

init()

class OpenGPTError(Exception):
	@staticmethod
	def Print(context: Text, warn: Optional[bool] = False) -> None:
		if warn:
			print(Fore.YELLOW + "Warning: " + context + Style.RESET_ALL)
		else:
			print(Fore.RED + "Error: " + context + Style.RESET_ALL)
			sys.exit(1)

class Model:
	@classmethod
	def __init__(self: type, style: Optional[Text] = "Hotpot Art 9") -> None:
		self._SETUP_LOGGER()
		self.__DIR: Text = os.path.dirname(os.path.abspath(__file__))
		self.__LoadStyles()
		self.__session: requests.Session = requests.Session()
		self.__UNIQUE_ID: str = UniqueID(16)
		self.STYLE: Text = style
		self.__STYLE_ID = self.__GetStyleID(self.STYLE)
		self.__HEADERS: Dict[str, str] = {
			"Accept": "*/*",
			"Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
			"Content-Type": f"multipart/form-data; boundary=----WebKitFormBoundary{self.__UNIQUE_ID}",
			"Authorization": "hotpot-temp9n88MmVw8uaDzmoBq",
			"Host": "api.hotpot.ai",
			"Origin": "https://hotpot.ai",
			"Referer": "https://hotpot.ai/",
			"Sec-Ch-Ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
			"Sec-Ch-Ua-mobile": "?0",
			"Sec-Ch-Ua-platform": "\"Windows\"",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-site",
			"User-Agent": fake_useragent.UserAgent().random
		}

	@classmethod
	def _SETUP_LOGGER(self: type) -> None:
		self.__logger: logging.getLogger = logging.getLogger(__name__)
		self.__logger.setLevel(logging.DEBUG)
		console_handler: logging.StreamHandler = logging.StreamHandler()
		console_handler.setLevel(logging.DEBUG)
		formatter: logging.Formatter = logging.Formatter("Model - %(levelname)s - %(message)s")
		console_handler.setFormatter(formatter)

		self.__logger.addHandler(console_handler)

	@classmethod
	def __GetStyleID(self: type, style: Text) -> int:
		if style in self.__DATA:
			return int(self.__DATA[style])
		else:
			OpenGPTError.Print(context=f"The style \"{style}\" not found. Changing to \"Hotpot Art 9\"", warn=True)
			self.STYLE = "Hotpot Art 9"
			return int(140)

	@classmethod
	def UpdateStyle(self: type, style: Text) -> None:
		self.STYLE = style
		self.__STYLE_ID = self.__GetStyleID(self.STYLE)

	@classmethod
	def __LoadStyles(self: type) -> None:
		self.__DATA: Dict[Text, Text] = yaml.safe_load(open(self.__DIR + "/styles.yml", "r").read())

	@classmethod
	def __Fields(self: type, *args: Tuple[int, str], **kwargs: Dict[str, Any]) -> Text:
		return kwargs

	@classmethod
	def __AddField(self: type, field: Text, value: Any, end: Optional[bool] = False) -> Text:
		form: Text = ''

		form += f"\n\n------WebKitFormBoundary{self.__UNIQUE_ID}"
		form += f"\nContent-Disposition: form-data; name=\"{field}\""
		form += f"\n\n{value}"

		if end:
			form += f"\n------WebKitFormBoundary{self.__UNIQUE_ID}--"
		return form

	@classmethod
	def Generate(self: type, prompt: Text, width: Optional[int] = 256, height: Optional[int] = 256) -> Generator[ModelResponse, None, None]:
		__DATA: Dict[str, str] = self.__Fields(seedValue=-1, inputText=prompt, width=width, height=height, styleId=self.__STYLE_ID, 
			styleLabel=self.STYLE, isPrivate=False, requestId=f"8-{self.__UNIQUE_ID}", 
			resultUrl=f"https://hotpotmedia.s3.us-east-2.amazonaws.com/8-{self.__UNIQUE_ID}.png")

		__FORM_DATA: Text = ''

		for field in __DATA:
			if field != "resultUrl":
				__FORM_DATA += self.__AddField(field, __DATA[field])
			else:
				__FORM_DATA += self.__AddField(field, __DATA[field], end=True)

		self.__logger.debug("Generating image " + Fore.CYAN + f"\"{prompt}\"" + Style.RESET_ALL)
		url: Text = self.__session.post("https://api.hotpot.ai/art-premium-test1", headers=self.__HEADERS, data=__FORM_DATA).content
		return ModelResponse(**{
			"id": __DATA["requestId"],
			"url": url.decode().replace("\"", ""),
			"style": self.STYLE,
			"width": __DATA["width"],
			"height": __DATA["height"]
		})
