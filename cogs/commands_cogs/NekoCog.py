import discord
from discord.ext import commands
import aiohttp

from ..common import current_language


class NekoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="gif", description=current_language["nekos"])
    @discord.app_commands.choices(category=[
        discord.app_commands.Choice(name=category.capitalize(), value=category)
        for category in ['baka', 'bite', 'blush', 'bored', 'cry', 'cuddle', 'dance', 'facepalm', 'feed', 'handhold', 'happy', 'highfive', 'hug', 'kick', 'kiss', 'laugh', 'nod', 'nom', 'nope', 'pat', 'poke', 'pout', 'punch', 'shoot', 'shrug']
    ])
    async def gif(self, ctx, category: discord.app_commands.Choice[str]):
        base_url = "https://nekos.best/api/v2/"

        url = base_url + category.value

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await ctx.channel.send("Failed to fetch the image.")
                    return

                json_data = await response.json()

                results = json_data.get("results")
                if not results:
                    await ctx.channel.send("No image found.")
                    return

                image_url = results[0].get("url")

                embed = discord.Embed(colour=0x141414)
                embed.set_image(url=image_url)
                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(NekoCog(bot))
