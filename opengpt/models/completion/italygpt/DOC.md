# How to Use

To use this model is very simple.
To make a ChatBot with ItalyGPT You can:
```py
from opengpt.italygpt.model import Model # first, we import it

italygpt = Model() # here we initialize the model.

while True:
    prompt = input("Your Prompt: ") # here we get your prompt
    for chunk in italygpt.GetAnswer(prompt, italygpt.messages): # here we ask the question to the model
        print(chunk, end='') # here we print the answer
```

Alternatively, you can also do it in that way:

```py
from opengpt.italygpt.model import Model # first, we import it

italygpt = Model() # here we initialize the model.

while True:
    prompt = input("Your Prompt: ") # here we get your prompt
    italygpt.GetAnswer(prompt, italygpt.messages): # here we ask the question to the model
    print(italygpt.answer) # here we print the answer
```