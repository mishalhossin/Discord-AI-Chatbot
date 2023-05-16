# How to Use

To use this model is very simple, first you need to import it:

```py
from opengpt.usesless.model import Model
```

After importing, we initialize the class to work with it.

```py
usesless = Model()
```

> **Attention:** If you want to use the `GPT-4` model, just pass the `model=` argument and the model that is `gpt-4` in the parameters.

```py
usesless = Model(model="gpt-4")
```

> To adjust the temperature of the model you can pass the `temperature=` argument and the value from 0 to 1. The higher the creativity increases.

```py
usesless = Model(model="gpt-4", temperature=0.7)
```

Now we define in the `SetupConversation` function what we want to ask.

```py
usesless.SetupConversation("prompt here")
```

Now we just run the `SendConversation` function to get the answer.

```py
for r in usesless.SendConversation():
	print(r.choices[0].delta.content, end='')
```

The complete code would be like this:

```py
from opengpt.usesless.model import Model

usesless = Model(model="gpt-3.5-turbo", temperature=0.7)
usesless.SetupConversation("Create an list with all popular cities of United States.")

for r in usesless.SendConversation():
	print(r.choices[0].delta.content, end='')
```
