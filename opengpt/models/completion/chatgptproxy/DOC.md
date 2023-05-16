# How to Use

To use this model is very simple, first you need to import it:

```py
from opengpt.chatgptproxy.model import Model
```

After importing, we initialize the class to work with it.

```py
chatgptproxy = Model()
```

Now we just run the `GetAnswer` function to get the answer.

```py
print(chatgptproxy.GetAnswer(prompt="What is the meaning of life?"))
```
Note: Conversations are kept by default.

Here is how you could make a simple chatbot with ChatGPTProxy

```py
from opengpt.chatgptproxy.model import Model

chatgptproxy = Model()

while True:
    prompt = input("Your prompt: ")
    print(chatgptproxy.GetAnswer(prompt=prompt))
```
