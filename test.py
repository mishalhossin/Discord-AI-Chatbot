from gpt4free import usesless

def generate_response(prompt, message_id=""):
    req = usesless.Completion.create(prompt=prompt, parentMessageId=message_id)
    return req['text'], req['id']

message_history = []

while True:
    prompt = input("Question: ")
    if prompt == "!stop":
        break

    answer, message_id = generate_response(prompt, message_id)
    message_history.append((prompt, answer, message_id))

    print(f"Answer: {answer}")
