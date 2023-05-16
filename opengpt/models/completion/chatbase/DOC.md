# How to Use

To use this model is very simple, first you need to import it:

```py
from opengpt.chatbase.model import Model
```

After importing, we initialize the class to work with it.

```py
chatbase = Model()
```

Now we just run the `GetAnswer` function to get the answer.

```py
print(chatbase.GetAnswer(prompt="What is the meaning of life?", model="gpt-4"))
```
Note: Available models are gpt-4 and gpt-3.5-turbo. Conversations are kept by default. You will get 2 answers: one from GPT and one from DAN, this is because for this service to work we need to use the DAN prompt which is already added before your prompt.

Here is how you could make a simple chatbot with ChatBase

```py
from opengpt.chatbase.model import Model

chatbase = Model()

while True:
    prompt = input("Your prompt: ")
    print(chatbase.GetAnswer(prompt=prompt, model="gpt-4"))
```
