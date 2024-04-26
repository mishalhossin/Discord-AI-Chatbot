import os
from openai import Client 
from dotenv import load_dotenv
from bot_utilities.config_loader import config

load_dotenv()

client = Client(
    base_url=config['API_BASE_URL'],
    api_key=os.environ.get("API_KEY"),
)
models = client.models.list()
for model in models.data:
    if model.active:
        try:
            response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": "Say this is a test",
                        }
                    ],
                    model=model.id
                )
            print(f"{model.id} responded with : {response.choices[0].message.content}\n\n")
        except Exception:
            print(f'{model.id} failed : {response}\n\n')