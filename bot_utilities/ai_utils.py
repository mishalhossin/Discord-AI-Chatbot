import aiohttp
import asyncio
import io
import json
import openai
import os
import re
import requests
import time
import random

from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote
from bot_utilities.config_loader import load_current_language, config

from dotenv import load_dotenv

from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chains import LLMMathChain
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import MessagesPlaceholder, PromptTemplate
from langchain.schema import SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
current_language = load_current_language()
internet_access = config['INTERNET_ACCESS']

openai.api_key = os.getenv('CHIMERA_GPT_KEY')
openai.api_base = "https://api.naga.ac/v1"
openai.model = config['GPT_MODEL']
openai.max_tokens = config['MAX_TOKENS']

browserless_token = os.getenv('BROWSERLESS_TOKEN')
serp_api_key = os.getenv('SERP_API_KEY')

def sdxl(prompt):
    response = openai.Image.create(
    model="sdxl",
    prompt=prompt,
    n=1,  # images count
    size="1024x1024"
)
    return response['data'][0]["url"]

def summary(text):
    """
    The following function defines an llm chain that summarizes scraped content if its is too long.
    This uses paragraph and escape splits as seperators for a recursive character text splitter as well as map_reduce for the summarizing strategy

    """
    # Define the system prompt 
    map_reduce_prompt = """
    Write a summary of the following website content:
    "{text}"
    SUMMARY:
    """

    llm = ChatOpenAI(openai_api_base = openai.api_base,
    openai_api_key = openai.api_key,
    temperature=0,
    model=openai.model,
    max_tokens=openai.max_tokens)

    # Prepare splitter and split content
    text_splitter = RecursiveCharacterTextSplitter(separators=["/n/n", "\n"], chunk_size=5000, chunk_overlap=350)
    split_website_text = text_splitter.create_documents([text])

    # Prepare summarizer chain
    summary_prompt_template = PromptTemplate(template=map_reduce_prompt, input_variables=["text"])
    summarize_chain = load_summarize_chain(llm=llm, chain_type='map_reduce', map_prompt=summary_prompt_template)

    summary = summarize_chain.run(split_website_text)
    return summary

def scrape_website(url: str):
    """
    Defining a website scraping tool, this tool will also summarize content if the website is too long

    """
    headers = {
        'Content-Type': 'application/json',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.1234.567 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate'
    }

    data = {
        "url": url
    }

    error_message = "I appear to be having issues with this request"

    data_json = json.dumps(data)
    try:
        # Fast and reliable web scraping and browser automation for any size project. Todo: Create and update token
        response = requests.post(f"https://chrome.browserless.io/content?token={browserless_token}", headers=headers, data=data_json)

        # parse content
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text()

            if len(text) > 5000:
                text = summary(text)
                
            return text
        else:
            print(f"HTTP request failed with status code {response.status_code}")
            return error_message
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"An error occurred: {e}")
        return error_message

def search(query):
    """
    A tool that enables search functionality over the web for auxillary knowledge to boost the LLM's capability

    """
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })
    headers = {
        'X-API-KEY': f'{serp_api_key}',
        'Content-Type': 'application/json',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.1234.567 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate'
    }

    error_message = {"data": "I appear to be having issues with this request"}
    error_obj = json.dumps(error_message)
    
    #try:
    # Make the GET request
    response = requests.request("POST", url, headers=headers, data=payload)

    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()

        return results
    else:
        print(f"HTTP request failed with status code {response.status_code}")
        return error_obj
    #except (requests.exceptions.RequestException, ValueError) as e:
    #    print(f"An error occurred: {e}")
    #    return error_obj



def create_agent(id, instructions):
    system_message = SystemMessage(
        content=instructions
    )

    agent_kwargs = {
        "system_message": system_message,
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }

    memory = ConversationBufferWindowMemory(memory_key="memory", return_messages=True)

    llm = ChatOpenAI(openai_api_base = openai.api_base,
        openai_api_key = openai.api_key,
        temperature=0,
        model=openai.model,
        max_tokens=openai.max_tokens)

    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    tools = [  
        Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
        ),
        Tool(
        name="Search",
        func=search,
        description = "Only use this to answer questions about events, data, or terms that you don't really understand. You should ask targeted questions"
        ),
        Tool(
            name="Scrape_website",
            func = scrape_website,
            description = "Use this to pull content and knowledge from a website url"
        ),
    ]
    
    # Todo: Consider replacing agent type with SELF_ASK_WITH_SEARCH
    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory
    )

    agent_db[id] = agent
    
    return agent
    
async def fetch_models():
    return openai.Model.list()

agent_db = {}

def generate_response(instructions, user_input):
    id = user_input["id"]
    message = user_input["message"]


    # Establish new agent if one doesnt exist for the current user
    if id not in agent_db:
        agent = create_agent(id, instructions)
        # Starting message to establish the user's handle
        message = "My username is " + user_input["name"] + ". " + message
    else:
        agent = agent_db[id]

    time_start = datetime.now()
    print(f"User request started at: {time_start.strftime('%Y-%m-%d %H:%M:%S')}")
    response = agent.run(message)
    time_end = datetime.now()
    print(f"User request ended at: {time_end.strftime('%Y-%m-%d %H:%M:%S')}. Total duration: {time_end - time_start}")

    return response

# Todo: Remove
async def search_old(prompt):
    """
    Asynchronously searches for a prompt and returns the search results as a blob.

    Args:
        prompt (str): The prompt to search for.

    Returns:
        str: The search results as a blob.

    Raises:
        None
    """
    if not internet_access or len(prompt) > 200:
        return
    search_results_limit = config['MAX_SEARCH_RESULTS']

    # Find if any URL's matched and I imagine get those if required
    url_match = re.search(r'(https?://\S+)', prompt)
    if url_match:
        search_query = url_match.group(0) 
    else:
        search_query = prompt

    # Cant do long searches
    if search_query is not None and len(search_query) > 200:
        return

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    blob = f"Search results for: '{search_query}' at {current_time}:\n"
    if search_query is not None:
        try:
            async with aiohttp.ClientSession() as session:
                # Search uses duck-duck-go api
                async with session.get('https://ddg-api.awam.repl.co/api/search',
                                       params={'query': search_query, 'maxNumResults': search_results_limit}) as response:
                    search = await response.json()
        except aiohttp.ClientError as e:
            print(f"An error occurred during the search request: {e}")
            return

        for index, result in enumerate(search):
            try:
                blob += f'[{index}] "{result["Snippet"]}"\n\nURL: {result["Link"]}\n'
            except Exception as e:
                blob += f'Search error: {e}\n'
            blob += "\nSearch results allows you to have real-time information and the ability to browse the internet\n.As the links were generated by the system rather than the user, please send a response along with the link if necessary.\n"
        return blob
    else:
        blob = "No search query is needed for a response"
    return blob

# Todo: remove
def generate_response_old(instructions, search, history):
    if search is not None:
        search_results = search
    elif search is None:
        search_results = "Search feature is disabled"
    messages = [
            {"role": "system", "name": "instructions", "content": instructions},
            *history,
            {"role": "system", "name": "search_results", "content": search_results},
        ]
    response = openai.ChatCompletion.create(
        model=config['GPT_MODEL'],
        messages=messages
    )
    message = response.choices[0].message.content
    return message

def generate_gpt4_response(prompt):
    messages = [
            {"role": "system", "name": "admin_user", "content": prompt},
        ]
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=messages
    )
    message = response.choices[0].message.content
    return message

async def poly_image_gen(session, prompt):
    seed = random.randint(1, 100000)
    image_url = f"https://image.pollinations.ai/prompt/{prompt}?seed={seed}"
    async with session.get(image_url) as response:
        image_data = await response.read()
        image_io = io.BytesIO(image_data)
        return image_io

# async def fetch_image_data(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.read()

async def dall_e_gen(model, prompt, size, num_images):
    response = openai.Image.create(
        model=model,
        prompt=prompt,
        n=num_images,
        size=size,
    )
    imagefileobjs = []
    for image in response["data"]:
        image_url = image["url"]
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                content = await response.content.read()
                img_file_obj = io.BytesIO(content)
                imagefileobjs.append(img_file_obj)
    return imagefileobjs
    

async def generate_image_prodia(prompt, model, sampler, seed, neg):
    print("\033[1;32m(Prodia) Creating image for :\033[0m", prompt)
    start_time = time.time()
    async def create_job(prompt, model, sampler, seed, neg):
        if neg is None:
            negative = "(nsfw:1.5),verybadimagenegative_v1.3, ng_deepnegative_v1_75t, (ugly face:0.8),cross-eyed,sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy, DeepNegative, facing away, tilted head, {Multiple people}, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worstquality, low quality, normal quality, jpegartifacts, signature, watermark, username, blurry, bad feet, cropped, poorly drawn hands, poorly drawn face, mutation, deformed, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, extra fingers, fewer digits, extra limbs, extra arms,extra legs, malformed limbs, fused fingers, too many fingers, long neck, cross-eyed,mutated hands, polar lowres, bad body, bad proportions, gross proportions, text, error, missing fingers, missing arms, missing legs, extra digit, extra arms, extra leg, extra foot, repeating hair, nsfw, [[[[[bad-artist-anime, sketch by bad-artist]]]]], [[[mutation, lowres, bad hands, [text, signature, watermark, username], blurry, monochrome, grayscale, realistic, simple background, limited palette]]], close-up, (swimsuit, cleavage, armpits, ass, navel, cleavage cutout), (forehead jewel:1.2), (forehead mark:1.5), (bad and mutated hands:1.3), (worst quality:2.0), (low quality:2.0), (blurry:2.0), multiple limbs, bad anatomy, (interlocked fingers:1.2),(interlocked leg:1.2), Ugly Fingers, (extra digit and hands and fingers and legs and arms:1.4), crown braid, (deformed fingers:1.2), (long fingers:1.2)"
        else:
            negative = neg
        url = 'https://api.prodia.com/generate'
        params = {
            'new': 'true',
            'prompt': f'{quote(prompt)}',
            'model': model,
            'negative_prompt': f"{negative}",
            'steps': '100',
            'cfg': '9.5',
            'seed': f'{seed}',
            'sampler': sampler,
            'upscale': 'True',
            'aspect_ratio': 'square'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                return data['job']
            
    job_id = await create_job(prompt, model, sampler, seed, neg)
    url = f'https://api.prodia.com/job/{job_id}'
    headers = {
        'authority': 'api.prodia.com',
        'accept': '*/*',
    }

    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url, headers=headers) as response:
                json = await response.json()
                if json['status'] == 'succeeded':
                    async with session.get(f'https://images.prodia.xyz/{job_id}.png?download=1', headers=headers) as response:
                        content = await response.content.read()
                        img_file_obj = io.BytesIO(content)
                        duration = time.time() - start_time
                        print(f"\033[1;34m(Prodia) Finished image creation\n\033[0mJob id : {job_id}  Prompt : ", prompt, "in", duration, "seconds.")
                        return img_file_obj
