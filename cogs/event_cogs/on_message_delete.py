from discord.ext import commands
from ..common import replied_messages

class OnMessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.id in replied_messages:
            replied_to_message = replied_messages[message.id]
            await replied_to_message.delete()
            del replied_messages[message.id]

async def setup(bot):
    await bot.add_cog(OnMessageDelete(bot))
