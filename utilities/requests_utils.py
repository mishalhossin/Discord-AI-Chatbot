import aiohttp
import asyncio
import os
import uuid
from utilities.config_loader import config

API_URLS = config['OCR_MODEL_URLS']

async def fetch_response(client, api_url, data):
    headers = {"Content-Type": "application/json"}
    async with client.post(api_url, headers=headers, data=data, timeout=40) as response:
        if response.status != 200:
            raise Exception(f"API request failed with status code {response.status}: {await response.text()}")

        return await response.json()

async def query(filename):
    with open(filename, "rb") as f:
        data = f.read()

    async with aiohttp.ClientSession() as client:
        tasks = [fetch_response(client, api_url, data) for api_url in API_URLS]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    return responses


async def download_image(image_url, save_as):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            with open(save_as, "wb") as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
    await session.close()


async def process_image_link(image_url):
    image_type = image_url.split('.')[-1]
    image_type = image_type.rsplit('.', 1)[0]
    temp_image = f"{str(uuid.uuid4())}.{image_type}"
    await download_image(image_url, temp_image)
    output = await query(temp_image)
    os.remove(temp_image)
    return output