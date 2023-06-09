import json
import aiohttp

class Completion:
    @staticmethod
    async def createStreaming(
            systemMessage: str = "You are a helpful assistant",
            prompt: str = "",
            parentMessageId: str = "",
            temperature: float = 0.7,
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
                buffer = ""
                async for chunk in response.content.iter_any():
                    chunk = chunk.decode("utf-8")
                    buffer += chunk
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        if line.strip():
                            data = json.loads(line)
                            text = data["text"]
                            yield text
    @staticmethod
    async def create(
            systemMessage: str = "You are a helpful assistant",
            prompt: str = "",
            parentMessageId: str = "",
            temperature: float = 0.7,
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
        split = decode_content.rsplit("\n", 1)
        if len(split) > 1:
            to_json = json.loads(split[1])
            return to_json
        else:
            return {}