import os
import threading
from flask import Flask

def run_flask_app():
    app = Flask("keepalive")

    @app.route('/', methods=['GET', 'POST', 'CONNECT', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'TRACE', 'HEAD'])
    def main():
        return 'Replit: Where code comes to life, dreams take shape, and possibilities are infinite'

    app.run(host='0.0.0.0', port=3000, debug=False, use_reloader=False)

def detect_replit():
    if os.path.isfile("replit.nix") or os.path.isfile(".replit"):
        print("""\033[1;31m ⚠️ Warning: Looks like you are running this project on Replit\033[0m
\033[1;33mPlease note that the .env file cannot exist on Replit.
Instead, create environment variables (e.g., DISCORD_TOKEN and HUGGING_FACE_API) in the "Secrets" tab under "Tools".\033[0m""")
        flask_thread = threading.Thread(target=run_flask_app)
        flask_thread.start()
        return True
    else:
        return False

running_on_replit = detect_replit()
