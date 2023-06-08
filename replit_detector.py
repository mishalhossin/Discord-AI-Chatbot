import threading
from flask import Flask
import os
import sys
import logging

app = Flask("keepalive")

@app.route('/', methods=['GET', 'POST', 'CONNECT', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'TRACE', 'HEAD'])
def main():
    repl_owner = os.environ.get('REPL_OWNER')
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta content="A Python-based Discord chat bot that uses the discord.py library. It can respond to messages using GPT3, It also utilizes the Imaginepy for generating midjourney like images" property="og:description" />
    <meta content="https://replit.com/public/icons/favicon-prompt-192.png" property="og:image" />
    <meta content="#fcba03" data-react-helmet="true" name="theme-color" />
    <link rel="icon" href="https://replit.com/public/icons/favicon-prompt-192.png" type="image/png">
    <title>Discord AI Chatbot</title>
    <style>
        body {{
            background-color: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        
        h1 {{
            --gradient-start: orange;
            --gradient-end: purple;
            color: white;
            font-family: Arial, sans-serif;
            font-size: 4vw;
            text-align: center;
            background: linear-gradient(45deg, var(--gradient-start), var(--gradient-end));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
    </style>
</head>
<body>
    <h1>Hey there, {repl_owner}! Are we going to create a custom persona for the Chatbot, or should we stick with the default, like DAN and others?</h1>
</body>
</html>
'''


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.logger.disabled = True
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

def run_flask_app():
    app.run(host='0.0.0.0', port=3000, debug=False, use_reloader=False)

Welcomer = """\033[1;31m⚠️ Looks like you are running this project on Replit\033[0m
        
\033[1;33mPlease note that the .env file cannot exist on Replit.
Instead, create environment variable DISCORD_TOKEN in the "Secrets" tab under "Tools".\033[0m
"""
            
def detect_replit():
    if "REPL_OWNER" in os.environ:
        return True
    return False

def detect_replit_and_run():
  if detect_replit() is True:
    threading.Thread(target=run_flask_app).start()
    print(Welcomer)
  else:
    return

if __name__ == "__main__":
    detect_replit_and_run()
