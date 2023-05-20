import discord
from discord import app_commands
from discord.ext import commands
import platform
import aiohttp
import os
import time

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# Load api key
try:
    with open("api_key.txt") as f:
        api_key = f.read()
except FileNotFoundError:
    api_key = "0000000000"
    print("No api key selected. Using anonymous account!")


@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="Try /imagine"))
    print(f"{bot.user.name} has connected to Discord!")
    invite_link = discord.utils.oauth_url(
        bot.user.id,
        permissions=discord.Permissions(administrator=True),
        scopes=("bot", "applications.commands")
    )
    print(f"Invite link: {invite_link}")


async def download_image(image_url, save_as):
    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)
    with open(save_as, "wb") as f:
        f.write(response.content)    

@bot.hybrid_command(name="stablegen", description="Write an amazing prompt for Stable Diffusion to generate")
async def imagine(ctx, *, prompt: str):
    sanitized = ""
    forbidden = ['"', "'", "`", "\\", "$"]

    for char in prompt:
        if char in forbidden:
            continue
        else:
            sanitized += char

    # Add ephemeral=True to make it only visible by you
    await ctx.send(f"{ctx.user.mention} is generating \"{sanitized}\"")

    # Generate image
    print(f"Generating {sanitized}")

    current_time = time.time()

    if platform.system() == "Windows":
        os.system(f"python AI-Horde-With-Cli/cli_request.py --prompt '{sanitized}'"
                  f" --api_key '{api_key}' -n 4 -f {current_time}.png")
    else:
        os.system(f"python3 AI-Horde-With-Cli/cli_request.py --prompt '{sanitized}'"
                  f" --api_key '{api_key}' -n 4 -f {current_time}.png")

    # Loop until image generates
    while True:
        if os.path.exists(f"0_{current_time}.png"):
            break
        else:
            continue

    for i in range(4):
        with open(f'{i}_{current_time}.png', 'rb') as file:
            picture = discord.File(file)
            await ctx.send(file=picture)
        os.remove(f"{i}_{current_time}.png")


try:
    with open("bot_token.txt") as f:
        bot_token = f.read()
except FileNotFoundError:
    print("BOT TOKEN NOT FOUND! PUT YOUR BOT TOKEN IN `bot_token.txt`")


    
@bot.hybrid_command(name="polygen", description="Generate image using pollinations")
async def polygen(ctx, *, prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    images = []
    
    for _ in range(4):
        image_url = f'https://image.pollinations.ai/prompt/{encoded_prompt}'
        response = requests.get(image_url)
        
        if response.status_code == 200:
            image_data = response.json()['image']
            
            await download_image(image_data['uuid'], f'{image_data["uuid"]}.png')
                
            images.append(f'{image_data["uuid"]}.png')

    image_files = [discord.File(image) for image in images]
    await ctx.send(files=image_files)
    for image in images:
        os.remove(image)    
    
    
@bot.hybrid_command(name="dallegen", description="Generate image using an endpoint")
async def images(ctx, *, prompt):
    url = "https://imagine.mishal0legit.repl.co"
    json_data = {"prompt": prompt}

    try:
        temp_message = await ctx.send("Generating image avg: 6 seconds")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_data) as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data.get("image_url")
                    if image_url:
                        image_name = f"{prompt}.jpeg"
                        await download_image(image_url, image_name)  # Assuming you have a download_image function defined
                        with open(image_name, 'rb') as file:
                            
                            await ctx.send(
                                f"Prompt by {ctx.author.mention} : `{prompt}\n\n`",
                                file=discord.File(file, filename=f"{image_name}")
                            )
                        await temp_message.edit(content="Finished Image Generation")
                        os.remove(image_name)
                    else:
                        await temp_message.edit(content="An error occurred during image generation.")
                else:
                    await temp_message.edit(content="Your request was rejected as a result of our safety system. Your prompt may contain text that is not allowed by our safety system.")
    except aiohttp.ClientError as e:
        await temp_message.edit(content=f"An error occurred while sending the request: {str(e)}")
    except Exception as e:
        await temp_message.edit(content=f"An error occurred: {str(e)}")
        

bot.run(bot_token)
