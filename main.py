import os
import phind
import aiohttp
import discord
from keep_alive import keep_alive
from discord.ext import commands

# Set up the Discord bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    global current_status
    print(f"{bot.user.name} has connected to Discord!")

def generate_response(prompt):
    result = phind.Completion.create(
        model='gpt-3.5-turbo',
        prompt=prompt,
        results=phind.Search.create(prompt, actualSearch=False),  # create search (set actualSearch to False to disable internet)
        creative=True,
        detailed=False,
        codeContext=''  # up to 3000 chars of code
    )
    return result.completion.choices[0].text

message_history = {}
MAX_HISTORY = 3


@bot.event
async def on_message(message):
    if message.author.bot:
        return # ignore messages from bots

    if isinstance(message.channel, discord.DMChannel):
        author_id = str(message.author.id)
        if author_id not in message_history:
            message_history[author_id] = []

        message_history[author_id].append(message.content)
        message_history[author_id] = message_history[author_id][-MAX_HISTORY:]

        user_prompt = "\n".join(message_history[author_id])
        prompt = f"{user_prompt}\n{message.author.name}: {message.content}\n{bot.user.name}:"
        response = generate_response(prompt)
        # get user object from ID
        user = bot.get_user(int(author_id))
        if user:
            await message.reply(response)
            message_history[author_id].append(f"{bot.user.name}: {response}")
            message_history[author_id] = message_history[author_id][-MAX_HISTORY:]

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
