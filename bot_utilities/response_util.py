import re
import random
import aiohttp
from langdetect import detect

async def replace_with_image_url(response):
    if match := re.search(r'<draw:(.*?)>', response):
        original_text = match.group(0)
        original_url = await get_random_image_url(match.group(1))

        return (
            response.replace(original_text, original_url)
            if original_url is not None
            else response.replace(original_text, "No results found")
        )
    return response

async def get_random_image_url(query):
    encoded_query = aiohttp.helpers.quote(query)
    url = f'https://ddmm.ai/api/gsearch/a/{encoded_query}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            json_data = await response.json()
            if images_results := json_data.get("images_results", []):
                original_urls = [result["original"] for result in images_results]
                return random.choice(original_urls)
    return None

def split_response(response, max_length=1999):
    lines = response.splitlines()
    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = line
        else:
            if current_chunk:
                current_chunk += "\n"
            current_chunk += line

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

async def translate_to_en(text):
    detected_lang = detect(text)
    if detected_lang == "en":
        return text
    API_URL = "https://api.pawan.krd/gtranslate"
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params={"text": text,"from": detected_lang,"to": "en",}) as response:
            data = await response.json()
            return data.get("translated")

async def get_random_prompt(prompt):
    url = 'https://lexica.art/api/infinite-prompts'
    headers = {
        'authority': 'lexica.art',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://lexica.art',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    data = {
        'text': prompt,
        'searchMode': 'images',
        'source': 'search',
        'cursor': 0,
        'model': 'lexica-aperture-v2'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status != 200:
                return prompt
            response_json = await response.json()
            prompts = response_json['prompts']
            random_prompt = random.choice(prompts)
            return random_prompt['prompt']