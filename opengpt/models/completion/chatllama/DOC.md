# How to Use

To use this model is very simple, first you need to import it:

```py
from opengpt.chatllama.model import Model
```

After importing, we initialize the class to work with it.

```py
chatllama = Model()
```

Now we just run the `GetAnswer` function to get the answer.

```py
print(chatllama.GetAnswer(prompt="What is the meaning of life?"))
```
Note: Conversations are not kept.

Here is how you could make a simple chatbot with ChatGPTProxy

```py
from opengpt.chatllama.model import Model

chatllama = Model()

while True:
    prompt = input("Your prompt: ")
    print(chatllama.GetAnswer(prompt=prompt))
```
