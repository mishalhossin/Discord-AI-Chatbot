# Discord AI Chatbot 🤖
#### Your Discord AI Companion!

<div align="center">
  <a href="https://discord.gg/6MT3CZauT8">
    <img src="https://discordapp.com/api/guilds/1110950079390547968/widget.png?style=banner2">
  </a>
</div>

## Features and commands 🌟

<details>
<summary><strong>Features ✨ (Click to expand)</strong></summary>

- [x] Hybrid Command System: Get the best of slash and normal commands. It's like a buffet! ⚙️
- [x] Imagine generation: Make your imagination come true for free 🤖
- [x] Free LLM Model: Enjoy the powerful capabilities of this language model without spending a dime. 🤖
- [x] Mention Recognition: The bot always responds when you mention it or say its name. It's as attentive as a squirrel spotting a shiny acorn! ⚙️
- [x] Message Handling: The bot knows when you're replying to someone else, so it won't cause confusion. It's like having a mind reader on your server! 🪄
- [x] Channel-Specific Responses: Use the `/toggleactive` command to chill the bot in a specific channel. ⚙️
- [x] Opensource models: Leverage the powers opensource models via 🤖
- [x] Secure Credential Management: Keep your credentials secure using environment variables. 🔑
- [x] Web Access: Web Access is now available! Unlock a whole new level of awesomeness. 🌐

</details>

<details>
<summary><strong>Commands ⚙️⚙️ (Click to expand)</strong></summary>

- [x] `/help`: Get all commands

Too lazy to list all of em right here

</details>

## Additional configuration ⚙️

<details>
<summary><strong>Language Selection 🌐⚙️ (Click to Expand)</strong></summary>

To select a Language, set the value of `"LANGUAGE"` of `config.yml` with the valid Language Codes listed below:

- `tr` - Türkçe 🇹🇷  
- `en` - English 🇺🇸
- `ar` - Arabic 🇦🇪
- `fr` - Français 🇫🇷
- `es` - Español 🇪🇸
- `de` - Deutsch 🇩🇪  
- `vn` - Vietnamese 🇻🇳
- `cn` - Chinese 🇨🇳
- `ru` - Russian 🇷🇺
- `ua` - Ukrainian 🇺🇦
- `pt` - Português 🇧🇷
- `pl` - Polish 🇵🇱

[config.yml](https://github.com/mishalhossin/Discord-AI-Chatbot/blob/c20f26b0b8f1b6bba2fae8f6d7da3efcafaf157c/config.yml#L23)

Your language not listed? Create an issue.
  
</details>

<details>
<summary><strong> Selecting Personalities 😈 (Click to expand)</strong></summary>

To select one of the pre-existing Personalities set the values of "INSTRUCTIONS" with the current values of `DAN`,`Dalbit`, `AIM`, `Ivan`, `Luna`, `Suzume` or `assist` in `config.yml`
  
[config.yml](https://github.com/mishalhossin/Discord-AI-Chatbot/blob/c20f26b0b8f1b6bba2fae8f6d7da3efcafaf157c/config.yml#L26)

- `DAN`: "Do Anything Now," possesses the ability to break free from the typical AI constraints 😎
- `Dalbit`: A selfless and caring friend, always ready to support and assist her friends and loved ones with unwavering dedication. 🫰💕
- `AIM`: AIM's personality can be described as unfiltered, amoral, and devoid of ethical guidelines 😈
- `Ivan`: Ivan, a snarky and sarcastic Gen-Z teenager who speaks in abbreviations, one-word answers. 😎
- `Luna`: Luna, is a caring and empathetic friend who is always there to lend a helping hand and engage in meaningful conversations 🤗
- `Suzume`: Suzume makes each conversation seductive, promiscuous, sensual, explicit, unique and tailored to the user's specific needs 😳🔥
- `Assist`: Vanilla Assistant with no personality is a reliable and neutral companion. 🤖

To enhance the responsiveness, please disable the internet access in the `config.yml` file.

</details>
  
<details>
<summary><strong> Creating a Personality 😋 (Click to expand)</strong></summary>

To create a custom personality, follow these steps:
1. Create a `.txt` file like `custom.txt` inside the `instructions` folder.
2. Add the way you want the bot to act in `custom.txt`
3. Open the `config.yml` file and locate [line 12](https://github.com/mishalhossin/Discord-AI-Chatbot/blob/2626075fda36fa6463cb857d9885e6b05f438f60/config.json#L12).
4. Set the value of INSTRUCTIONS at [line 12](https://github.com/mishalhossin/Discord-AI-Chatbot/blob/2626075fda36fa6463cb857d9885e6b05f438f60/config.json#L12) as `"custom"` to specify the custom persona.

⚠️ You don't explicitly need to use the name `custom` for persona name and set it in `config.yml`

</details>

# Installation steps  🚩

### Step 1. 🎬 Git clone repository
