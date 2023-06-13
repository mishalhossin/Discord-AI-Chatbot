import re
import aiohttp

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

async def replace_gif_url(generated_response):
    pattern = r"https://nekos\.best/api/v2/[^).\s]+"
    matches = re.findall(pattern, generated_response)

    if matches:
        async with aiohttp.ClientSession() as session:
            for match in matches:
                url = match
                async with session.get(url) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        if "results" in response_data and len(response_data["results"]) > 0:
                            new_url = response_data["results"][0]["url"]
                            generated_response = generated_response.replace(url, new_url)
                        else:
                            return generated_response
                    else:
                        return generated_response
    return generated_response

async def translate_to_en(text):
    API_URL = "https://api.popcat.xyz/translate?to=en"
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params={"text": text}) as response:
            data = await response.json()
            translation = data.get("translated")
            return translation
