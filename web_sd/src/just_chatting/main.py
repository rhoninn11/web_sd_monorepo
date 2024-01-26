from model_init import llm_init
from prompt import load_conversation

def main():
    model, tokenizer, streamer, _ = llm_init()

    conv = []
    conv_to_load = True
    try:


        while True:
            if conv_to_load:
                conv = load_conversation()
                conv_to_load = False
                
            prompt_from_tokenizer = tokenizer.apply_chat_template(conv, tokenize=False)
            prompt = prompt_from_tokenizer

            inputs = tokenizer(prompt, return_tensors="pt").to(0)
            outputs = model.generate(**inputs, streamer=streamer, max_new_tokens=2000)
    except KeyboardInterrupt:
        print("Ctrl + C")
    

main()