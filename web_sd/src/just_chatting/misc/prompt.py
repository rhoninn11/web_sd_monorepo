import json

def load_conversation():


    json_file = "fs/just_chatting.json"
    conversation = []
    with open(json_file, "r") as f:
        preload = json.load(f)
        for _ , msg in enumerate(preload):
            msg["content"] = "".join(msg["content"])
            conversation.append(msg)
            
    print(conversation)
    return conversation