import asyncio
from itertools import cycle
import discord
from discord.ext import commands

from bot_utilities.config_loader import config
from ..common import presences_disabled, current_language, presences

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        presences_cycle = cycle(presences + [current_language['help_footer']])
        print(f"{self.bot.user} aka {self.bot.user.name} has connected to Discord!")
        invite_link = discord.utils.oauth_url(
            self.bot.user.id,
            permissions=discord.Permissions(),
            scopes=("bot", "applications.commands")
        )
        print(f"Invite link: {invite_link}")
        if presences_disabled:
            return
        while True:
            presence = next(presences_cycle)
            presence_with_count = presence.replace("{guild_count}", str(len(self.bot.guilds)))
            delay = config['PRESENCES_CHANGE_DELAY']
            await self.bot.change_presence(activity=discord.Game(name=presence_with_count))
            await asyncio.sleep(delay)

async def setup(bot):
    await bot.add_cog(OnReady(bot))
