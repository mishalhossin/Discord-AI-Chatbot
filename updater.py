import asyncio
import aiohttp
import hashlib
import os
import shutil
import zipfile

GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

async def download_file(session, url, destination):
    async with session.get(url) as response:
        with open(destination, "wb") as f:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)

async def update_repository():
    repo_url = "https://github.com/mishalhossin/Discord-AI-Chatbot/archive/main.zip"
    excluded_files = ["config.yml", "channels.txt", ".env"]

    async with aiohttp.ClientSession() as session:
        async with session.get(repo_url) as response:
            total_size = int(response.headers.get("Content-Length", 0))
            downloaded_size = 0
            block_size = 1024  # 1 KB
            progress_bar = "["

            with open("repository.zip", "wb") as zip_file:
                while True:
                    chunk = await response.content.read(block_size)
                    if not chunk:
                        break
                    downloaded_size += len(chunk)
                    if total_size > 0:
                        progress = int(downloaded_size / total_size * 20)
                    else:
                        progress = 0
                    progress_bar += "#" * progress + "-" * (20 - progress) + "]"
                    print(f"Downloading: {progress_bar}", end="\r")

    print("\nExtracting files...")

    with zipfile.ZipFile("repository.zip", "r") as zip_ref:
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
        return True
    else:
        print("No files have been updated.")
        return False

if __name__ == "__main__":
    asyncio.run(update_repository())
