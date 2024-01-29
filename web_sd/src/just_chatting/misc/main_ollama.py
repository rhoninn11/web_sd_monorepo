import ollama

from prompt import load_conversation

def main():
    
    conv = []
    conv_to_load = True
    loop = True

    try:
        while loop:
            if conv_to_load:
                conv = load_conversation()
                conv_to_load = False

            stream = ollama.chat(
                model='notus',
                messages=conv,
                stream=True,
            )

            response_tokens = []
            for chunk in stream:
                try:
                    token = chunk['message']['content']
                    response_tokens.append(token)
                    print(token, end='', flush=True)
                except:
                    print(chunk)
                
            
            loop = False

    except KeyboardInterrupt:
        print("Ctrl + C")


main()