from flask import Flask, render_template_string
from threading import Thread

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'CONNECT', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'TRACE', 'HEAD'])
def main():
    return 'I\'m alive!'

def run():
    app.run(host='0.0.0.0', port=3000, debug=False, use_reloader=False)

def keep_alive():
    server = Thread(target=run)
    server.start()
