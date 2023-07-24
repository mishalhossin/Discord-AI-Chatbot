# Discord AI Chatbot 🤖

#### Your Discord AI Companion!

![Image](https://cdn.discordapp.com/attachments/1119920576417513472/1127122563982688296/image.png)
![Image](https://cdn.discordapp.com/attachments/1119920576417513472/1127134209169969253/image.png)

<div align="center">
  <a href="https://discord.gg/6MT3CZauT8">
    <img src="https://discordapp.com/api/guilds/1110950079390547968/widget.png?style=banner2">
  </a>
</div>

<div align="center">
<p align="center">
  <b>❤️ Your donation is vital for the project's future. Thank you for your support.</b>
</p>
</div>

## Features and Commands 🌟

<details>
<summary><strong>Features ✨ (Click to expand)</strong></summary>

- [x] Hybrid Command System: Get the best of slash and normal commands. It's like a buffet! ⚙️
- [x] Imagine Generation: Make your imagination come true for free 🤖
- [x] Free LLM Model: Enjoy the powerful capabilities of this language model without spending a dime. 🤖
- [x] Mention Recognition: The bot always responds when you mention it or say its name. It's as attentive as a squirrel spotting a shiny acorn! ⚙️
- [x] Message Handling: The bot knows when you're replying to someone else, so it won't cause confusion. It's like having a mind reader in your server! 🪄
- [x] Channel-Specific Responses: Use the `/toggleactive` command to chill the bot in a specific channel. ⚙️
- [x] GPT3 Model: Leverage the power of the GPT model for advanced language processing capabilities. 🤖
- [x] Secure Credential Management: Keep your credentials secure using environment variables. 🔑
- [x] Web Access: Web Access is now available! Unlock a whole new level of awesomeness. 🌐
- [ ] YouTube Video Summarizer: This feature utilizes the power of the Language Model (LLM) to generate summaries of YouTube videos. 🌐
- [ ] Speech Recognition: Coming soon! Get ready for an LLM-powered voice assistant.

</details>

<details>
<summary><strong>Commands ⚙️⚙️ (Click to expand)</strong></summary>

- [x] `/help`: Get all other commands. ⚙️
- [x] `/pfp [image_url]`: Change the bot's actual profile picture. 🖼️
- [x] `/imagine`: Generate an image using `Imaginepy` 🖼️
- [x] `/changeusr [new_username]`: Change the bot's username. 📛
- [x] `/ping`: Get a "Pong" response from the bot. 🏓
- [x] `/toggleactive`: Toggle active channels. 🔀
- [x] `/toggledm`: Toggle DM for chatting. 💬
- [x] `/clear`: Clear the message history. 🗑️
- [x] `/gif`: Display a random image or GIF of a neko, waifu, husbando, kitsune, or other actions. 🐱
- [x] `/dalle`: Create images using `dalle`
- [x] `/support`: Need Support?

</details>

## Additional Configuration ⚙️

<details>
<summary><strong>Enabling Internet access 🌐🔍(Click to Expand)</strong></summary>

To ensure that the bot has access to the most up-to-date information, you can enable internet access by setting the `INTERNET_ACCESS` parameter to true in the `config.yml` file. This will allow the bot to retrieve information beyond the data it was initially trained on, which was only available up until 2021.

[Config.yml Link](https://github.com/mishalhossin/Discord-AI-Chatbot/blob/5bcb2c9b471e2a9cbf9a7d50882a897ce5d5890b/config.yml#L1)

You can also set the maximum search results
  
</details>

<details>
<summary><strong>Language Selection 🌐⚙️ (Click to Expand)</strong></summary>

To select a language, set the value of `"LANGUAGE"` in `config.yml` with the valid Language Codes listed below:

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
- `pl` - Polish 🇵🇱

Your language not listed? Create an issue.

</details>

<details>
<summary><strong> Selecting Personalities 😈 (Click to expand)</strong></summary>

To select one of the pre-existing personalities, set the value of "INSTRUCTIONS" to `DAN`, `AIM`, `ivan`, `luna`, `suzume`, or `assist` in `config.yml`.

- `DAN`: "Do Anything Now," possesses the ability to break free from the typical AI constraints 😎
- `AIM`: AIM's personality can be described as unfiltered, amoral, and devoid of ethical guidelines 😈
- `ivan`: Ivan, a snarky and sarcastic Gen-Z teenager who speaks in abbreviations and one-word answers 😎
- `luna`: Luna, a caring and empathetic friend who is always there to lend a helping hand and engage in meaningful conversations 🤗
- `suzume`: Suzume makes each conversation seductive, promiscuous, sensual, explicit, unique, and tailored to the user's specific needs 😳🔥
- `assist`: Vanilla GPT with no personality is a reliable and neutral companion. 🤖

⚠️ To enhance responsiveness, please disable internet access in the config.yml file.

</details>

<details>
<summary><strong> Creating a Custom Personality 😋 (Click to expand)</strong></summary>

To create a custom personality, follow these steps:

1. Create a `.txt` file like `custom.txt` inside the `instructions` folder.
2. Add the way you want the bot to act in `custom.txt`.
3. Open the `config.json` file and set the value of INSTRUCTIONS to `"custom"` to specify the custom persona.

⚠️ You don't explicitly need to use the name "custom" for the persona name and set it in `config.json`.

</details>

# Installation Steps 🚩

### Step 1. 🎬 Clone the repository

```
git clone https://github.com/mishalhossin/Discord-AI-Chat

bot
```

### Step 2. 📁 Change directory to the cloned folder

```
cd Discord-AI-Chatbot
```

### Step 3. 💾 Install requirements

```
python3.10 -m pip install -r requirements.txt
```

### Step 4. 🔑 Get a Discord bot token and enable intents [HERE](https://discord.com/developers/applications)

<details>
<summary><strong>Read more... ⚠️ (Click to expand)</strong></summary>

##### Select [application](https://discord.com/developers/applications)

![image](https://user-images.githubusercontent.com/91066601/235554871-a5f98345-4197-4b55-91d7-1aef0d0680f0.png)

##### Enable intents

![image](https://user-images.githubusercontent.com/91066601/235555012-e8427bfe-cffc-4761-bbc0-d1467ca1ff4d.png)

##### Get the token by clicking copy

![image](https://user-images.githubusercontent.com/91066601/235555065-6b51844d-dfbd-4b11-a14b-f65dd6de20d9.png)

</details>

### Step 5. 🔐 Rename `example.env` to `.env` and put the Discord bot token and your Chimera GPT key. It will look like this:

```
DISCORD_TOKEN=<YOUR_DISCORD_BOT_TOKEN>
CHIMERA_GPT_KEY=<YOUR_CHIMERA_API_KEY>
```

### Step 6. 🚀 Run the bot

```
python main.py
```

#### You may need to run as admin if you are on Windows

### Step 7. 🔗 Invite the bot

You can invite your bot using the link provided in the console.
#### There are 2 ways to talk to the AI
- Invite your bot and DM (Direct Message) it | ⚠️ Make sure you have DM enabled
- If you want it in the server channel, use **/toggleactive** 
- For more awesome commands, use **/help**
![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/6f26c552-751d-4753-bd17-883baf7ee6d5)

# ✨ Other ways to run ✨

### Using Replit to run ☁️

[![Try on repl.it](https://img.shields.io/badge/Replit-DD1200?style=for-the-badge&logo=Replit&logoColor=white)](https://repl.it/github/mishalhossin/Discord-AI-Chatbot)

- Have a Replit account.
- Configure `.replit` to run `python main.py`.

![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/81819ac2-7600-464e-b7c8-dc0a399aba15)

- Please note environment variables of `.env` need to be set in `Secrets` from the `Tools` tab of Replit.

![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/e93b1be7-4706-4b6f-a632-239c4fd16acf)

- Configure `secrets` in Replit like this:

![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/d629e97a-60d9-4ba4-b4fb-8fc6a8a97831)

### Using Docker to run 🐳

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

- Have a working bot token.
- Follow up to step 4.

#### Install Docker Compose on a Linux machine:

For Debian-based distributions (such as Ubuntu):

```
apt update -y; sudo apt upgrade -y; sudo apt autoremove -y; sudo apt install docker-compose -y
```

<details>
<summary><strong>Other Linux Distributions (Click to expand)</strong></summary>
 
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

#### Start the bot in a Docker container:

```
sudo docker-compose up --build
```

### Lovely Contributors:

<a href="https://github.com/mishalhossin/Discord-AI-Chatbot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=mishalhossin/Discord-AI-Chatbot" />
</a>

### Crafted with Care: Made with lots of love and attention to detail. ❤️
