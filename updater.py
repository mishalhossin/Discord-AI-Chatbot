import os
import shutil
import requests
from zipfile import ZipFile
from tqdm import tqdm
import hashlib

GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def update_repository():
    repo_url = "https://github.com/mishalhossin/Discord-AI-Chatbot/archive/main.zip"
    excluded_files = ["config.yml", "channels.txt", ".env"]
    response = requests.get(repo_url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 KB
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

    with open("repository.zip", "wb") as zip_file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            zip_file.write(data)

    progress_bar.close()

    with ZipFile("repository.zip", "r") as zip_ref:
        zip_ref.extractall("temp")

    changed_files = []
    for root, dirs, files in os.walk("temp/Discord-AI-Chatbot-main"):
        for file in files:
            file_path = os.path.join(root, file)

            if file in excluded_files:
                continue

            destination_path = os.path.join(os.getcwd(), file_path.split("Discord-AI-Chatbot-main/", 1)[1])

            current_hash = hashlib.sha256(open(file_path, "rb").read()).hexdigest()

            if os.path.exists(destination_path):
                existing_hash = hashlib.sha256(open(destination_path, "rb").read()).hexdigest()
            else:
                existing_hash = ""

            if current_hash != existing_hash:
                shutil.copyfile(file_path, destination_path)
                changed_files.append(file)

    shutil.rmtree("temp")
    os.remove("repository.zip")

    if changed_files:
        print(GREEN + "The following files have been updated:" + RESET)
        for file in changed_files:
            print(YELLOW + "- " + file + RESET)
    else:
        print("No files have been updated.")
if __name__ == "__main__":
    update_repository()
