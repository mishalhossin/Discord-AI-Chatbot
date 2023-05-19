import requests
class Model:
    captcha_code = "hadsa"
    def GetAnswer(self, prompt: str, model: str = "gpt-4"):
        if model == "gpt-4":
            chat_id = "quran---tafseer-saadi-pdf-wbgknt7zn"
        elif model == "gpt-3.5-turbo":
            chat_id = "chatbase--1--pdf-p680fxvnm"
        messages = [{"role": "system", "content": ""}, {"role": "user", "content": prompt}]
        r = requests.post("https://www.chatbase.co/api/fe/chat", json={"chatId": chat_id, "captchaCode": self.captcha_code, "messages": messages}).text
        return r
