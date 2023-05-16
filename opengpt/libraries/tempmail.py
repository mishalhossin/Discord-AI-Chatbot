# <Library by UesleiDev />
# <w> Thanks to Use! </w>

from typing import Dict, List, Union
import tls_client
import fake_useragent

class TempMail:
	@classmethod 
	def __init__(self: type) -> None:
		self.__api: str = "https://web2.temp-mail.org"
		self.__session: tls_client.Session = tls_client.Session(client_identifier="chrome_110")

		self.__HEADERS: Dict[str, str] = {
			"Authority": "web2.temp-mail.org",
			"Accept": "*/*",
			"Accept-Language": "pt-BR,en;q=0.9,en-US;q=0.8,en;q=0.7",
			"Authorization": f"Bearer {self.__GetTokenJWT()}",
			"Origin": "https://temp-mail.org",
			"Referer": "https://temp-mail.org/",
			"Sec-Ch-Ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
			"Sec-Ch-Ua-mobile": "?0",
			"Sec-Ch-Ua-platform": "\"macOS\"",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-site",
			"User-Agent": fake_useragent.UserAgent().random
		}

	@classmethod
	def __GetTokenJWT(self: type) -> str:
		DATA_: Dict[str, str] = self.__session.post(f"{self.__api}/mailbox").json()

		self.__EMAIL: str = DATA_["mailbox"]
		return DATA_["token"]

	@property
	def GetAddress(self: type) -> str:
		return f"{self.__EMAIL}"

	@classmethod
	def GetMessages(self: type) -> List[Dict[str, str]]:
		messages: Union[List, List[Dict[str, str]]] = []

		messages = self.__session.get(f"{self.__api}/messages", headers=self.__HEADERS).json()["messages"]

		return messages

	@classmethod
	def GetMessage(self: type, id: str) -> Dict[str, str]:
		DATA_: object = self.__session.get(f"{self.__api}/messages/{id}", headers=self.__HEADERS)

		if DATA_.status_code != 200:
			return "Invalid ID."

		return DATA_.json()