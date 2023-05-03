import os
from gpt4free import theb
import aiohttp
import discord
from collections import deque
from keep_alive import keep_alive
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Set up the Discord bot

TOKEN = os.getenv('DISCORD_TOKEN') # Loads Discord bot token from env

# Keep track of the channels where the bot is active

active_channels = set()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

def generate_response(prompt):
    response = ""
    while not response:
        for token in theb.Completion.create(prompt):
            response += token
    return response


conversation_history = deque(maxlen=2)
def bonk():
    conversation_history.clear()
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    global conversation_history

    if message.author.bot:
        return # ignore messages from bots
    if isinstance(message.channel, discord.DMChannel) or message.channel.id in active_channels:
        # Save user message to conversation history
        conversation_history.append(f"{message.author.name}: {message.content}")

        # Combine conversation history with current prompt
        prompt = '\n'.join(conversation_history) + f"\nLLM:"
        response = generate_response(prompt)

        # Save bot response to conversation history
        conversation_history.append(f"LLM : {response}")

        # Send the complete response
        await message.reply(response)
    await bot.process_commands(message)


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

@bot.command()
@commands.has_permissions(administrator=True)
async def addchannel(ctx):
    channel_id = ctx.channel.id
    if channel_id not in active_channels:
        active_channels.add(channel_id)
        with open("channels.txt", "a") as f:
            f.write(str(channel_id) + "\n")
        await ctx.send(f"{ctx.channel.mention} has been added to the list of active channels.")
    else:
        await ctx.send(f"{ctx.channel.mention} is already in the list of active channels.")
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
    
@bot.command()
async def welp(ctx):
    embed = discord.Embed(title="Bot Commands", color=0x00ff00)
    embed.add_field(name="!pfp [image_url]", value="Change the bot's profile picture", inline=False)
    embed.add_field(name="!bonk", value="Clears history of the bot", inline=False)
    embed.add_field(name="!changeusr [new_username]", value="Change the bot's username", inline=False)
    embed.add_field(name="!ping", value="Pong", inline=False)
    embed.add_field(name="!addchannel", value="Add the current channel to the list of active channels", inline=False)   
    embed.set_footer(text="Created by Mishal#1916")
            

keep_alive()

bot.run(TOKEN)
