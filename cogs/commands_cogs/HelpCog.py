import discord
from discord.ext import commands


from ..common import current_language


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description=current_language["help"])
    async def help(self, ctx):
        embed = discord.Embed(title="Bot Commands", color=0x03a64b)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        command_tree = self.bot.commands
        for command in command_tree:
            if command.hidden:
                continue
            command_description = command.description or "No description available"
            embed.add_field(name=command.name,
                            value=command_description, inline=False)

        embed.set_footer(text=f"{current_language['help_footer']}")
        
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
