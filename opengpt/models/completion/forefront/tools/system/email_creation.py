<<<<<<< HEAD:opengpt/models/completion/forefront/tools/system/email_creation.py
from typing import Dict
from libraries.tempmail import TempMail
from libraries.colorama import init, Fore, Style
from ..typing.response import EmailResponse
import re
import json
import logging
import fake_useragent
import tls_client

init()

class Email:
	@classmethod
	def __init__(self: type) -> None:
		self.__SETUP_LOGGER()
		self.__session: tls_client.Session = tls_client.Session(client_identifier="chrome_110")

	@classmethod
	def __SETUP_LOGGER(self: type) -> None:
		self.__logger: logging.getLogger = logging.getLogger(__name__)
		self.__logger.setLevel(logging.DEBUG)
		console_handler: logging.StreamHandler = logging.StreamHandler()
		console_handler.setLevel(logging.DEBUG)
		formatter: logging.Formatter = logging.Formatter("Account Creaction - %(levelname)s - %(message)s")
		console_handler.setFormatter(formatter)

		self.__logger.addHandler(console_handler)

	@classmethod
	def __AccountState(self: object, output: str, field: str) -> bool:
		if field not in output:
			return False
		return True

	@classmethod
	def CreateAccount(self: object) -> str:
		Mail = TempMail()
		MailAddress = Mail.GetAddress

		self.__session.headers = {
			"Origin": "https://accounts.forefront.ai",
			"User-Agent": fake_useragent.UserAgent().random
		}

		self.__logger.debug(Fore.CYAN + "Checking URL" + Style.RESET_ALL)
		
		output = self.__session.post("https://clerk.forefront.ai/v1/client/sign_ups?_clerk_js_version=4.38.4", data={"email_address": MailAddress})

		if not self.__AccountState(str(output.text), "id"):
			self.__logger.error(Fore.RED + "Failed to create account." + Style.RESET_ALL)
			return "Failed"

		trace_id = output.json()["response"]["id"]

		output = self.__session.post(f"https://clerk.forefront.ai/v1/client/sign_ups/{trace_id}/prepare_verification?_clerk_js_version=4.38.4", 
			data={"strategy": "email_link", "redirect_url": "https://accounts.forefront.ai/sign-up/verify"})

		if not self.__AccountState(output.text, "sign_up_attempt"):
			self.__logger.error(Fore.RED + "Failed to create account." + Style.RESET_ALL)
			return "Failed"

		self.__logger.debug(Fore.CYAN + "Verifying account" + Style.RESET_ALL)

		while True:
			messages: Mail.GetMessages = Mail.GetMessages()

			if len(messages) > 0:
				message: Dict[str, str] = Mail.GetMessage(messages[0]["_id"])
				verification_url = re.findall(r"https:\/\/clerk\.forefront\.ai\/v1\/verify\?token=\w.+", message["bodyHtml"])[0]
				if verification_url:
					break

		r = self.__session.get(verification_url.split("\"")[0])
		__client: str = r.cookies["__client"]

		output = self.__session.get("https://clerk.forefront.ai/v1/client?_clerk_js_version=4.38.4")
		token: str = output.json()["response"]["sessions"][0]["last_active_token"]["jwt"]
		sessionID: str = output.json()["response"]["last_active_session_id"]

		self.__logger.debug(Fore.GREEN + "Created account!" + Style.RESET_ALL)

=======
from typing import Dict
from .tempmail import TempMail
from ..typing.response import EmailResponse
import re
import json
import logging
import fake_useragent
import tls_client

class Email:
	@classmethod
	def __init__(self: type) -> None:
		self.__SETUP_LOGGER()
		self.__session: tls_client.Session = tls_client.Session(client_identifier="chrome_110")

	@classmethod
	def __SETUP_LOGGER(self: type) -> None:
		self.__logger: logging.getLogger = logging.getLogger(__name__)
		self.__logger.setLevel(logging.DEBUG)
		console_handler: logging.StreamHandler = logging.StreamHandler()
		console_handler.setLevel(logging.DEBUG)
		formatter: logging.Formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
		console_handler.setFormatter(formatter)

		self.__logger.addHandler(console_handler)

	@classmethod
	def __AccountState(self: object, output: str, field: str) -> bool:
		if field not in output:
			return False
		return True

	@classmethod
	def CreateAccount(self: object) -> str:
		Mail = TempMail()
		MailAddress = Mail.GetAddress

		self.__session.headers = {
			"Origin": "https://accounts.forefront.ai",
			"User-Agent": fake_useragent.UserAgent().random
		}

		self.__logger.debug("Checking URL")
		
		output = self.__session.post("https://clerk.forefront.ai/v1/client/sign_ups?_clerk_js_version=4.38.4", data={"email_address": MailAddress})

		if not self.__AccountState(str(output.text), "id"):
			self.__logger.error("Failed to create account :(")
			return "Failed"

		trace_id = output.json()["response"]["id"]

		output = self.__session.post(f"https://clerk.forefront.ai/v1/client/sign_ups/{trace_id}/prepare_verification?_clerk_js_version=4.38.4", 
			data={"strategy": "email_link", "redirect_url": "https://accounts.forefront.ai/sign-up/verify"})

		if not self.__AccountState(output.text, "sign_up_attempt"):
			self.__logger.error("Failed to create account :(")
			return "Failed"

		self.__logger.debug("Verifying account")

		while True:
			messages: Mail.GetMessages = Mail.GetMessages()

			if len(messages) > 0:
				message: Dict[str, str] = Mail.GetMessage(messages[0]["_id"])
				verification_url = re.findall(r"https:\/\/clerk\.forefront\.ai\/v1\/verify\?token=\w.+", message["bodyHtml"])[0]
				if verification_url:
					break

		r = self.__session.get(verification_url.split("\"")[0])
		__client: str = r.cookies["__client"]

		output = self.__session.get("https://clerk.forefront.ai/v1/client?_clerk_js_version=4.38.4")
		token: str = output.json()["response"]["sessions"][0]["last_active_token"]["jwt"]
		sessionID: str = output.json()["response"]["last_active_session_id"]

		self.__logger.debug("Created account!")

>>>>>>> 79cab608409c040e5ef9b9496ef0fce35d025764:opengpt/forefront/tools/system/email_creation.py
		return EmailResponse(**{"sessionID": sessionID, "client": __client})