from flask import Flask, render_template_string
from threading import Thread

app = Flask(__name__)

@app.route('/')
def main():
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI - ChatBot</title>
        <style>
            body {{
                background-image: url('https://images.unsplash.com/photo-1470115636492-6d2b56f9146d?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=800&ixid=MnwxfDB8MXxyYW5kb218MHx8d2FsbHBhcGVyfHx8fHx8MTY4MjY2OTA1MQ&ixlib=rb-4.0.3&q=80&utm_campaign=api-credit&utm_medium=referral&utm_source=unsplash_source&w=800');
                background-size: cover;
            }}
            .commands-container {{
                border-radius: 25px;
                background-color: rgba(241, 241, 241, 0.8);
                padding: 20px;
                width: 60%;
                margin: 0 auto;
            }}
            .command {{
                animation: typing 2s steps(1000000, end), blink-caret .75s step-end infinite;
                font-family: monospace;
                font-size: 16px;
                color: #000000;
                text-shadow: 0 0 3px #fabb34;
                white-space: nowrap;
                overflow: hidden;
            }}
            @keyframes typing {{
                from {{ width: 0 }}
                to {{ width: 100% }}
            }}
            @keyframes blink-caret {{
                50% {{ border-color: transparent }}
            }}
            h1 {{
                text-align: center;
                color: white;
            }}
            h2 {{
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>Created by Mishal</h1>
        <div class="commands-container">
            <h2>GPT4FREE Chatbot Commands</h2>
            <p class="command">!pfp [image_url] - Change the bot's profile picture</p>
            <p class="command">!changeusr [new_username] - Change the bot's username</p>
            <p class="command">!ping - Pong</p>
            <p class="command">!clear or !bonk - Clear bot's message history</p>
            <p class="command">!toggleactive - Makes the bot active in the channel</p>
            <p class="command">!toggledm - Turn on or off DMs/p>
            <div style="text-align: center; margin-top: 20px;">
                <a href="https://github.com/mishalhossin/Coding-Chatbot-Gpt4Free" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #fabb34; color: #fff; border-radius: 50px;">View Source Code on GitHub</a>
            </div>
        </div>
    </body>
    </html>
    '''

    return render_template_string(html)

def run():
    app.run(host='0.0.0.0', port=3000)

def keep_alive():
    server = Thread(target=run)
    server.start()
