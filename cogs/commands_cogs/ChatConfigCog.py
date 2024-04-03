import discord
from discord.ext import commands

from ..common import current_language, instructions, instruc_config, message_history
from bot_utilities.config_loader import load_active_channels
import json

class ChatConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_channels = load_active_channels

    @commands.hybrid_command(name="toggleactive", description=current_language["toggleactive"])
    @discord.app_commands.choices(persona=[
        discord.app_commands.Choice(name=persona.capitalize(), value=persona)
        for persona in instructions
    ])
    @commands.has_permissions(administrator=True)
    async def toggleactive(self, ctx, persona: discord.app_commands.Choice[str] = instructions[instruc_config]):
        channel_id = f"{ctx.channel.id}"
        active_channels = self.active_channels()
        if channel_id in active_channels:
            del active_channels[channel_id]
            with open("channels.json", "w", encoding='utf-8') as f:
                json.dump(active_channels, f, indent=4)
            await ctx.send(f"{ctx.channel.mention} {current_language['toggleactive_msg_1']}", delete_after=3)
        else:
            active_channels[channel_id] = persona.value if persona.value else persona
            with open("channels.json", "w", encoding='utf-8') as f:
                json.dump(active_channels, f, indent=4)
            await ctx.send(f"{ctx.channel.mention} {current_language['toggleactive_msg_2']}", delete_after=3)

    @commands.hybrid_command(name="clear", description=current_language["bonk"])
    async def clear(self, ctx):
        key = f"{ctx.author.id}-{ctx.channel.id}"
        try:
            message_history[key].clear()
        except Exception as e:
            await ctx.send("⚠️ There is no message history to be cleared ", delete_after=2)
            return

        await ctx.send("Message history has been cleared", delete_after=4)

async def setup(bot):
    await bot.add_cog(ChatConfigCog(bot))
