import openai


def read_cli_input():
    pass

def initialize_gpt():
    instance = None
    return instance


def translate_text(text, gpt_instance):

    translated_text = None
    return translated_text


def main():

    text_to_translate = '''Był sobie kiedyś prezes pewnej firmy zwiazanej z bezpieczeństwem przemysłowym.
      Charakter miał niezby dobry, ale znajomi nazywali go "byczkiem smolnym"'''
    translate_instance = initialize_gpt()
    eng_txt = translate_text(text_to_translate, translate_instance)

    print(f"------------------")
    print(f"tekst po polsku: {text_to_translate}")
    print(f"------------------")
    print(f"tekst po angielsku: {eng_txt}")

    pass

main()