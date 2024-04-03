from g4f.client import Client
from g4f.Provider import RetryProvider, FlowGpt, ChatgptAi, Liaobots

client = Client(
    provider=RetryProvider([FlowGpt, ChatgptAi, Liaobots]),
)
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say this is a test"}],
    )
    print(response.choices[0].message.content)
    print('gpt-3.5-turbo worked fine')
except:
    print('gpt-3.5-turbo failed')
try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Say this is a test"}],
    )
    print(response.choices[0].message.content)
    print('gpt-4 worked fine')
except:
    print('gpt-4 failed')