import requests
import hashlib
import os
import shutil

def calculate_md5(file_path):
    """Calculate the MD5 hash of a file."""
    with open(file_path, 'rb') as f:
        content = f.read()
        md5_hash = hashlib.md5(content).hexdigest()
    return md5_hash

def download_file(url, destination):
    """Download a file from a URL and save it to the specified destination."""
    response = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(response.content)

def check_main_file_integrity():
    """Check if the local main.py file is the same as the one at the given URL.
    If they are different, replace the local file with the one from the URL."""
    local_main_path = 'main.py'
    temp_download_path = 'temp_main.py'

    # Calculate MD5 hash of local main.py file
    local_main_md5 = calculate_md5(local_main_path)

    # Download main.py from the URL
    download_file("https://raw.githubusercontent.com/mishalhossin/Discord-AI-Chatbot/main/main.py", temp_download_path)

    # Calculate MD5 hash of downloaded main.py file
    downloaded_main_md5 = calculate_md5(temp_download_path)

    if local_main_md5 != downloaded_main_md5:
        shutil.move(temp_download_path, local_main_path)
    else:
        os.remove(temp_download_path)
