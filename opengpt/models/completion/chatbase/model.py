import aiohttp
import asyncio

class Model:
    captcha_code = "hadsa"

    async def get_answer(self, prompt: str, model: str = "gpt-4"):
        if model == "gpt-4":
            chat_id = "quran---tafseer-saadi-pdf-wbgknt7zn"
        elif model == "gpt-3.5-turbo":
            chat_id = "chatbase--1--pdf-p680fxvnm"
        messages = [{"role": "system", "content": ""}, {"role": "user", "content": prompt}]

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                "https://www.chatbase.co/api/fe/chat",
                json={"chatId": chat_id, "captchaCode": self.captcha_code, "messages": messages}
            )
            result = await response.text()

        return result
   


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
    
