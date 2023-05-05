import os
import re
import io
import theb
import aiohttp
import discord
from keep_alive import keep_alive
from discord.ext import commands
from dotenv import load_dotenv
import discord.errors
from wit import Wit
from pydub import AudioSegment

load_dotenv()

# Set up the Discord bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, heartbeat_timeout=20)

TOKEN = os.getenv('DISCORD_TOKEN') # Loads Discord bot token from env
WIT_TOKEN = os.getenv('WIT_TOKEN') # Loads Wit.ai token for speech to text

speech_to_text_client = Wit(WIT_TOKEN)

# Keep track of the channels where the bot should be active

allow_dm = True
active_channels = set()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Coded by Mishal#1916"))
    print(f"{bot.user.name} has connected to Discord!")

def generate_response(prompt):
    response = theb.Completion.create(prompt)
    if not response:
        response = "I couldn't generate a response. Please try again."
    return ''.join(token for token in response)
    

def bonk():
    global message_history
    message_history = {}
    
message_history = {}
MAX_HISTORY = 10


@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    if ctx.valid and ctx.command:
        await bot.process_commands(message)
        return
    
    if message.author.bot:
        author_id = str(bot.user.id)
    else:
        author_id = str(message.author.id)

    if author_id not in message_history:
        message_history[author_id] = []

    message_history[author_id].append(message.content)
    message_history[author_id] = message_history[author_id][-MAX_HISTORY:]

    if message.channel.id in active_channels and not message.author.bot:
        user_history = "\n".join(message_history[author_id])
        prompt = f"{user_history}\n{message.author.name}: {message.content}\n{bot.user.name}:"

        # Send a loading message
        loading_message = await message.channel.send("Loading response...")

        for attachment in message.attachments:
            if attachment.content_type.startswith('audio'):
                file_bytes = io.BytesIO(await attachment.read())
                ogg_audio = AudioSegment.from_file(file_bytes, format="ogg")
                wav_bytes = io.BytesIO()
                ogg_audio.export(wav_bytes, format="wav")
                resp = speech_to_text_client.speech(wav_bytes, {'Content-Type': 'audio/wav'})
                if "text" not in resp.keys():
                    await message.channel.send("Error, try again later!")
                    return
                if resp["text"] == "":
                    await message.channel.send("Unrecognizable audio clip, please try again!")
                    return
                prompt = f"{user_history}\n{message.author.name}: {resp['text']}\n{bot.user.name}:"
                # await message.channel.send(resp["text"]) # The text from speech
                break

        # Display typing animation
        async with message.channel.typing():
            response = generate_response(prompt)

        # Edit the loading message with the generated response
        await loading_message.edit(content=response)



@bot.command()
async def pfp(ctx, attachment_url=None):
    if attachment_url is None and not ctx.message.attachments:
        return await ctx.send(
            "Please provide an image URL or attach an image with the command"
        )

    if attachment_url is None:
        attachment_url = ctx.message.attachments[0].url

    async with aiohttp.ClientSession() as session:
        async with session.get(attachment_url) as response:
            await bot.user.edit(avatar=await response.read())

    await ctx.send("My profile picture has been updated!")

@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000
    await ctx.send(f"Pong! Latency: {latency:.2f} ms")

@bot.command()
async def changeusr(ctx, new_username):
    # Check that the new username is not already taken
    taken_usernames = [user.name.lower() for user in bot.get_all_members()]
    if new_username.lower() in taken_usernames:
        await ctx.send(f"Sorry, the username '{new_username}' is already taken.")
        return
    if new_username == "":
        await ctx.send("Please send the new username as well!")
        return 
    try:
        await bot.user.edit(username=new_username)
    except discord.errors.HTTPException as e:
        await ctx.send("".join(e.text.split(":")[1:]))

@bot.command()
async def toggledm(ctx):
    global allow_dm
    allow_dm = not allow_dm
    await ctx.send(f"DMs are now {'allowed' if allow_dm else 'disallowed'} for active channels.")
    
@bot.command()
@commands.has_permissions(administrator=True)
async def toggleactive(ctx):
    channel_id = ctx.channel.id
    if channel_id in active_channels:
        active_channels.remove(channel_id)
        with open("channels.txt", "w") as f:
            for id in active_channels:
                f.write(str(id) + "\n")
        await ctx.send(
            f"{ctx.channel.mention} has been removed from the list of active channels."
        )
    else:
        active_channels.add(channel_id)
        with open("channels.txt", "a") as f:
            f.write(str(channel_id) + "\n")
        await ctx.send(
            f"{ctx.channel.mention} has been added to the list of active channels.")

# Read the active channels from channels.txt on startup
if os.path.exists("channels.txt"):
    with open("channels.txt", "r") as f:
        for line in f:
            channel_id = int(line.strip())
            active_channels.add(channel_id)
      
@bot.command(name='bonk')
async def _bonk(ctx):
    bonk()
    await ctx.send('Ugh my head hurts')
    
@bot.command(name='clear')
async def _bonk(ctx):
    bonk()
    await ctx.send('Garm? whot huh? what did you just say? baby yoda?')
    
@bot.command()
async def welp(ctx):
    embed = discord.Embed(title="Bot Commands", color=0x00ff00)
    embed.add_field(name="!pfp [image_url]", value="Change the bot's profile picture", inline=False)
    embed.add_field(name="!bonk", value="Clears history of the bot", inline=False)
    embed.add_field(name="!changeusr [new_username]", value="Change the bot's username", inline=False)
    embed.add_field(name="!ping", value="Pong", inline=False)
    embed.add_field(name="!toggleactive", value="Toggle the current channel to the list of active channels", inline=False)   
    embed.add_field(name="!toggledm", value="Toggle if DM should be active or not", inline=False)   
    embed.set_footer(text="Created by Mishal#1916")
    
    await ctx.send(embed=embed)
            
keep_alive()

bot.run(TOKEN)
