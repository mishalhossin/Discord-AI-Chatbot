from gpt4free import theb

prefix = "Bot : "

while True:
    input_text = input("User : ")
    
    if input_text.lower() == "exit":
        break
    
    completed_text = ""
    for token in theb.Completion.create(input_text):
        completed_text += token
    print(f"{prefix}{completed_text}")
