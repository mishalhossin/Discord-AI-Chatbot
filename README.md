# Discord-Chat-bot 🤖
This is a [Python](https://www.python.org)-based Discord bot using the `discord.py` library. The bot responds to messages, can change its profile picture, and provide latency information. Additionally, it uses the `usesless` model from [OpenGPT](https://github.com/uesleibros/OpenGPT) for generating responses based on conversation history.

## My Discord
  <a href="https://discord.com/users/1025245410224263258">
    <img src="https://lanyard.cnrad.dev/api/1025245410224263258?theme=dark&bg=171515&borderRadius=5px&animated=true&idleMessage=15%20year%20old%20solo%20dev">
  </a>
</p>

# If you want to use `Replit` or `Docker` [check this](https://github.com/mishalhossin/Discord-AI-Chatbot#--other-ways-to-run-)

# Feature showcase 👀
## Imagine generation using DALL-E
![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/0aa3fc13-8023-47fe-b21c-3066d4ecc817)
## OCR for images (Good for text not symbols)
![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/85f4f847-ded5-45fc-ac07-37251edfa627)
## Web access using duckduckgo
![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/33d6eaf7-497b-4cdc-ac19-a18f34743ce5)
## Youtube video summary
![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/554045b8-bbdd-4b4e-82f5-27f852786d2d)




# Features ✨
- [x] Hybrid Command System: Get the best of slash and normal commands. It's like a buffet! ⚙️
- [x] Imagine generation : Make you imagination come true for free 🤖
- [x] Free LLM Model: Enjoy the powerful capabilities of this language model without spending a dime. 🤖
- [x] Mention Recognition: The bot always responds when you mention it or say its name. It's as attentive as a squirrel spotting a shiny acorn! ⚙️
- [x] Message Handling: The bot knows when you're replying to someone else, so it won't cause confusion. It's like having a mind reader in your server! 🪄
- [x] Channel-Specific Responses: Use the `/toggleactive` command to chill the bot in a specific channel. ⚙️
- [x] GPT-3.5-Turbo Model: This bot runs on turbo power! Powered by the lightning-fast GPT-3.5-Turbo language model. 🤖
- [x] Image Detection Model: The bot can detect objects and text in images with a OCR and GPT2 captioning using a fancy Hugging Face API. 🕵️‍♂️
- [x] Secure Credential Management: Keep your credentials secure using environment variables. 🔑
- [x] Crafted with Care: Made with lots of love and attention to detail. ❤️
- [x] Web Access : Web Access is now available! Unlock a whole new level of awesomeness. 🌐
- [x] YouTube Video Summarizer : This is a a feature that utilizes the power of the Language Model (LLM) to generate summaries of YouTube videos. 🌐
- [ ] Speech recognition : Coming soon! Get ready to for a LLM powered voice assistant

## Commands ⚙️⚙️
- [x] `/pfp [image_url]`: Change the bot's actual profile picture.
- [x] `/changeusr [new_username]`: Change the bot's username.
- [x] `/ping`: Get a "Pong" response from the bot.
- [x] `/toggleactive`: Toggle active channels.
- [x] `/toggledm`: Toggle DM for chatting.
- [x] `/bonk`: Clear the message history.
- [x] `/neko`: Display a random image or GIF of a neko, waifu, husbando, kitsune, or other actions.
- [x] `/help`: Get all other commands.
- [x] `/imagine`: Generate image using an endpoint.

# Steps to install and run 🚩 :
### Step 1. 🎬 Git clone repository
```
git clone https://github.com/mishalhossin/Discord-AI-Chatbot
```
### Step 2. 📁 Changing directory to cloned directory
```
cd Discord-AI-Chatbot
```
### Step 3. 🔑 Getting discord bot token and enabling intents from [HERE](https://discord.com/developers/applications)
## [For more info click here](https://github.com/mishalhossin/Discord-Chatbot-Gpt4Free/blob/main/discord_token.md#select-application) ⚠⚠️ IMPORTANT ⚠️⚠

### Step 4. 🔑 Get hugging face Access Tokens from [HEREE](https://huggingface.co/settings/tokens)
## Read or Write it dosent matter (I use Write)
![image](https://user-images.githubusercontent.com/91066601/236681615-71600817-774a-430c-8cec-8e6710a82b49.png)

### Step 5. 🔐 Rename `example.env` to `.env` and put the discord token and hugging face access token. It will look like this:
```
HUGGING_FACE_API=hf_access_token_from_step_4
DISCORD_TOKEN=token_from_step_3
```
### Step 6. ⚙️ Install all the dependencies
```
pip install -r requirements.txt
```
### Step 7. 🚀 Run the bot
```
python main.py
```
### Step 8. Invite the bot
![image](https://user-images.githubusercontent.com/91066601/236673317-64a1789c-f6b1-48d7-ba1b-dbb18e7d802a.png)


### 🏁 Finally talk to the bot
#### There are 2 ways to talk to the ai
- Invite your bot and DM (Direct message) it | ⚠️ Make sure you have DM enabled
- if you want it in server channel use **/toggleactive** 
- For more awesome commands use **/help**

![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/6f26c552-751d-4753-bd17-883baf7ee6d5)


# ✨✨✨  Other ways to run ✨✨✨
### Using replit to run ☁️
# [![Try on repl.it](https://repl-badge.jajoosam.repl.co/try.png)](https://repl.it/github/mishalhossin/Discord-AI-Chatbot)

- Follow all the steps except `step 1`
- Have a replit account
- Please note `.env` found in secrets tab of replit :

![image](https://user-images.githubusercontent.com/91066601/235810871-5d4c1469-35fd-42d2-a3a2-3382002877cb.png)

- Config `secrets` in replit like this :

![image](https://github.com/mishalhossin/Discord-AI-Chatbot/assets/91066601/2898567b-7d8a-422d-93e2-a4b3bec0ff18)


### Using docker to run :whale:
- Have a working bot token
- Follow up-to step 5
#### Install docker compose on linux machine :
```
apt update -y ; sudo apt upgrade -y; sudo apt autoremove -y; sudo apt install docker-compose -y
```
#### Start the bot in docker container :

```
sudo docker-compose up --build
```

###### Want to run as selfbot ? then check this out: [SELF-GPT](https://github.com/mishalhossin/Self-AI-Chatbot)
