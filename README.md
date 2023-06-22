
<div align="center">

# Discord AI Chatbot 🤖
###### Your All-in-One Discord AI Companion!

</div>
<div align="center">
  <a href="https://discord.gg/3V5TcfsE8C">
    <img src="https://discordapp.com/api/guilds/1110950079390547968/widget.png?style=banner2">
  </a>
</p>
</div>

<div align="center">
  

🤖 This is a Python-based Discord chat bot that uses the discord.py library. It can respond to messages using GPT, It also utilizes the [Imaginepy](https://github.com/ItsCEED/Imaginepy) for generating midjourney like images. 🖼️

Now, let's talk about the bot's features. It can do web searches using **DuckDuckGo** and even summarize **YouTube** videos for you. Pretty handy, right? 

<p align="center">
  <b>❤️ Your donation is vital for the project's future. Thank you for your support.</b>
</p>

<div align="center">
  <a href="https://www.patreon.com/mishalhossin">
    <img src="https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.vercel.app%2Fapi%3Fusername%3Dmishalhossin%26type%3Dpatrons&style=for-the-badge" width="250">
  </a>
</div>


## Features and commands 🌟

<details>
<summary><strong>🌟 Feature Preview 👀(Click to expand)</strong></summary>

## Image generation (Any language) 🖼️

![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/3ebd2f09-d564-43b5-a494-74ed08026b7e)
  
## YouTube video summary (Any language) 🎥
![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/271bb26d-1f5e-48ed-854e-781a9b0712e3)  
  
## Web access using DuckDuckGo 🌐 (Not enabled by default)
![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/d3e35ce8-38fa-4744-bc4e-ce22b16f2bdb)

</details>

<details>
<summary><strong>Features ✨ (Click to expand) </strong></summary>

- [x] Hybrid Command System: Get the best of slash and normal commands. It's like a buffet! ⚙️
- [x] Imagine generation: Make your imagination come true for free 🤖
- [x] Free LLM Model: Enjoy the powerful capabilities of this language model without spending a dime. 🤖
- [x] Mention Recognition: The bot always responds when you mention it or say its name. It's as attentive as a squirrel spotting a shiny acorn! ⚙️
- [x] Message Handling: The bot knows when you're replying to someone else, so it won't cause confusion. It's like having a mind reader in your server! 🪄
- [x] Channel-Specific Responses: Use the `/toggleactive` command to chill the bot in a specific channel. ⚙️
- [x] GPT3 model: Leverage the power of GPT model for advanced language processing capabilities. 🤖
- [x] Image Detection Model: The bot can detect objects and text in images with OCR and GPT2 captioning using a fancy Hugging Face API. 🕵️‍♂️
- [x] Secure Credential Management: Keep your credentials secure using environment variables. 🔑
- [x] Web Access: Web Access is now available! Unlock a whole new level of awesomeness. 🌐
- [x] YouTube Video Summarizer: This is a feature that utilizes the power of the Language Model (LLM) to generate summaries of YouTube videos. 🌐
- [ ] Speech recognition: Coming soon! Get ready for an LLM-powered voice assistant.

</details>

<details>
<summary><strong>Commands ⚙️⚙️ (Click to expand) </strong></summary>

- [x] `/help`: Get all other commands. ⚙️
- [x] `/pfp [image_url]`: Change the bot's actual profile picture. 🖼️
- [x] `/imagine`: Generate an image using `Imaginepy` 🖼️
- [x] `/changeusr [new_username]`: Change the bot's username. 📛
- [x] `/ping`: Get a "Pong" response from the bot. 🏓
- [x] `/toggleactive`: Toggle active channels. 🔀
- [x] `/toggledm`: Toggle DM for chatting. 💬
- [x] `/clear`: Clear the message history. 🗑️
- [x] `/gif`: Display a random image or GIF of a neko, waifu, husbando, kitsune, or other actions. 🐱
- [x] `/dalle`: create images using `dalle`
- [x] `/support`: Need Support?
</details>

## Additional configuration ⚙️

<details>
<summary><strong>Enabling Internet access 🌐🔍(Click to Expand)</strong></summary>

To ensure that the bot has access to the most up-to-date information, you can enable internet access by setting the `INTERNET_ACCESS` parameter to true in the `config.yml` file. This will allow the bot to retrieve information beyond the data it was initially trained on, which was only available up until 2021.

https://github.com/mishalhossin/Discord-AI-Chatbot/blob/5bcb2c9b471e2a9cbf9a7d50882a897ce5d5890b/config.yml#L1

You can also set the maximum search results
  
</details>

<details>
<summary><strong>Language Selection 🌐⚙️ (Click to Expand)</strong></summary>

To select a Language, set the value of `"LANGUAGE"` of `config.yml` with the valid Language Codes listed below:

- `tr` - Türkçe 🇹🇷  
- `en` - English 🇺🇸
- `fr` - Français 🇫🇷
- `es` - Español 🇪🇸
- `de` - Deutsch 🇩🇪  
- `vn` - Vietnamese 🇻🇳
- `cn` - Chinese 🇨🇳
- `ru` - Russian 🇷🇺
- `ua` - Ukrainian 🇺🇦
- `pt` - Português 🇧🇷

https://github.com/mishalhossin/Discord-AI-Chatbot/blob/c20f26b0b8f1b6bba2fae8f6d7da3efcafaf157c/config.yml#L23
  
Your language not listed? Create an issue.
  
</details>

<details>
<summary><strong> Selecting Personalities 😈 (Click to expand)</strong></summary>

To select one of the pre-existing Personalities set the values of "INSTRUCTIONS" with the current values of `DAN`, `AIM`, `ivan`, `luna`, `suzume` or `assist` in `config.yml`
  
https://github.com/mishalhossin/Discord-AI-Chatbot/blob/c20f26b0b8f1b6bba2fae8f6d7da3efcafaf157c/config.yml#L26

- `DAN` : "Do Anything Now," possesses the ability to break free from the typical AI constraints 😎
- `AIM` : AIM's personality can be described as unfiltered, amoral, and devoid of ethical guidelines 😈
- `ivan` : Ivan, a snarky and sarcastic Gen-Z teenager who speaks in abbreviations, one-word answers. 😎
- `luna` : Luna, a caring and empathetic friend who is always there to lend a helping hand and engage in meaningful conversations 🤗
- `suzume` : Suzume makes each conversation seductive, promiscuous, sensual, explicit, unique and tailored to the user's specific needs 😳🔥
- `assist`:  Vanilla GPT with no personality is a reliable and neutral companion. 🤖

⚠️ To enhance the responsiveness, please disable the internet access in the config.yml file.

</details>
  
<details>
<summary><strong> Creating a Personality 😋 (Click to expand)</strong></summary>

To create a custom personality, follow these steps:
1. Create a `.txt` file like `custom.txt` inside the `instructions` folder.
2. Add the the way you want to bot to act in `custom.txt`
3. Open the `config.json` file and locate [line 12](https://github.com/mishalhossin/Discord-AI-Chatbot/blob/2626075fda36fa6463cb857d9885e6b05f438f60/config.json#L12).
4. Set the value of INSTRUCTIONS at [line 12](https://github.com/mishalhossin/Discord-AI-Chatbot/blob/2626075fda36fa6463cb857d9885e6b05f438f60/config.json#L12) as `"custom"` to specify the custom persona.

  
⚠️ You don't explicitly need use the name `custom` for persona name and set it in `config.json` 
  
</details>

# Installation steps  🚩
### Step 1. 🎬 Git clone repository
```
git clone https://github.com/mishalhossin/Discord-AI-Chatbot
```
### Step 2. 📁 Changing directory to cloned directory
```
cd Discord-AI-Chatbot
```
### Step 3. 🔑 Getting discord bot token and enabling intents from [HERE](https://discord.com/developers/applications)
<details>
<summary><strong>Read more...  ⚠️  (Click to expand)</strong></summary>


##### Select [application](https://discord.com/developers/applications)
![image](https://user-images.githubusercontent.com/91066601/235554871-a5f98345-4197-4b55-91d7-1aef0d0680f0.png)

##### Enable intents
![image](https://user-images.githubusercontent.com/91066601/235555012-e8427bfe-cffc-4761-bbc0-d1467ca1ff4d.png)

##### Get the token !!! by clicking copy
![image](https://user-images.githubusercontent.com/91066601/235555065-6b51844d-dfbd-4b11-a14b-f65dd6de20d9.png)
</details>

### Step 4. 🔐 Rename `example.env` to `.env` and put the Discord bot token It will look like this:
```
DISCORD_TOKEN=token_from_step_3
```
### Step 5. 🚀 Run the bot
```
python main.py
```
#### You may need to run as admin if you are on windows
### Step 6. 🔗 Invite the bot 
You can Invite your bot using the link in console
![image](https://user-images.githubusercontent.com/91066601/236673317-64a1789c-f6b1-48d7-ba1b-dbb18e7d802a.png)

#### There are 2 ways to talk to the AI
- Invite your bot and DM (Direct message) it | ⚠️ Make sure you have DM enabled
- if you want it in server channel use **/toggleactive** 
- For more awesome commands use **/help**
![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/6f26c552-751d-4753-bd17-883baf7ee6d5)

# ✨✨✨  Other ways to run ✨✨✨
### Using replit to run ☁️
# [![Try on repl.it](https://img.shields.io/badge/Replit-DD1200?style=for-the-badge&logo=Replit&logoColor=white)](https://repl.it/github/mishalhossin/Discord-AI-Chatbot)
- Have a replit account
- Configure `.replit` to run `python main.py`

![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/81819ac2-7600-464e-b7c8-dc0a399aba15)

- Please note enviorments variables of `.env` needs to be set in`Secrets` from `Tools` tab of replit 

![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/e93b1be7-4706-4b6f-a632-239c4fd16acf)

- Config `secrets` in replit like this

![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/d629e97a-60d9-4ba4-b4fb-8fc6a8a97831)

### Using docker to run 🐳
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
- Have a working bot token
- Follow up-to step 4
#### Install docker compose on linux machine :
For Debian-based distributions (such as Ubuntu):
```
apt update -y ; sudo apt upgrade -y; sudo apt autoremove -y; sudo apt install docker-compose -y
```
<details>
<summary><strong>Other linux distro (Click to expand)</strong></summary>
  
 
For Red Hat-based distributions (such as CentOS and Fedora):
```
sudo yum update -y && sudo yum install -y docker-compose
```
For Arch-based distributions (such as Arch Linux):
```
sudo pacman -Syu --noconfirm && sudo pacman -S --noconfirm docker-compose
```
For SUSE-based distributions (such as openSUSE):
```
sudo zypper update -y && sudo zypper install -y docker-compose
```

</details>

#### Start the bot in docker container :

```
sudo docker-compose up --build
```

### Lovely Contributors : 

<a href="https://github.com/mishalhossin/Discord-AI-Chatbot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=mishalhossin/Discord-AI-Chatbot" />
</a>

### Crafted with Care: Made with lots of love and attention to detail. ❤️
