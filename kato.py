import asyncio

async def GetAnswer(prompt):
    url = "https://www.kato.to/advancedApi/ai/chat"
    headers = {
        "content-type": "application/json"
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
