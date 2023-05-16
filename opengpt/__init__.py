from typing import Optional, Union, Dict, List, Text
from .libraries.colorama import init, Fore, Style
import importlib
import yaml
import sys
import inspect
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

class OpenGPT:
	@classmethod
	def __init__(self: type, provider: Text, type: Optional[Text] = "completion", options: Optional[Union[Dict[Text, Text], None]] = None) -> None:
		self.__DIR: Text = os.path.dirname(os.path.abspath(__file__))
		self.__LoadModels()
		self.__TYPE: Text = type
		self.__OPTIONS: Union[Dict[Text, Text], None] = options
		self.__PROVIDER: Text = provider
		self.__Verifications()
		self.__MODULE: module = importlib.import_module(f"opengpt.models.{self.__TYPE}.{self.__PROVIDER}.model")
		self.__MODEL_CLASS: type = getattr(self.__MODULE, "Model")
		self.__model: type = None
		self.__InitializeModelClass()

	@classmethod
	def __InitializeModelClass(self: type) -> None:
		if not self.__OPTIONS is None:
			args: List[Text] = inspect.signature(self.__MODEL_CLASS.__init__)
			reqArgs: List[Text] = [
				param.name
				for param in args.parameters.values()
				if param.default == inspect.Parameter.empty
			]
			missingArgs: List[Text] = []

			for arg in reqArgs:
				if arg not in self.__OPTIONS:
					missingArgs.append(arg)

			if len(missingArgs) > 0:
				OpenGPTError.Print(f"Missing one of non-optional parameters: {', '.join(missingArgs)}")

			self.__model = self.__MODEL_CLASS(**self.__OPTIONS)
		else:
			self.__model = self.__MODEL_CLASS()

	@classmethod
	def __LoadModels(self: type) -> None:
		self.__DATA: Dict[Text, Text] = yaml.safe_load(open(self.__DIR + "/config.yml", "r").read())

	@classmethod
	def __Verifications(self: type) -> None:
		exists: bool = False

		if self.__TYPE not in self.__DATA["models"]:
			OpenGPTError.Print(f"The type \"{self.__TYPE}\" not be founded. Try: {', '.join(self.__DATA['models'])}")

		if self.__PROVIDER not in self.__DATA["models"][self.__TYPE]:
			for type in self.__DATA["models"]:
				for model in self.__DATA["models"][type]:
					if model == self.__PROVIDER:
						rest: Text = f"Changing to \"{type}\"."
						OpenGPTError.Print(context=f"The provider \"{self.__PROVIDER}\" not is from type \"{self.__TYPE}\". " + rest, warn=True)
						self.__TYPE = type
						exists = True
		else:
			exists = True

		if not exists:
			OpenGPTError.Print(f"The provider \"{self.__PROVIDER}\" not exists.")

		incompletRest: Text = ''
		rest: Text = ''
		
		if self.__DATA["models"][self.__TYPE][self.__PROVIDER]["state"] == "incomplete":
			incompletRest = f"The provider \"{self.__PROVIDER}\" is incomplete. "
			if len(self.__DATA["models"][self.__TYPE][self.__PROVIDER]["bugs"]) > 0:
				rest = "In addition to having some bugs that have not yet been fixed."

		if len(rest) > 0 or len(incompletRest) > 0:
			OpenGPTError.Print(context=incompletRest + rest + " It is recommended not to use.", warn=True)

	@classmethod
	def __getattr__(self: type, name: Text) -> None:
		if hasattr(self.__model, name):
			attr: type = getattr(self.__model, name)
			if callable(attr):
				return lambda *args, **kwargs: attr(*args, **kwargs)
			return attr
		raise AttributeError(f"\"OpenGPT\" object has no attribute \"{name}\"")
