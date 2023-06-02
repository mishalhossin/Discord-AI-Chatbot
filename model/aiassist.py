import json

import aiohttp


class Completion:
    @staticmethod
    async def create(
            systemMessage: str = "You are a helpful assistant",
            prompt: str = "",
            parentMessageId: str = "",
            temperature: float = 0.8,
            top_p: float = 1,
    ):
        json_data = {
            "prompt": prompt,
            "options": {"parentMessageId": parentMessageId},
            "systemMessage": systemMessage,
            "temperature": temperature,
            "top_p": top_p,
        }

        url = "http://43.153.7.56:8080/api/chat-process"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_data) as response:
                content = await response.read()

        response = Completion.__load_json(content)
        return response

    @classmethod
    def __load_json(cls, content) -> dict:
        decode_content = str(content.decode("utf-8"))
        split = decode_content.rsplit("\n", 1)[1]
        to_json = json.loads(split)
        return to_json
