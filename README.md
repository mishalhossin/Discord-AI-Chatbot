# Gpt4Free-Chat-bot 🤖
This is a [Python](https://www.python.org)-based Discord bot using the `discord.py` library. The bot responds to messages, can change its profile picture, and provide latency information. Additionally, it uses the `theb` from [GPT4FREE](https://github.com/xtekky/gpt4free) for generating responses based on conversation history.

# Preview 👀
![image](https://user-images.githubusercontent.com/91066601/235470838-cad26039-c843-4497-8ba7-fc88c66dab49.png)


## Commands ⚙️⚙️

- Toggle active channel for a server by using `!toggleactive` command. ⚠️

![image](https://user-images.githubusercontent.com/91066601/235982560-d7c068d6-d35f-4153-9723-923a8c31546d.png)


- Toggle if dm should be active or not by using `!toggledm` ⚠️

![image](https://user-images.githubusercontent.com/91066601/235982180-d9926bb6-b6f9-44de-a0f7-045fce0dbda1.png)

- Changes its profile picture with the `!pfp [url or attachment]` command.

- Provides latency information with the `!ping` command.

- Changes its username with the `!changeusr [New username]` command.

- If anything gose wrong use `!bonk` to clear history ⚠️

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

##### Get the token !!! by clicking copy
![image](https://user-images.githubusercontent.com/91066601/235555065-6b51844d-dfbd-4b11-a14b-f65dd6de20d9.png)



### Step 4. 🔐 Rename `example.env` to `.env` and put the discord token. It will look like this:
```
DISCORD_TOKEN=token_from_step_3
```
![image](https://user-images.githubusercontent.com/91066601/235554576-74e9e1e5-40ed-49d8-b815-dfecf890892d.png)
### Step 5. ⚙️ Install all the dependencies
#### Windows:
- If you dont have pip already. Run `python get-pip.py` on windows
```
pip install -r requirements.txt
```
#### Linux :
```
pip3 install -r requirements.txt
```
### Step 6. 🚀 Run the bot
#### Windows :
```
py main.py
```
or
```
python main.py
```
#### Linux :
```
python main.py
```
or
```
python3 main.py
```
### Step 7. Invite the bot
![image](https://user-images.githubusercontent.com/91066601/236211332-7ed404aa-6b25-40d9-b3df-516432508043.png)

### 🏁 Finally talk to the bot
#### There are 2 ways to talk to the ai
- Invite your bot and DM (Direct message) it | ⚠️ Make sure you have DM enabled
- **if you want it in server channel use !toggleactive** 
- For more awesome commands use **!welp**

![image](https://user-images.githubusercontent.com/91066601/235474066-d805b10b-168b-4965-b623-6b37470ca6bb.png)

# ✨✨✨  Other ways to run ✨✨✨

### Using docker to run :whale:
- Have a working bot token
- Follow up-to step 4 
#### Install docker compose on linux machine :
```
apt update -y ; sudo apt upgrade -y; sudo apt autoremove -y; sudo apt install docker-compose -y
```
#### Start the bot in docker container :

```
sudo docker-compose up --build
```
### Using replit to run ☁️
- Follow all the steps except `step 1`
- Have a replit account
- Please note `.env` is found in secrets tab of replit :

![image](https://user-images.githubusercontent.com/91066601/235810871-5d4c1469-35fd-42d2-a3a2-3382002877cb.png)

- Config `.env` in replit like this :

![image](https://user-images.githubusercontent.com/91066601/235811115-689c40e8-660a-448d-83dd-194631324436.png)

# [![Try on repl.it](https://repl-badge.jajoosam.repl.co/try.png)](https://repl.it/github/mishalhossin/Discord-Chatbot-Gpt4Free)

###### Want something nsfw ? then check this out: [SEX-GPT](https://github.com/mishalhossin/Gpt3-sexbot-discord)
