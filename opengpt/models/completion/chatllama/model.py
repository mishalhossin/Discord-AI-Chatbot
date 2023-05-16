import requests

class Model:
    @staticmethod
    def GetAnswer(prompt: str):
        headers = {
            "Origin": "https://chatllama.baseten.co",
            "Referer": "https://chatllama.baseten.co/",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-length": "17",
            "content-type": "application/json",
            "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.post("https://us-central1-arched-keyword-306918.cloudfunctions.net/run-inference-1", headers=headers, json={"prompt": prompt}).json()
        try:
            return r["completion"]
        except:
            print(f"There was an error. The request response was: {r}")
            return