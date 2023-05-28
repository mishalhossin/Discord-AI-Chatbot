import json
import hashlib
import random
import string
from fake_useragent import UserAgent
import aiohttp

class ChatCompletion:
    @classmethod
    def md5(cls, text):
        return hashlib.md5(text.encode()).hexdigest()[::-1]

    @classmethod
    def get_api_key(cls, user_agent):
        part1 = str(random.randint(0, 10**11))
        part2 = cls.md5(user_agent + cls.md5(user_agent + cls.md5(user_agent + part1 + "x")))
        return f"tryit-{part1}-{part2}"

    @classmethod
    async def create(cls, messages):
        user_agent = UserAgent().random
        api_key = cls.get_api_key(user_agent)
        headers = {
            "api-key": api_key,
            "user-agent": user_agent
        }
        files = {
            "chat_style": (None, "chat"),
            "chatHistory": (None, json.dumps(messages))
        }

        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.deepai.org/chat_response", headers=headers, data=files) as response:
                response.raise_for_status()
                full_response = ""
                while True:
                    chunk = await response.content.read()
                    if not chunk:
                        break
                    full_response += chunk.decode()

                return full_response

class Completion:
    @classmethod
    async def create(cls, prompt):
        return await ChatCompletion.create([
            {
                "role": "user",
                "content": prompt
            }
        ])
