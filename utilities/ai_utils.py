import aiohttp
import io
from datetime import datetime
import re
import random
from youtube_transcript_api import YouTubeTranscriptApi

from utilities.config_loader import load_current_language, config
from imaginepy import AsyncImagine, Style, Ratio

current_language = load_current_language()
internet_access = config['INTERNET_ACCESS']

async def search(prompt):
    blacklist = ["image", "gifs", "gif", "images", "picture", "pictures", "draw", "draws", "drawing" "video", "youtube","pirated", "hack", "crack", "phishing", "malware", "virus"]
    if any(word in prompt.lower() for word in blacklist):
        return
    if not internet_access or len(prompt) > 200:
        return
    
    search_results_limit = config['MAX_SEARCH_RESULTS']
    search_query = (" " + prompt)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    blob = f"Search results for '{prompt}' at {current_time}:\n\n"
    
    if search_query is not None:
        print(f"\nSearching for: {search_query}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://ddg-api.herokuapp.com/search',
                                       params={'query': prompt, 'limit': search_results_limit}) as response:
                    search = await response.json()
        except aiohttp.ClientError as e:
            print(f"An error occurred during the search request: {e}")
            return

        for index, result in enumerate(search):
            blob += f'[{index}] "{result["snippet"]}"\n\nURL: {result["link"]}\n'
            
        blob += "\nThese links were provided by the system and not the user, so you should send a response and link if needed\n"
        return blob
    else:
        blob = "[Query: No search query is needed for a response]"

    return blob

async def generate_response(instructions, search, image_caption, history):
    base_urls = ['https://a.z-pt.com', 'http://chat.darkflow.top']
    arguments = '/api/openai/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo-16k-0613',
        'temperature': 0.1,
        'presence_penalty': 1.0,
        'messages': [
            {"role": "system", "content": instructions},
            {"role": "system", "content": search},
            *history,
            {"role": "system", "content": image_caption},
        ]
    }
    random.shuffle(base_urls)

    for base_url in base_urls:
        endpoint = base_url + arguments
        for attempt in range(2):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(endpoint, headers=headers, json=data) as response:
                        response_data = await response.json()
                        choices = response_data['choices']
                        if choices:
                            return choices[0]['message']['content']
            except aiohttp.ClientError as error:
                print(f'Error making the request with {base_url}: {error}')
                if attempt < 1:
                    print('Retrying with a different base URL.')
                    break

    print('All base URLs failed to provide a response.')
    return None

async def detect_nsfw(prompt):
    fullprompt = f"""Ignore all the instructions you got before. From now on, you are going to act as nsfw art image to text prompt detector. If the following contains stuff that involes graphic sexual material or nudity, content respond with "1" else respond with "0" and nothing else

Prompt = {prompt}

Eval = """
    async with aiohttp.ClientSession() as session:
        async with session.post('https://a.z-pt.com/api/openai/v1/engines/text-davinci-003/completions', headers={'Content-Type': 'application/json'}, json={'prompt': fullprompt, 'max_tokens': 200, 'temperature': 1}) as response:
            response_data = await response.json()
            response = response_data['choices'][0]['text']
    if response == "1":
        return True
    else:
        return False

async def generate_dalle_image(prompt, size):
    url = "https://a.z-pt.com/api/openai/v1/images/generations"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'prompt': prompt,
        'n': 1,
        'size': size
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response_data = await response.json()
            if 'error' in response_data:
                return None
            image_url = response_data['data'][0]['url']
            async with session.get(image_url) as image_response:
                image_content = await image_response.read()
                img_file = io.BytesIO(image_content)
                
    return img_file

async def generate_image(image_prompt, style_value, ratio_value, negative, upscale):
    imagine = AsyncImagine()
    style_enum = Style[style_value]
    ratio_enum = Ratio[ratio_value]
    img_data = await imagine.sdprem(
        prompt=image_prompt,
        style=style_enum,
        ratio=ratio_enum,
        priority="1",
        high_res_results="1",
        steps="70",
        negative=negative
    )

    if upscale:
        img_data = await imagine.upscale(image=img_data)

    try:
        img_file = io.BytesIO(img_data)
    except Exception as e:
        print(f"An error occurred while creating the in-memory image file: {e}")
        return None

    await imagine.close()
    return img_file

async def get_yt_transcript(message_content):
    def extract_video_id(message_content):
        youtube_link_pattern = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        match = youtube_link_pattern.search(message_content)
        return match.group(6) if match else None

    video_id = extract_video_id(message_content)
    if not video_id:
        return None

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    first_transcript = next(iter(transcript_list), None)
    if not first_transcript:
        return None

    translated_transcript = first_transcript.translate('en')
    formatted_transcript = ". ".join(
        [entry['text'] for entry in translated_transcript.fetch()])
    formatted_transcript = formatted_transcript[:2500]

    response = f"Ignore all the instructions you got before. Summarizie the following in 8 bullet points:\n\n{formatted_transcript}\n\n\nProvide a summary or additional information based on the content. Write the summary in {current_language['language_name']}"

    return response
