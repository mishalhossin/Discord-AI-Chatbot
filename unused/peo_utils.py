import poe
import random

def generate_gpt4_response(prompt):
    token = random.choice(open('poe_tokens.txt', 'r', encoding='utf-8').read().splitlines())
    client = poe.Client(token.split(':')[0])
    completion = client.send_message('beaver', prompt, with_chat_break=True)
    response = ''.join(token['text_new'] for token in completion)

    return response
