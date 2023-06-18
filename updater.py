import os
import shutil
import requests
from zipfile import ZipFile
from tqdm import tqdm
import hashlib

# ANSI escape codes for colorful output
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# Repository URL
repo_url = "https://github.com/mishalhossin/Discord-AI-Chatbot/archive/main.zip"

# Files to exclude from update
excluded_files = ["config.yml", "channels.txt", ".env"]

# Download the repository zip file
response = requests.get(repo_url, stream=True)
total_size = int(response.headers.get("content-length", 0))
block_size = 1024  # 1 KB
progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

with open("repository.zip", "wb") as zip_file:
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        zip_file.write(data)

progress_bar.close()

# Extract the downloaded zip file
with ZipFile("repository.zip", "r") as zip_ref:
    zip_ref.extractall("temp")

# Iterate over the extracted files
changed_files = []
for root, dirs, files in os.walk("temp/Discord-AI-Chatbot-main"):
    for file in files:
        file_path = os.path.join(root, file)

        # Exclude specific files from updating
        if file in excluded_files:
            continue

        # Determine the destination path for the updated file
        destination_path = os.path.join(os.getcwd(), file_path.split("Discord-AI-Chatbot-main/", 1)[1])

        # Calculate the file hash
        current_hash = hashlib.sha256(open(file_path, "rb").read()).hexdigest()

        # Calculate the hash of the existing file
        if os.path.exists(destination_path):
            existing_hash = hashlib.sha256(open(destination_path, "rb").read()).hexdigest()
        else:
            existing_hash = ""

        # Replace the existing file with the updated file if it has changed
        if current_hash != existing_hash:
            shutil.copyfile(file_path, destination_path)
            changed_files.append(file)

# Clean up the temporary directory and zip file
shutil.rmtree("temp")
os.remove("repository.zip")

# Print the changed files with colorful output
if changed_files:
    print(GREEN + "The following files have been updated:" + RESET)
    for file in changed_files:
        print(YELLOW + "- " + file + RESET)
else:
    print("No files have been updated.")
