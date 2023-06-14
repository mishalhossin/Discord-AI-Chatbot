import re
import random
import aiohttp

async def replace_with_image_url(response):
    match = re.search(r'<draw:(.*?)>', response)

    if match:
        original_text = match.group(0)
        original_url = await get_random_image_url(match.group(1))
        
        if original_url is not None:
            replaced_response = response.replace(original_text, original_url)
        else:
            replaced_response = response.replace(original_text, "No results found")
        
        return replaced_response

    return response

async def get_random_image_url(query):
    encoded_query = aiohttp.helpers.quote(query)
    url = f'https://ddmm.ai/api/gsearch/a/{encoded_query}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                json_data = await response.json()
                images_results = json_data.get("images_results", [])
                if images_results:
                    original_urls = [result["original"] for result in images_results]
                    random_original_url = random.choice(original_urls)
                    return random_original_url
            else:
                return None
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
    API_URL = "https://api.popcat.xyz/translate?to=en"
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params={"text": text}) as response:
            data = await response.json()
            translation = data.get("translated")
            return translation
