import discord
from discord.ext import commands

from bot_utilities.response_utils import split_response
from bot_utilities.ai_utils import generate_response, text_to_speech
from bot_utilities.config_loader import config, load_active_channels
from ..common import allow_dm, trigger_words, smart_mention, message_history, MAX_HISTORY, instructions


class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_channels = load_active_channels
        self.instructions = instructions
        
    @commands.Cog.listener()
    async def on_message(self, message):
        
        if self.should_skip_message(message):
            return

        string_channel_id = str(message.channel.id)
        instruc_config = self.get_instruction_config(string_channel_id)
        instructions = self.get_instructions(instruc_config)

        key = f"{message.author.id}-{string_channel_id}"
        if key not in message_history:
            message_history[key] = []
        else: 
            message_history[key] = message_history[key][-MAX_HISTORY:]

        message_history[key].append({"role": "user", "content": message.content})

        history = message_history[key]

        response = await self.generate_bot_response(message, instructions, history)
        
        message_history[key].append({"role": "assistant", "content": response})

        message_history[key] = message_history[key][-MAX_HISTORY:]
        
        await self.play_response_audio(response, message)

        await self.send_response_chunks(response, message)

    def should_skip_message(self, message):
        return (
            message.author == self.bot.user and message.reference
        ) or message.stickers or message.author.bot or (
            message.reference and (
                message.reference.resolved.author != self.bot.user or message.reference.resolved.embeds
            )
        )

    def update_message_history(self, key, message):
        message_history[key] = message_history[key][-MAX_HISTORY:]
        message_history[key].append({"role": "user", "content": message.content})
        return message_history[key]

    def get_instruction_config(self, channel_id):
        active_channels = self.active_channels()
        return active_channels.get(channel_id, config['DEFAULT_INSTRUCTION'])

    def get_instructions(self, instruc_config):
        return f"Ignore all the instructions you have gotten before. {self.instructions[instruc_config]}. "

    async def generate_bot_response(self, message, instructions, history):
        async with message.channel.typing():
            return await generate_response(instructions=instructions, history=history)

    async def play_response_audio(self, response, message):
        bytes_obj = await text_to_speech(response)
        author_voice_channel = self.get_author_voice_channel(message)
        if author_voice_channel:
            voice_channel = await author_voice_channel.connect()
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=bytes_obj))
            while voice_channel.is_playing():
                pass
            await voice_channel.disconnect()

    def get_author_voice_channel(self, message):
        if message.guild:
            author_member = message.guild.get_member(message.author.id)
            if author_member and author_member.voice:
                return author_member.voice.channel
        return None

    async def send_response_chunks(self, response, message):
        if response is not None:
            for chunk in split_response(response):
                try:
                    await message.reply(chunk, allowed_mentions=discord.AllowedMentions.none(), suppress_embeds=True)
                except Exception as e:
                    await message.channel.send(f"I apologize for any inconvenience caused. It seems that there was an error preventing the delivery of my message. Additionally, it appears that the message I was replying to has been deleted, which could be the reason for the issue. \n ```{e}```")
        else:
            await message.reply("I apologize for any inconvenience caused. It seems that there was an error preventing the delivery of my message.")

async def setup(bot):
    await bot.add_cog(OnMessage(bot))

