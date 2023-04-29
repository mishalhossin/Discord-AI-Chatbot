import os
import phind
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
    result = phind.Completion.create(
        model='gpt-4',
        prompt=prompt,
        results=phind.Search.create(prompt, actualSearch=False),  # create search (set actualSearch to False to disable internet)
        creative=False,
        detailed=False,
        codeContext=''  # up to 3000 chars of code
    )
    return result.completion.choices[0].text


conversation_history = deque(maxlen=3)

@bot.event
async def on_message(message):
    global conversation_history

    if message.author.bot:
        return # ignore messages from bots

    if isinstance(message.channel, discord.DMChannel):
        # Save user message to conversation history
        conversation_history.append(f"{message.author.name}: {message.content}")

        # Combine conversation history with current prompt
        prompt = '\n'.join(conversation_history) + f"\n{bot.user.name}:"
        response = generate_response(prompt)

        # Save bot response to conversation history
        conversation_history.append(f"{bot.user.name}: {response}")

        # Split response into smaller chunks if it's too large
        max_message_length = 1900
        if len(response) > max_message_length:
            response_chunks = []
            current_chunk = ''
            words = response.split(' ')
            for word in words:
                if len(current_chunk) + len(word) < max_message_length:
                    current_chunk += word + ' '
                else:
                    response_chunks.append(current_chunk.strip())
                    current_chunk = word + ' '
            if current_chunk:
                response_chunks.append(current_chunk.strip())
            for chunk in response_chunks:
                await message.reply(chunk)
        else:
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


keep_alive()

bot.run(os.getenv("DISCORD_TOKEN"))
