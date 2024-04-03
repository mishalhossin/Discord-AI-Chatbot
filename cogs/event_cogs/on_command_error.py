from discord.ext import commands

from ..common import current_language

class OnError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} You do not have permission to use this command.")
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"{ctx.author.mention} Only the owner of the bot can use this command.")

async def setup(bot):
    await bot.add_cog(OnError(bot))
