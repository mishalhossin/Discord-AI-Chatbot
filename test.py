from theb import Completion

message_id = ""
while True:
    prompt = input("Question: ")
    if prompt == "!stop":
        break

    req = Completion.create(prompt=prompt, parentMessageId=message_id)

    print(f"Answer: {req['text']}")
    message_id = req["id"]
