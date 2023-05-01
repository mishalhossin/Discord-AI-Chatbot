import os
from gpt4free import theb
import aiohttp
import discord
from collections import deque
from keep_alive import keep_alive
from discord.ext import commands

# Set up the Discord bot
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

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    global conversation_history

    if message.author.bot:
        return # ignore messages from bots

    if isinstance(message.channel, discord.DMChannel):
        # Save user message to conversation history
        conversation_history.append(f"{message.author.name}: {message.content}")

        # Combine conversation history with current prompt
        prompt = '\n'.join(conversation_history) + f"\nLLM:"
        response = generate_response(prompt)

        # Save bot response to conversation history
        conversation_history.append(f"LLM : {response}")

        # Send the complete response
        await message.reply(response)


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


keep_alive()

bot.run(os.getenv("DISCORD_TOKEN"))
