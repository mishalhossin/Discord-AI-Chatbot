# Table of Contents
- Defining Values
  - [With Account](#With-created-Account)
  - [Without Account](#Without-Account)
- Using Model
  - [Using ForeFront.AI](#Using-ForeFront.AI)
    - [Conversation System](#Conversation-System)
      - [Conversation](#Conversation)
        - [Creating Chat](#Creating-Chat)
        - [Managing Chats](#Managing-Chats)
        
# How to Use

First you need to import the model and the system to create email, example:

```py
from opengpt.forefront.model import Model
from opengpt.forefront.tools.system.email_creation import Email
```

After importing let's confirm some things. Firstly, if you already have a ForeFront.ai account, you can use it as follows:

## With created Account

### Step 1

Go to the chat with AI page [`/chat`](https://chat.forefront.ai) and then open your terminal and go to the `Applications` tab.

![Applications Tab](https://cdn.discordapp.com/attachments/814722115831595018/1102442650415681546/image.png)
![Cookies Tab](https://cdn.discordapp.com/attachments/814722115831595018/1102442837649412188/image.png)

### Step 2

You will take your Customer Token and keep it.

![Client Token](https://cdn.discordapp.com/attachments/814722115831595018/1102443129140949012/image.png)

### Step 3

Now you will need to get your `session_id`. To do this you will first have to go to the `Network` tab.

![Network Tab](https://cdn.discordapp.com/attachments/814722115831595018/1102443624664399882/image.png)

If nothing appears, just reload the page with this tab open. After that, check the option to only receive requests.

![Fetch/XHR](https://cdn.discordapp.com/attachments/814722115831595018/1102443860568838185/image.png)

### Step 4

Now you will look for the request that you have written in it `touch?_clerk_js_version=4.38.4`

![touch](https://cdn.discordapp.com/attachments/814722115831595018/1102444199414075444/image.png)

Click on any of those I had and it will get your session_id.

![SessionID](https://cdn.discordapp.com/attachments/814722115831595018/1102444640608735262/image.png)

Now you can save these obtained values ​​in variables to use them later.

```py
client = "your_client"
sessionID = "your_session_id"
```

## Without Account

If you don't have an account you can simply use the function that we imported from Email.

```py
email = Email() # Intialize a class
```

Now you will use the `CreateAccount` property.

```py
res = email.CreateAccount()
```

It will take some time to create the account, but after creating it, it will return some values ​​like: `client` and `sessionID`. You can store these values in variables for later use.

```py
client = res.client
sessionID = res.sessionID
```

> **Attention:** You can create several accounts and have several of these values, so you don't need to create an account for each time you use it, just use the data from the other account created.

## Using ForeFront.AI

With the values we got we can use them easily, first we need to initialize and pass some values to the class:

```py
forefront = Model(sessionID=sessionID, client=client, model="gpt-3.5-turbo")
```

If you want to use GPT-4 you can pass the value `gpt-4` in the `model=` field.
Now to configure the conversation you can do the following:

```py
forefront.SetupConversation("Your prompt here.")
```

To get the answer you can do the following:

```py
for r in forefront.SendConversation():
  print(r.choices[0].delta.content, end='')
```

The complete code would look like this:

```py
from opengpt.forefront.model import Model
from opengpt.forefront.tools.system.email_creation import Email

client = "MY_CLIENT"
sessionID = "MY_SESSION"

forefront = Model(sessionID=sessionID, client=client, model="gpt-3.5-turbo")
forefront.SetupConversation("Create a story where the child can get rich in less than 3 days.")

for r in forefront.SendConversation():
  print(r.choices[0].delta.content, end='')
```

### Conversation System

![Future](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRy6dKkIjt1LXljQEYgP3R-g42eLHx4fMIGhg&usqp=CAU)

It's a future of systems, you can talk with AI and his remember what you talk before, that's crazy right? Then, this is implemented and is more easy than you think.



#### Conversation

For start, i will explain something. The conversation system is automatic, on you talk with AI, the memory is located on thr latest chat.

Let's start with existing chats, if you have the ID of a chat already created, you can pass it in 2 ways.

**Way 1 (Using Model class)**

```py
forefront = Model(...., conversationID="id_here")
```



**Way 2 (Dynamic change)**

```py
forefront = Model(....)
forefront.CONVERSATION_ID = "id_here"
```

> You can change the `CONVERSATION_ID` every time you want.

If you pass a nonexistent Id, when it is created it automatically changes to a valid one, this works for both methods.

##### Creating Chat

As you know, it automatically creates a chat if there is no current one, and if there is one it uses this one, so how to create a Chat?

In the `SetupConversation` method that we use to pass the prompt, there is a parameter called `options`, in which you can pass if you want to create a chat in that message. Example:

```py
prompt: str = "example"
user_list: List[str] = ["userid1", "userid2"]
example_id: str = "userid3"

if not example_id in user_list:
  forefront.SetupConversation(prompt=prompt, options={"create": True, "name": example_id + " Chat"})
```

As you can see, this `options` property has two keys:

- **create** -> if a chat is going to be created in this prompt;

- **name** -> the name of the chat that will be created.

##### Managing Chats

So far we're just creating the chats, but we don't know what the information is or the methods to manipulate them. For that reason, I present you the `Conversation` sub-class, which gives you the freedom to carry out these manipulations. You use it like this:

```py
forefront.Conversation.method_here
```

I will list all the methods and how to use them, follow the list:

- **GetList** `()`
  - This method returns all chats that were created.
  ```py
  print(forefront.Conversation.GetList())
  ```

- **Rename** `(id[string], name[string])`
  - This method renames the name of an existing chat, just passing its id and the name you want.
  ```py
  forefront.Conversation.Rename(id="id_here", name="new_name_here")
  ```
 
- **Remove** `(id[string])`
  - This method remove the specify existing chat.
  ```py
  forefront.Conversation.Remove(id="id_here")
  ```
  
- **ClearAll** `()`
  - This method remove all existing chats.
  > Depending on the number of channels this can be a little time consuming.
  ```py
  forefront.Conversation.ClearAll()
  ```
