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

            for chunk in stream:
                try:
                    print(chunk['message']['content'], end='', flush=True)
                except:
                    print(chunk)
                
            
            loop = False

    except KeyboardInterrupt:
        print("Ctrl + C")


main()