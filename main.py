import os
import re
import json
import uuid
import asyncio
import aiohttp
import discord
from imaginepy import AsyncImagine, Style, Ratio
from datetime import datetime
from model import Model
from youtube_transcript_api import YouTubeTranscriptApi
from discord import Embed, Colour, app_commands
from discord.ext import commands
from dotenv import load_dotenv
import replit_detector

load_dotenv()
# Config
with open('config.json') as config_file:
    config = json.load(config_file)

# Set up the Discord bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents, heartbeat_timeout=60)
TOKEN = os.getenv('DISCORD_TOKEN') # Loads Discord bot token from env

# Keep track of the channels where the bot should be active
allow_dm = True
active_channels = set()
trigger_words = config['TRIGGER']

# Internet access
internet_access = True

# Language settings
current_language_code = "en"
valid_language_codes = []
lang_directory = "lang"

for filename in os.listdir(lang_directory):
    if filename.startswith("lang.") and os.path.isfile(os.path.join(lang_directory, filename)):
        language_code = filename.split(".")[1]
        valid_language_codes.append(language_code)

def load_current_language():
    lang_file_path = os.path.join(lang_directory, f"lang.{current_language_code}")
    with open(lang_file_path, encoding="utf-8") as lang_file:
        current_language = json.load(lang_file)
    return current_language

current_language = load_current_language()

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="Coded by Mishal#1916"))
    print(f"{bot.user} aka {bot.user.name} has connected to Discord!")

    invite_link = discord.utils.oauth_url(
        bot.user.id,
        permissions=discord.Permissions(),
        scopes=("bot", "applications.commands")
    )
    print(f"Invite link: {invite_link}")

# Set up the Chat bot
instructions = current_language["instructions"]
evagpt4 = Model()
async def generate_response(history, search, yt_transcript, image_caption, botname, username):
    messages = [
        {"role": "system", "content": f"{instructions}. And your name is {botname} and users name is{username}. And only respond in the language the user is speaking, e.g., Vietnamese or English, etc."},
        *history,
        {
            "role": "system",
            "content": f"The following are the related search results, if any: {search}  if its None then user hasnt any questions\n\n" +
                       f"{yt_transcript} if its None then user hasnt provided it\n\n" +
                       f"Additionally, here is any attachment captioning: {image_caption} if its None then user hasnt provided it "
        }
    ]
    response = await evagpt4.ChatCompletion(messages)
    return response

def split_response(response, max_length=1900):
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

async def get_transcript_from_message(message_content):
    def extract_video_id(message_content):
        youtube_link_pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
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
    formatted_transcript = ". ".join([entry['text'] for entry in translated_transcript.fetch()])
    formatted_transcript = formatted_transcript[:2500]

    response = f"Summarizing the following in 10 bullet points ::\n\n{formatted_transcript}\n\n\n.Provide a summary or additional information based on the content."

    return response

async def search(prompt):
    if not internet_access:
        return

    wh_words = ['search', 'find', 'who', 'what', 'when', 'where', 'why', 'which', 'whom', 'whose', 'how',
         'is', 'are', 'am', 'can', 'could', 'should', 'would', 'do', 'does', 'did',
         'may', 'might', 'shall', 'will', 'have', 'has', 'had', 'must', 'ought', 'need',
         'want', 'like', 'prefer', 'tìm', 'tìm kiếm', 'làm sao', 'khi nào', 'hỏi', 'nào', 'google',
         'muốn hỏi', 'phải làm', 'cho hỏi']
                
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async with aiohttp.ClientSession() as session:
        async with session.get('https://ddg-api.herokuapp.com/search', params={'query': prompt, 'limit': 2}) as response:
            search = await response.json()

    blob = f"Search results for '{prompt}' at {current_time}:\n\n"
    for word in prompt.split():
        if any(wh_word in word.lower() for wh_word in wh_words):
            for index, result in enumerate(search):
                blob += f'[{index}] "{result["snippet"]}"\n\nURL: {result["link"]}\n\nThese links were provided by the system and not the user, so you should send the link to the user.\n'
            return blob

    return None

api_key = os.getenv('HUGGING_FACE_API')

API_URLS = [
    "https://api-inference.huggingface.co/models/microsoft/trocr-base-printed",
    "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning",
]
headers = {"Authorization": f"Bearer {api_key}"}

async def generate_image(image_prompt, style_value, ratio_value, negative):
    imagine = AsyncImagine()
    filename = str(uuid.uuid4()) + ".png"
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
    try:
        with open(filename, mode="wb") as img_file:
            img_file.write(img_data)
    except Exception as e:
        print(f"An error occurred while writing the image to file: {e}")
        return None

    await imagine.close()

    return filename

async def fetch_response(client, api_url, data):
    headers = {"Content-Type": "application/json"}
    async with client.post(api_url, headers=headers, data=data, timeout=20) as response:
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


message_history = {}
MAX_HISTORY = 8

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.reference and message.reference.resolved.author != bot.user:
        return  # Ignore replies to messages

    author_id = str(message.author.id)
    if author_id not in message_history:
        message_history[author_id] = []

    message_history[author_id].append({"role": "user", "content": message.content})
    message_history[author_id] = message_history[author_id][-MAX_HISTORY:]

    is_replied = message.reference and message.reference.resolved.author == bot.user
    is_dm_channel = isinstance(message.channel, discord.DMChannel)
    is_active_channel = message.channel.id in active_channels
    is_allowed_dm = allow_dm and is_dm_channel
    contains_trigger_word = any(word in message.content for word in trigger_words)
    is_bot_mentioned = bot.user.mentioned_in(message)
    bot_name_in_message = bot.user.name.lower() in message.content.lower()

    if is_active_channel or is_allowed_dm or contains_trigger_word or is_bot_mentioned or is_replied or bot_name_in_message:
        has_image = False
        image_caption = ""
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', 'webp')):
                    caption = await process_image_link(attachment.url)
                    has_image = True
                    image_caption = f"""{current_language["instruc_image_caption"]}{caption}.]"""
                    print(caption)
                    break

        search_results = await search(message.content)
        yt_transcript = await get_transcript_from_message(message.content)
        history = message_history[author_id]
        botname = bot.user.name
        username = message.author.name

        async def generate_response_in_thread(history, yt_transcript, image_caption, botname, username):
            temp_message = await message.channel.send("https://cdn.discordapp.com/emojis/1075796965515853955.gif?size=96&quality=lossless")
            response = await generate_response(history, search_results, yt_transcript, image_caption, botname, username)
            message_history[author_id].append({"role": "assistant", "content": response})
            chunks = split_response(response)
            for chunk in chunks:
                await message.reply(chunk)
            await temp_message.delete()
        async with message.channel.typing():
            asyncio.create_task(generate_response_in_thread(history, yt_transcript, image_caption, botname, username))



@bot.hybrid_command(name="pfp", description=current_language["pfp"])
async def pfp(ctx, attachment_url=None):
    if attachment_url is None and not ctx.message.attachments:
        return await ctx.send(
            f"{current_language['pfp_change_msg_1']}"
        )
    else:
        await ctx.send(
            f"{current_language['pfp_change_msg_2']}"
        )
    if attachment_url is None:
        attachment_url = ctx.message.attachments[0].url

    async with aiohttp.ClientSession() as session:
        async with session.get(attachment_url) as response:
            await bot.user.edit(avatar=await response.read())

@bot.hybrid_command(name="ping", description=current_language["ping"])
async def ping(ctx):
    latency = bot.latency * 1000
    await ctx.send(f"{current_language['ping_msg']}{latency:.2f} ms")

@bot.hybrid_command(name="changeusr", description=current_language["changeusr"])
@commands.is_owner()
async def changeusr(ctx, new_username):
    temp_message = await ctx.send(f"{current_language['changeusr_msg_1']}")
    taken_usernames = [user.name.lower() for user in bot.get_all_members()]
    if new_username.lower() in taken_usernames:
        await temp_message.edit(content=f"{current_language['changeusr_msg_2_part_1']}{new_username}{current_language['changeusr_msg_2_part_2']}")
        return
    try:
        await bot.user.edit(username=new_username)
        await temp_message.edit(content=f"{current_language['changeusr_msg_3']}'{new_username}'")
    except discord.errors.HTTPException as e:
        await temp_message.edit(content="".join(e.text.split(":")[1:]))


@bot.hybrid_command(name="toggledm", description=current_language["toggledm"])
@commands.has_permissions(administrator=True)
async def toggledm(ctx):
    global allow_dm
    allow_dm = not allow_dm
    await ctx.send(f"DMs are now {'on' if allow_dm else 'off'}")

@bot.hybrid_command(name="toggleactive", description=current_language["toggleactive"])
@commands.has_permissions(administrator=True)
async def toggleactive(ctx):
    channel_id = ctx.channel.id
    if channel_id in active_channels:
        active_channels.remove(channel_id)
        with open("channels.txt", "w") as f:
            for id in active_channels:
                f.write(str(id) + "\n")
        await ctx.send(
            f"{ctx.channel.mention} {current_language['toggleactive_msg_1']}"
        )
    else:
        active_channels.add(channel_id)
        with open("channels.txt", "a") as f:
            f.write(str(channel_id) + "\n")
        await ctx.send(
            f"{ctx.channel.mention} {current_language['toggleactive_msg_2']}")

# Read the active channels from channels.txt on startup
if os.path.exists("channels.txt"):
    with open("channels.txt", "r") as f:
        for line in f:
            channel_id = int(line.strip())
            active_channels.add(channel_id)


@bot.hybrid_command(name="bonk", description=current_language["bonk"])
async def bonk(ctx):
    message_history.clear()  # Reset the message history dictionary
    await ctx.send(f"{current_language['bonk_msg']}")


@bot.hybrid_command(name="imagine", description=current_language["imagine"])
@app_commands.choices(style=[
    app_commands.Choice(name='Imagine V4 Beta', value='IMAGINE_V4_Beta'),
    app_commands.Choice(name='Realistic', value='REALISTIC'),
    app_commands.Choice(name='Anime', value='ANIME_V2'),
    app_commands.Choice(name='Disney', value='DISNEY'),
    app_commands.Choice(name='Studio Ghibli', value='STUDIO_GHIBLI'),
    app_commands.Choice(name='Graffiti', value='GRAFFITI'),
    app_commands.Choice(name='Medieval', value='MEDIEVAL'),
    app_commands.Choice(name='Fantasy', value='FANTASY'),
    app_commands.Choice(name='Neon', value='NEON'),
    app_commands.Choice(name='Cyberpunk', value='CYBERPUNK'),
    app_commands.Choice(name='Landscape', value='LANDSCAPE'),
    app_commands.Choice(name='Japanese Art', value='JAPANESE_ART'),
    app_commands.Choice(name='Steampunk', value='STEAMPUNK'),
    app_commands.Choice(name='Sketch', value='SKETCH'),
    app_commands.Choice(name='Comic Book', value='COMIC_BOOK'),
    app_commands.Choice(name='Imagine V4 creative', value='V4_CREATIVE'),
    app_commands.Choice(name='Imagine V3', value='IMAGINE_V3'),
    app_commands.Choice(name='Cosmic', value='COMIC_V2'),
    app_commands.Choice(name='Logo', value='LOGO'),
    app_commands.Choice(name='Pixel art', value='PIXEL_ART'),
    app_commands.Choice(name='Interior', value='INTERIOR'),
    app_commands.Choice(name='Mystical', value='MYSTICAL'),
    app_commands.Choice(name='Super realism', value='SURREALISM'),
    app_commands.Choice(name='Minecraft', value='MINECRAFT'),
    app_commands.Choice(name='Dystopian', value='DYSTOPIAN')
])
@app_commands.choices(ratio=[
    app_commands.Choice(name='1x1', value='RATIO_1X1'),
    app_commands.Choice(name='9x16', value='RATIO_9X16'),
    app_commands.Choice(name='16x9', value='RATIO_16X9'),
    app_commands.Choice(name='4x3', value='RATIO_4X3'),
    app_commands.Choice(name='3x2', value='RATIO_3X2')
])
async def imagine(ctx, prompt: str, style: app_commands.Choice[str], ratio: app_commands.Choice[str], negative: str = None):
    temp_message = await ctx.send("https://cdn.discordapp.com/emojis/842555048973172756.gif?size=96&quality=lossless")
    filename = await generate_image(prompt, style.value, ratio.value, negative)
    if negative is not None:
        await ctx.send(content=f"Here is the generated image for {ctx.author.mention} \n- Prompt : `{prompt}`\n- Style : `{style.name}`\n- Ratio :`{ratio.value}` \n- Negative : `{negative}`", file=discord.File(filename))
    else:
        await ctx.send(content=f"Here is the generated image for {ctx.author.mention} \n- Prompt : `{prompt}`\n- Style : `{style.name}`\n- Ratio :`{ratio.value}`", file=discord.File(filename))
    os.remove(filename)
    await temp_message.edit(content=f"{current_language['imagine_msg']}")

@bot.hybrid_command(name="nekos", description=current_language["nekos"])
async def nekos(ctx, category):
    base_url = "https://nekos.best/api/v2/"

    valid_categories = ['husbando', 'kitsune', 'neko', 'waifu',
                        'baka', 'bite', 'blush', 'bored', 'cry', 'cuddle', 'dance',
                        'facepalm', 'feed', 'handhold', 'happy', 'highfive', 'hug',
                        'kick', 'kiss', 'laugh', 'nod', 'nom', 'nope', 'pat', 'poke',
                        'pout', 'punch', 'shoot', 'shrug', 'slap', 'sleep', 'smile',
                        'smug', 'stare', 'think', 'thumbsup', 'tickle', 'wave', 'wink', 'yeet']

    if category not in valid_categories:
        await ctx.send(f"{current_language['nekos_msg']}```{', '.join(valid_categories)}```")
        return

    url = base_url + category

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await ctx.send("Failed to fetch the image.")
                return

            json_data = await response.json()

            results = json_data.get("results")
            if not results:
                await ctx.send("No image found.")
                return

            image_url = results[0].get("url")

            embed = Embed(colour=Colour.blue())
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)

bot.remove_command("help")

@bot.hybrid_command(name="help", description=current_language["help"])
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", color=0x03a1fc)
    embed.set_thumbnail(url=bot.user.avatar.url)
    command_tree = bot.commands
    for command in command_tree:
        if command.hidden:
            continue
        command_description = command.description or "No description available"
        embed.add_field(name=command.name, value=command_description, inline=False)

    embed.set_footer(text=f"{current_language['help_footer']}")

    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")

bot.run(TOKEN)
