# Gpt4Free-Chat-bot 🤖
This is a [Python](https://www.python.org)-based Discord bot using the `discord.py` library. The bot responds to messages, can change its profile picture, and provide latency information. Additionally, it uses the `theb` library from [GPT4FREE](https://github.com/xtekky/gpt4free) for generating responses based on conversation history.

# Preview 👀

![image](https://user-images.githubusercontent.com/91066601/235470838-cad26039-c843-4497-8ba7-fc88c66dab49.png)

## Features 🥳

- Responds to messages in direct messages only
- Changes its profile picture with the `!pfp` command.
- Provides latency information with the `!ping` command.
- Changes its username with the `!changeusr` command.

# Steps to install and run 🚩 :
### Step 1. 🎬 Git clone repository
```
git clone https://github.com/mishalhossin/Discord-Chatbot-Gpt4Free
```
### Step 2. 📁 Changing directory to cloned directory
```
cd Discord-Chatbot-Gpt4Free
```
### Step 3. 🔑 Getting discord bot token and enabling intents from [here](https://discord.com/developers/applications)

##### Select application
![image](https://user-images.githubusercontent.com/91066601/235554871-a5f98345-4197-4b55-91d7-1aef0d0680f0.png)

##### Enable intents
![image](https://user-images.githubusercontent.com/91066601/235555012-e8427bfe-cffc-4761-bbc0-d1467ca1ff4d.png)

##### Get the token !!!
![image](https://user-images.githubusercontent.com/91066601/235555065-6b51844d-dfbd-4b11-a14b-f65dd6de20d9.png)



### Step 4. 🔐 Create a `.env` file. It will look like this:
```
DISCORD_TOKEN=token_from_step_3
```
![image](https://user-images.githubusercontent.com/91066601/235554576-74e9e1e5-40ed-49d8-b815-dfecf890892d.png)
### Step 5. ⚙️ Install all the dependencies
#### Windows:
```
py pip install -r requirements.txt
```
#### Linux :
```
pip3 install -r requirements.txt
```
### Step 6.🚀 Run the bot
#### Windows
```
py main.py
```
#### Linux
```
python main.py
```

### 🏁 Final step. Invite your bot and DM (Direct message) it | ⚠️ IMPORTANT

![image](https://user-images.githubusercontent.com/91066601/235474066-d805b10b-168b-4965-b623-6b37470ca6bb.png)

# ✨✨✨  Other ways to run ✨✨✨

### Using docker to run 🐳
- Install docker compose on linux machine 

```
apt update -y ; sudo apt upgrade -y; sudo apt autoremove -y; sudo apt install docker-compose -y
```
- Have working bot token
- Follow up-to step 4 
- Start the bot in docker container

```
sudo docker-compose up --build
```
### Using replit to run
- Follow all the steps. This just skips `step 1`

# [![Run on replit](https://img.shields.io/badge/replit-ff245e?style=for-the-badge&logo=replit&logoColor=white)](https://replit.com/@Mishal0legit/Discord-Chatbot-Gpt4Free)
###
###
###### Want something nsfw ? then check this out: [SEX-GPT](https://github.com/mishalhossin/Gpt3-sexbot-discord)
