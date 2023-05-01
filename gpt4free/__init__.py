from enum import Enum

from gpt4free import theb


class Provider(Enum):
    """An enum representing  different providers."""

    Theb = 'theb'


class Completion:
    """This class will be used for invoking the given provider"""

    @staticmethod
    def create(provider: Provider, prompt: str, **kwargs) -> str:
        
        """
        Invokes the given provider with given prompt and addition arguments and returns the string response

        :param provider: an enum representing the provider to use while invoking
        :param prompt: input provided by the user
        :param kwargs:  Additional keyword arguments to pass to the provider while invoking
        :return: A string representing the response from the provider
        """
        if provider == Provider.Theb:
            return Completion.__theb_service(prompt, **kwargs)
        else:
            raise Exception('Provider not exist, Please try again')

    @staticmethod
    def __theb_service(prompt: str, **kwargs):
        return ''.join(theb.Completion.create(prompt=prompt))
