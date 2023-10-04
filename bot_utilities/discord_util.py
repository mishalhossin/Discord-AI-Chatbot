import discord
from discord.ext import commands

intents = discord.Intents.all()

async def check_token(TOKEN):
    try:
        client = commands.Bot(command_prefix="/",
                              intents=intents, heartbeat_timeout=60)
        await client.login(TOKEN)
    except discord.LoginFailure:
        print("\033[31mDiscord Token environment variable is invalid\033[0m")
        return None
    else:
        print("\033[32mDiscord Token environment variable is valid\033[0m")
    finally:
        await client.close()


def get_discord_token():
    print("\033[31mLooks like you haven't properly set up a Discord token environment variable in the `.env` file. (Secrets on replit)\033[0m")
    print("\033[33mNote: If you don't have a Discord token environment variable, you will have to input it every time. \033[0m")
    return input("Please enter your Discord token: ")