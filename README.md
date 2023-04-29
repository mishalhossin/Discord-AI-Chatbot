# Gpt4Free-Chat-bot
This is a Python-based Discord bot using the `discord.py` library. The bot responds to messages, can change its profile picture, and provide latency information. Additionally, it uses the `phind` library from [GPT4FREE](https://github.com/xtekky/gpt4free) (removed phind 😭) for generating responses based on conversation history.

## Features

- Responds to messages in direct messages.
- Changes its profile picture with the `!pfp` command.
- Provides latency information with the `!ping` command.
- Changes its username with the `!changeusr` command.

# Steps to install and run :
### 1. git clone repository
```
git clone https://github.com/mishalhossin/Gpt4Free-Chat-bot
```
### 2. change directory to cloned directory
```
cd Gpt4Free-Chat-bot
```
### 3. Get discord bot token [here](https://discord.com/developers/applications)
### 4. Get `cf_clearance` cookie from [phind](https://www.phind.com/) by using this [extension](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
![image](https://media.discordapp.net/attachments/1085616784100560966/1101787228696481852/image.png)
### 5. Get useragent by searching `my useragent` or `what is my useragent ?` on [Google](https://google.com)
### 6. Set up .env it will look like this:
```
{
  "DISCORD_TOKEN": "Your discord bot token from step 3",
  "CF_COOKIE": "Your cookie from step 4",
  "USER_AGENT": "Your user agent from step 5"
}
```
### 7. Install all the dependencies
#### Windows:
```
py pip install -r requirements.txt
```
#### Linux :
```
python3 pip install -r requirements.txt
```
### 8.Run the bot
#### Windows
```
py main.py
```
#### Linux
```
python main.py
```
### 9. Invite your bot and DM (Direct message) it
![image](https://user-images.githubusercontent.com/91066601/235293746-60257d85-9a7c-4396-9f42-cea92ab78cf8.png)
