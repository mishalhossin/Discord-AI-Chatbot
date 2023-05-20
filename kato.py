import asyncio
import aiohttp

async def GetAnswer(prompt):
    url = "https://www.kato.to/advancedApi/ai/chat"
    headers = {
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    payload = [
        {
            "role": "system",
            "content": "<p><b>I'm sorry, but sometimes I may provide inaccurate information since I'm still a work in progress.</b></p>"
        },
        {
            "role": "user",
            "content": f"{prompt}"
        }
    ]
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            return await response.text()
