import requests, time, ast, json
from bs4 import BeautifulSoup
from hashlib import sha256

class Model:
    # answer is returned with html formatting
    next_id = None
    messages = []
    answer = None
    
    def __init__(self):
        r = requests.get("https://italygpt.it")
        soup = BeautifulSoup(r.text, "html.parser")
        self.next_id = soup.find("input", {"name": "next_id"})["value"]

    def GetAnswer(self, prompt: str, messages: list = []):
        r = requests.get("https://italygpt.it/question", params={"hash": sha256(self.next_id.encode()).hexdigest(), "prompt": prompt, "raw_messages": json.dumps(messages)}, stream=True)
        full_answer = ""
        for chunk in r.iter_lines():
            chunk = chunk.decode("utf-8")
            if "ip is banned" in chunk.lower():
                print("Your ip was banned. Support email is: support@ItalyGPT.it")
                break
            
            if "high fraud score" in chunk.lower():
                print("Your ip has a high fraus score. Support email is: support@ItalyGPT.it")
                break

            if "prompt too long" in chunk.lower():
                print("Your prompt is too long (max characters is: 1000)")
                break
                
            if chunk !="":
                full_answer += chunk
                yield chunk

        self.next_id = r.headers["next_id"]
        self.messages = ast.literal_eval(r.headers["raw_messages"])
        self.answer = full_answer