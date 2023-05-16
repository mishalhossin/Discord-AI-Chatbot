from .tools.typing.response import ForeFrontResponse
from .tools.system.signature import Encrypt
from .attributes.conversation import Conversation
from libraries.colorama import init, Fore, Style
from typing import Optional, Union, Generator, Dict, List
from base64 import b64encode
import fake_useragent
import requests
import json
import logging

init()

class Model:
	@classmethod
	def __init__(self: object, sessionID: str, client: str, model: Optional[str] = "gpt-3.5-turbo", 
		conversationID: Optional[Union[str, None]] = None
	) -> None:
		self._SETUP_LOGGER()
		self.Conversation: Conversation = Conversation(model=self)
		self._session: requests.Session = requests.Session()
		self._model: str = model
		self._API = "https://chat-api.tenant-forefront-default.knative.chi.coreweave.com/api/trpc"
		self.__NAME: Union[str, None] = None
		self._WORKSPACEID: str = ''
		self._USERID: str = "user_"
		self._CLIENT: str = client
		self._SESSION_ID: str = sessionID
		self.CONVERSATION_ID: [Union[str, None]] = conversationID
		self._PERSONA: str = "607e41fe-95be-497e-8e97-010a59b2e2c0"
		self._JSON: Dict[str, str] = {}
		self._HEADERS: Dict[str, str] = {
			"Authority": "streaming.tenant-forefront-default.knative.chi.coreweave.com",
			"Accept": "*/*",
			"Accept-Language": "en,pt-BR,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3",
			"Authorization": f"Bearer {self._CLIENT}",
			"Cache-Control": "no-cache",
			"Pragma": "no-cache",
			"Content-Type": "application/json",
			"Origin": "https://chat.forefront.ai",
			"Referer": "https://chat.forefront.ai/",
			"Sec-Ch-Ua": "\"Chromium\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
			"Sec-Ch-Ua-mobile": "?0",
			"Sec-Ch-Ua-platform": "\"macOS\"",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "cross-site",
			"X-Message": "this is already a free service, go to chat.forefront.ai to use gpt-4",
			"User-Agent": fake_useragent.UserAgent().random
		}

		self._JWT_HEADERS: Dict[str, str] = {
			"Authority": "clerk.forefront.ai",
			"Accept": "*/*",
			"Cache-Control": "no-cache",
			"Content-Type": "application/x-www-form-urlencoded",
			"Pragma": "no-cache",
			"Cookie": f"__client={self._CLIENT}",
			"Sec-Ch-Ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
			"Sec-Ch-Ua-mobile": "?0",
			"Sec-Ch-Ua-platform": "\"macOS\"",
			"Origin": "https://chat.forefront.ai",
			"Referer": "https://chat.forefront.ai/",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-site",
			"User-Agent": fake_useragent.UserAgent().random
		}

		self._WORKSPACEID = self._GetWorkspaceID()
		self._USERID = self._GetUserID()

		self._logger.debug(Fore.CYAN + "Connected" + Style.RESET_ALL + " in Workspace: " + Fore.MAGENTA + self._WORKSPACEID + Style.RESET_ALL)

	@classmethod
	def _SETUP_LOGGER(self: type) -> None:
		self._logger: logging.getLogger = logging.getLogger(__name__)
		self._logger.setLevel(logging.DEBUG)
		console_handler: logging.StreamHandler = logging.StreamHandler()
		console_handler.setLevel(logging.DEBUG)
		formatter: logging.Formatter = logging.Formatter("Model - %(levelname)s - %(message)s")
		console_handler.setFormatter(formatter)

		self._logger.addHandler(console_handler)

	@classmethod
	def _UpdateJWTToken(self: type) -> None:
		jwt_token: Dict[str, str] = {}
		jwt_status: int = 0

		jwt_token = self._session.post(f"https://clerk.forefront.ai/v1/client/sessions/{self._SESSION_ID}/tokens?_clerk_js_version=4.38.4", headers=self._JWT_HEADERS)
		jwt_status = jwt_token.status_code

		if jwt_status == 401:
			DATA_: Dict[str, str] = self._session.get("https://clerk.forefront.ai/v1/client?_clerk_js_version=4.39.0", headers=self._JWT_HEADERS)
			self._SESSION_ID = DATA_.json()["response"]["last_active_session_id"]

			self._logger.warn(Fore.YELLOW + "Your Session ID as Expired." + Style.RESET_ALL + ", Changing to a valid session id. Use this: " + Fore.MAGENTA + self._SESSION_ID + Style.RESET_ALL)
			self._UpdateJWTToken()
			return
		elif jwt_status == 404:
			DATA_: Dict[str, str] = self._session.get("https://clerk.forefront.ai/v1/client?_clerk_js_version=4.39.0", headers=self._JWT_HEADERS)
			self._SESSION_ID = DATA_.json()["response"]["last_active_session_id"]

			self._logger.warn(Fore.YELLOW + "Invalid Session ID." + Style.RESET_ALL + " Changing to a valid session id. Use this: " + Fore.MAGENTA + self._SESSION_ID + Style.RESET_ALL)
			self._UpdateJWTToken()
			return

		self._HEADERS["Authorization"] = f"Bearer {jwt_token.json()['jwt']}"

	@classmethod
	def _UpdateXSignature(self: type) -> None:
		self._HEADERS["X-Signature"] = "65a44079065a90fd4b8777a5a9e8393f35814ca137e902debf6ce60314099d856cc8e655e03de2dcdc8225712938b9614dea3b0e826b3e8021bc51bd0657c0ef"

	@classmethod								
	def _GetUserID(self: type) -> str:
		DATA_: Dict[str, str] = self._session.post(f"https://clerk.forefront.ai/v1/client/sessions/{self._SESSION_ID}/touch?_clerk_js_version=4.38.4",
																headers=self._JWT_HEADERS).json()
		return DATA_["response"]["user"]["id"]

	@classmethod
	def _GetWorkspaceID(self: type) -> str:
		self._UpdateJWTToken()

		url: str = f"{self._API}/workspaces.listWorkspaces,chat.loadTree?batch=1&input="
		payload: str = "{\"0\":{\"json\":null,\"meta\":{\"values\":[\"undefined\"]}},\"1\":{\"json\":{\"workspaceId\":\"\"}}}"
		return self._session.get(url + payload, headers=self._HEADERS).json()[0]["result"]["data"]["json"][0]["id"]

	@classmethod
	def SetupConversation(self: type, prompt: str, options: Optional[Dict[str, str]] = {}) -> None:
		action = "new"
		conversations: Dict[str, str] = self.Conversation.GetList()
		if self.CONVERSATION_ID is None:
			if conversations[-1]["type"] == "chat":
				self.CONVERSATION_ID = conversations[-1]["id"]
				action = "continue"
		else:
			action = "continue"

		if "create" in options:
			if options["create"]:
				action = "new"

				if "name" not in options:
					self.__logger.error("Invalid options.")
					return None

				for cv in conversations:
					if cv["name"].lower() != options["name"].lower():
						self.__NAME = options["name"]

		self._JSON = {
			"text": prompt,
			"action": action,
			"id": self.CONVERSATION_ID,
			"parentId": self._WORKSPACEID,
			"workspaceId": self._WORKSPACEID,
			"messagePersona": self._PERSONA,
			"model": self._model
		}

	@classmethod
	def IsAccountActive(self: type) -> bool:
		return self._session.post(f"https://clerk.forefront.ai/v1/client/sessions/{self._SESSION_ID}/touch?_clerk_js_version=4.38.4", 
			headers=self._JWT_HEADERS).status_code == 200

	@classmethod
	def SendConversation(self: type) -> Generator[ForeFrontResponse, None, None]:
		self._UpdateJWTToken()
		self._UpdateXSignature()
		
		for chunk in self._session.post("https://streaming.tenant-forefront-default.knative.chi.coreweave.com/chat", 
			headers=self._HEADERS, json=self._JSON, stream=True
		).iter_lines():
			if b"choices\":[" in chunk:
				data = json.loads(chunk.decode('utf-8').split("data: ")[1])
				yield ForeFrontResponse(**data)

		conversations: List[Dict[str, str]] = self.Conversation.GetList()
		if self.__NAME is not None:
			self.Conversation.Rename(conversations[-1]["id"], self.__NAME)
			self.__NAME = None
		else:
			if conversations[-1]["name"].lower() == "new chat" and self._JSON["action"] == "new":
				conversation: Dict[str, str] = conversations[-1]
				self.Conversation.Rename(conversation["id"], self.Conversation.GenerateName(self._JSON["text"]))
