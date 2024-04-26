import discord
from discord.ext import commands

import aiohttp
import asyncio
import random
from bot_utilities.ai_utils import poly_image_gen, generate_image_prodia
from prodia.constants import Model
from ..common import blacklisted_words


class AiStuffCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="imagine-pollinations", description="Bring your imagination into reality with pollinations.ai!")
    @discord.app_commands.describe(images="Choose the amount of your image.")
    @discord.app_commands.describe(prompt="Provide a description of your imagination to turn them into image.")
    async def imagine_poly(self, ctx, prompt: str, images: int = 4):
        await ctx.defer(ephemeral=True)
        images = min(images, 18)
        tasks = []
        async with aiohttp.ClientSession() as session:
            while len(tasks) < images:
                task = asyncio.ensure_future(poly_image_gen(session, prompt))
                tasks.append(task)
                
            generated_images = await asyncio.gather(*tasks)
                
        files = []
        for index, image in enumerate(generated_images):
            file = discord.File(image, filename=f"image_{index+1}.png")
            files.append(file)
            
        await ctx.send(files=files, ephemeral=True)

    @commands.guild_only()
    @commands.hybrid_command(name="imagine", description="Command to imagine an image")
    @discord.app_commands.choices(sampler=[
        discord.app_commands.Choice(name='📏 Euler (Recommended)', value='Euler'),
        discord.app_commands.Choice(name='📏 Euler a', value='Euler a'),
        discord.app_commands.Choice(name='📐 Heun', value='Heun'),
        discord.app_commands.Choice(name='💥 DPM++ 2M Karras', value='DPM++ 2M Karras'),
        discord.app_commands.Choice(name='💥 DPM++ SDE Karras', value='DPM++ SDE Karras'),
        discord.app_commands.Choice(name='🔍 DDIM', value='DDIM')
    ])
    @discord.app_commands.choices(model=[
        discord.app_commands.Choice(name='🌈 Elldreth vivid mix (Landscapes, Stylized characters, nsfw)', value='ELLDRETHVIVIDMIX'),
        discord.app_commands.Choice(name='💪 Deliberate v2 (Anything you want, nsfw)', value='DELIBERATE'),
        discord.app_commands.Choice(name='🔮 Dreamshaper (HOLYSHIT this so good)', value='DREAMSHAPER_6'),
        discord.app_commands.Choice(name='🎼 Lyriel', value='LYRIEL_V16'),
        discord.app_commands.Choice(name='💥 Anything diffusion (Good for anime)', value='ANYTHING_V4'),
        discord.app_commands.Choice(name='🌅 Openjourney (Midjourney alternative)', value='OPENJOURNEY'),
        discord.app_commands.Choice(name='🏞️ Realistic (Lifelike pictures)', value='REALISTICVS_V20'),
        discord.app_commands.Choice(name='👨‍🎨 Portrait (For headshots I guess)', value='PORTRAIT'),
        discord.app_commands.Choice(name='🌟 Rev animated (Illustration, Anime)', value='REV_ANIMATED'),
        discord.app_commands.Choice(name='🤖 Analog', value='ANALOG'),
        discord.app_commands.Choice(name='🌌 AbyssOrangeMix', value='ABYSSORANGEMIX'),
        discord.app_commands.Choice(name='🌌 Dreamlike v1', value='DREAMLIKE_V1'),
        discord.app_commands.Choice(name='🌌 Dreamlike v2', value='DREAMLIKE_V2'),
        discord.app_commands.Choice(name='🌌 Dreamshaper 5', value='DREAMSHAPER_5'),
        discord.app_commands.Choice(name='🌌 MechaMix', value='MECHAMIX'),
        discord.app_commands.Choice(name='🌌 MeinaMix', value='MEINAMIX'),
        discord.app_commands.Choice(name='🌌 Stable Diffusion v14', value='SD_V14'),
        discord.app_commands.Choice(name='🌌 Stable Diffusion v15', value='SD_V15'),
        discord.app_commands.Choice(name="🌌 Shonin's Beautiful People", value='SBP'),
        discord.app_commands.Choice(name="🌌 TheAlly's Mix II", value='THEALLYSMIX'),
        discord.app_commands.Choice(name='🌌 Timeless', value='TIMELESS')
    ])
    @discord.app_commands.describe(
        prompt="Write a amazing prompt for a image",
        model="Model to generate image",
        sampler="Sampler for denosing",
        negative="Prompt that specifies what you do not want the model to generate",
    )
    @commands.guild_only()
    async def imagine(self, ctx, prompt: str, model: discord.app_commands.Choice[str], sampler: discord.app_commands.Choice[str], negative: str = None, seed: int = None):
        for word in prompt.split():
            is_nsfw = word in blacklisted_words
        if seed is None:
            seed = random.randint(10000, 99999)
        await ctx.defer()

        model_uid = Model[model.value].value[0]

        if is_nsfw and not ctx.channel.nsfw:
            await ctx.send("⚠️ You can create NSFW images in NSFW channels only\n To create NSFW image first create a age ristricted channel ", delete_after=30)
            return
        imagefileobj = await generate_image_prodia(prompt, model_uid, sampler.value, seed, negative)

        if is_nsfw:
            img_file = discord.File(imagefileobj, filename="image.png", spoiler=True, description=prompt)
            prompt = f"||{prompt}||"
        else:
            img_file = discord.File(imagefileobj, filename="image.png", description=prompt)

        if is_nsfw:
            embed = discord.Embed(color=0xFF0000)
        else:
            embed = discord.Embed(color=discord.Color.random())
        embed.title = f"🎨Generated Image by {ctx.author.display_name}"
        embed.add_field(name='📝 Prompt', value=f'- {prompt}', inline=False)
        if negative is not None:
            embed.add_field(name='📝 Negative Prompt', value=f'- {negative}', inline=False)
        embed.add_field(name='🤖 Model', value=f'- {model.value}', inline=True)
        embed.add_field(name='🧬 Sampler', value=f'- {sampler.value}', inline=True)
        embed.add_field(name='🌱 Seed', value=f'- {seed}', inline=True)

        if is_nsfw:
            embed.add_field(name='🔞 NSFW', value=f'- {str(is_nsfw)}', inline=True)

        await ctx.send(embed=embed, file=img_file)


async def setup(bot):
    await bot.add_cog(AiStuffCog(bot))
