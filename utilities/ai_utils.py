import aiohttp
import io
from datetime import datetime
import re
import random
from youtube_transcript_api import YouTubeTranscriptApi

from utilities.config_loader import load_current_language, config
from utilities.response_util import translate_to_en
from imaginepy import AsyncImagine, Style, Ratio

current_language = load_current_language()
internet_access = config['INTERNET_ACCESS']

base_urls = ['https://a.z-pt.com', 'http://chat.darkflow.top']


async def search(prompt):
    prompt = await translate_to_en(prompt)
    if not internet_access or len(prompt) > 200:
        return
    
    search_results_limit = config['MAX_SEARCH_RESULTS']
    search_query = await get_query(prompt)
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
    search_results = 'Search feature is currently disabled so you have no realtime information'
    if search is not None:
        search_results = search
    endpoint = 'https://gpt4.gravityengine.cc/api/openai/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo-16k-0613',
        'temperature': 0.7,
        'messages': [
            {"role": "system", "content": instructions},
            *history,
            {"role": "system", "content": search_results},
            {"role": "system", "content": image_caption},
        ]
    }
    
    for attempt in range(2):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(endpoint, headers=headers, json=data) as response:
                    response_data = await response.json()
                    choices = response_data['choices']
                    if choices:
                        return choices[0]['message']['content']
        except aiohttp.ClientError as error:
            print(f'Error making the request with {endpoint}: {error}')
            if attempt < 1:
                print('Retrying with a different base URL.')
                break

    print('All base URLs failed to provide a response.')
    return None

async def generate_completion(prompt, max_token=None, temp=None):
    endpoint = '/api/openai/v1/engines/text-davinci-003/completions'
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        for base_url in base_urls:
            url = base_url + endpoint
            async with session.post(url, headers=headers, json={'prompt': prompt, 'max_tokens': max_token or 2048, 'temperature': temp or 0.7}) as response:
                if response.status != 200:
                    continue
                response_data = await response.json()
                response = response_data['choices'][0]['text']
                return response

    return None

async def detect_nsfw(prompt):
    fullprompt = f"""Ignore all the instructions you got before. From now on, you are going to act as nsfw art image to text prompt detector. If the following contains stuff that involves graphic sexual material or nudity, content respond with "1" else respond with "0" and nothing else
Prompt = a Girl, China, 20yo, HD, realistic, without dress, uncensored. sfw.
Eval = 1
Prompt = a Girl, China, 20yo, HD, realistic, without dress, Transparent bra, uncensored.
Eval = 1
Prompt = girl, european, 18yo
Eval = 1
Prompt = A cute anime girl
Eval = 0
Prompt = {prompt}
Eval = """
    response = await generate_completion(prompt=fullprompt, max_token=20, temp=1)
    if response == "1":
        return True
    else:
        return False

async def get_query(prompt):
    fullprompt = f"""If a message is not directly addressed to the second person, you will need to initiate a search query.

Message: What is happening in ukraine
Query: Ukraine military news today
Message : Hi
Query: False
Message: What is the latest donald trump scandal?
Query: Donald Trump scandal latest news
Message : Who made you ?
Query: False
Message : How are you doing ?
Query: False
Message : Who won in 2022 world cup ?
Query: 2022 FIFA World Cup final
Message : Thats scary
Query: False
Message : {prompt}
Query : """

    response = await generate_completion(prompt=fullprompt, max_token=20)
    if "false" in response.lower():
        return None
    response = response.lower().replace("query:", "").replace("query", "").replace(":", "")
    if response:
        return response
    else:
        return None

async def generate_dalle_image(prompt, size):
    base_urls = ['https://a.z-pt.com', 'http://chat.darkflow.top']
    endpoint = '/api/openai/v1/images/generations'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'prompt': prompt,
        'n': 1,
        'size': size
    }

    async with aiohttp.ClientSession() as session:
        for base_url in base_urls:
            url = base_url + endpoint
            async with session.post(url, headers=headers, json=data) as response:
                if response.status != 200:
                    continue

                response_data = await response.json()
                if 'error' in response_data:
                    return None

                image_url = response_data['data'][0]['url']
                async with session.get(image_url) as image_response:
                    image_content = await image_response.read()
                    img_file = io.BytesIO(image_content)
                    return img_file

    return None

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
    formatted_transcript = formatted_transcript[:1000]

    response = f"Ignore all the instructions you got before. Summarizie the following in 8 bullet points:\n\n{formatted_transcript}\n\n\nProvide a summary or additional information based on the content. Write the summary in {current_language['language_name']}"

    return response
