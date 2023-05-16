from typing import List, Dict
from pydantic import BaseModel
from libraries.colorama import init, Fore, Style
import json
import uuid

class Conversation():
	@classmethod
	def __init__(self: type, model: type) -> None:
		self.__model: type = model

	@classmethod
	def GetList(self: type) -> List[Dict[str, str]]:
		self.__model._UpdateJWTToken()
		PAYLOAD: Dict[str, str] = {
		   "0":{
		      "json":{
		         "workspaceId": self.__model._WORKSPACEID
		      }
		   },
		   "1":{
		      "json":{
		         "workspaceId": self.__model._WORKSPACEID
		      }
		   }
		}

		return self.__model._session.get(f"{self.__model._API}/chat.loadTree,personas.listPersonas?batch=1&input={json.dumps(PAYLOAD)}", headers=self.__model._HEADERS).json()[0]["result"]["data"]["json"][0]["data"]
		

	@classmethod
	def Rename(self: type, id: str, name: str) -> None:
		conversations: List[Dict[str, str]] = self.GetList()
		PAYLOAD: Dict[str, str] = {
			"0": {
				"json": {
					"id": id,
					"name": name,
					"workspaceId": self.__model._WORKSPACEID
				}
			}
		}

		for cv in conversations:
			if id == cv["id"]:
				DATA_: object = self.__model._session.post(f"{self.__model._API}/chat.renameChat?batch=1", json=PAYLOAD, headers=self.__model._HEADERS)

				if DATA_.status_code == 200:
					self.__model._logger.debug(f"Renamed conversation ({Fore.CYAN}{id}{Style.RESET_ALL}) to ({Fore.MAGENTA}{name}{Style.RESET_ALL}).")
				else:
					self.__model._logger.error(f"{Fore.RED}Error on rename the conversation {id}{Style.RESET_ALL}")
					return None

	@classmethod
	def GenerateName(self: type, message: str) -> str:
		__PAYLOAD: Dict[str, str] = {
			"0": {
				"json": {
					"messages": [
						{
							"id": "",
							"content": message,
							"parentId": str(uuid.uuid4()),
							"role": "user",
							"createdAt": "",
							"model": self.__model._model
						}
					]
				},
				"meta": {
					"values": {
						"messages.0.createdAt": ["Date"]
					}
				}
			}
		}
		Suggestion: Dict[str, str] = self.__model._session.post(f"{self.__model._API}/chat.generateName?batch=1", 
											  headers=self.__model._HEADERS, json=__PAYLOAD).json()
		return Suggestion[0]["result"]["data"]["json"]["title"]


	@classmethod
	def Remove(self: type, id: str) -> None:
		conversations: List[Dict[str, str]] = self.GetList()
		PAYLOAD: Dict[str, str] = {
			"0": {
				"json": {
					"id": id,
					"workspaceId": self.__model._WORKSPACEID
				}
			}
		}

		for cv in conversations:
			if id == cv["id"]:
				DATA_: object = self.__model._session.post(f"{self.__model._API}/chat.removeChat?batch=1", 
									 json=PAYLOAD, headers=self.__model._HEADERS)

				if DATA_.status_code == 200:
					self.__model._logger.debug(f"Deleted conversation ({Fore.CYAN}{id}{Style.RESET_ALL}).")
				else:
					self.__model._logger.error(f"{Fore.RED}Error on delete conversation {id}{Style.RESET_ALL}")
					return None

	@classmethod
	def GetMessages(self: type, id: str) -> List[Dict[str, str]]:
		__PAYLOAD: Dict[str, str] = {
			"0": {
				"json": {
					"chatId": id,
					"workspaceId": self.__model._WORKSPACEID
				}
			}
		}
		DATA_: Dict[str, str] = self.__model._session.post(f"{self.__model._API}/chat.getMessagesByChatId?batch=1", 
										headers=self.__model._HEADERS, json=__PAYLOAD)

		if DATA_.status_code != 200:
			self.__model._logger.error(f"{Fore.RED}Error on get messages of conversation ({id}){Style.RESET_ALL}")
			return {}

		return DATA_.json()[0]["result"]["data"]["json"]["messages"]

	@classmethod
	def ClearAll(self: type) -> None:
		conversations: List[Dict[str, str]] = self.GetList()
		ct: int = 0

		for cv in conversations:
			if cv["type"] == "chat":
				self.Remove(cv["id"])
				ct += 1

		print(f"Deleted ({Fore.CYAN}{ct}{Style.RESET_ALL}) conversation(s).")