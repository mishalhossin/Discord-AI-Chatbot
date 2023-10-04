import re


def sanitize_username(name):
    name = name.lower()
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    name = name.replace(' ', '')
    name = name[:64]
    return name

def sanitize_prompt(input_string):
    return re.sub(r'[^\w\s]', '', input_string)