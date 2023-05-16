import requests, random, time

chars="abcdefghijklmnopqrstuvwxyz1234567890"

class Model:
    session_id = "".join([random.choice(chars) for i in range(32)])
    user_fake_id = "".join([random.choice(chars) for i in range(16)])
    chat_id = "0"

    def GetAnswer(self, prompt: str):
        r = requests.post("https://chatgptproxy.me/api/v1/chat/conversation", json={"data": {"parent_id": self.chat_id, "session_id": self.session_id, "question": prompt, "user_fake_id": self.user_fake_id}}).json()
        if r["code"] == 200 and r["code_msg"] == "Success":
            self.chat_id = r["resp_data"]["chat_id"]
            r = requests.post("https://chatgptproxy.me/api/v1/chat/result", json={"data": {"chat_id": self.chat_id, "session_id": self.session_id, "user_fake_id": self.user_fake_id}}).json()
            if r["code"] == 200 and r["code_msg"] == "Success":
                if r["resp_data"]["answer"] != "":
                    return r["resp_data"]["answer"]
                r = requests.post("https://chatgptproxy.me/api/v1/chat/result", json={"data": {"chat_id": self.chat_id, "session_id": self.session_id, "user_fake_id": self.user_fake_id}}).json()
                if r["code"] == 200 and r["code_msg"] == "Success":
                    return r["resp_data"]["answer"]
            else:
                if "operation too frequent" in r["code_msg"].lower():
                    print("Operation too frequent for result. Waiting 10 seconds...")
                    time.sleep(10)
                    return self.GetAnswer(prompt)
                print(f"There was an error with your request for result. The response was: {r}")
                return
        else:
            if "operation too frequent" in r["code_msg"].lower():
                print("Operation too frequent for question. Waiting 10 seconds...")
                time.sleep(10)
                return self.GetAnswer(prompt)
            elif "Your question has been received" in r["code_msg"]:
                print("Session id or user fake id probably already in use. Generating new ones...")
                self.session_id = "".join([random.choice(chars) for i in range(32)])
                self.user_fake_id = "".join([random.choice(chars) for i in range(16)])
                return self.GetAnswer(prompt)
            print(f"There was an error with your request for question. The response was: {r}")
            return