import openai
import os
import json
import argparse

script_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.abspath(os.path.join(script_directory, "..", ".."))
input_file_path = os.path.join(project_directory, "fs", "input.json")
output_file_path = os.path.join(project_directory, "fs", "translation.json")


def read_cli_input():
    parser = argparse.ArgumentParser(description="Text to translation")
    parser.add_argument("--text", type=str, help="Type text to translate")
    args = parser.parse_args()

    if args.text:
        text_from_cmd = args.text
    else: 
        text_from_cmd = '''Missing input CLI text'''

    return text_from_cmd

def pars_input_file(in_file_path):
    with open(in_file_path, "r") as json_file:
        parsed_input = json.load(json_file)
    return parsed_input

def gpt_internal_functions():
    functions = [
        {
            "name": "validate_translation",
            "description":  "Funkcja oceni czy dane translacje spełniają jej oczekiwania",
            "parameters": {
                "type": "object",
                "properties": {
                    "text_pl": {
                        "type": "string",
                        "description": "Tłumaczenie wielkiego tłumacza język na polski",
                    },
                    "tekst_eng": {
                        "type": "string",
                        "description": "Tłumaczenie wielkiego tłumacza język na angielski",
                    }
                },
                "required": ["text_pl", "tekst_eng"],
            },
        }
    ]
    return functions


# def gpt_internal_functions():
#     functions = [
#         {
#             "name": "validate_translation",
#             "description":  "Funkcja oceni czy dane translacje spełniają jej oczekiwania",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "text_pl": {
#                         "type": "string",
#                         "description": "Tłumaczenie wielkiego tłumacza język na polski",
#                     },
#                     "tekst_eng": {
#                         "type": "string",
#                         "description": "Tłumaczenie wielkiego tłumacza język na angielski",
#                     },
#                     "tekst_cz": {
#                         "type": "string",
#                         "description": "Tłumaczenie wielkiego tłumacza język na czeski",
#                     }
#                 },
#                 "required": ["text_pl", "tekst_eng", "tekst_cz"],
#             },
#         }
#     ]
#     return functions


def gpt_run_translation(input_text):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    #input_text= read_cli_input()

    messages = [
    {"role": "system", "content": "Jesteś wybinym poliglotą, który włada językami niczym czarodziej żywiołami, twoje translacje zotaną poddane obiektywnej ocenie, postaraj się tłumaczyć tak aby sens tekstu został w pełni zachowany uwazględzniając ukryte konteksty. Ludzie zwą cię wielkim tłumaczem"},
    {"role": "user", "content": f"Tekst do przetłumaczenia: '{input_text}', przekaż tłumaczenia" }]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=gpt_internal_functions(),
        function_call={"name": "validate_translation"},  # "auto" is default, you need to test if this way always call the function
    )
    response_message = response["choices"][0]["message"]

    #print(f"+++++++++{response_message}")
    
    clue_of_response = response_message["function_call"]["arguments"]
    parsed_clue = json.loads(clue_of_response)


    print(f"++<TO_ZWRACAM>++++{parsed_clue}")

    return parsed_clue

def save_translation(input_answer, out_file_path):

    #print(f"CHAT GPT ODPOWIADA:")
    #print(f"{input_answer}")

    input_text = input_answer.get('text_pl', '')
    translate_text = input_answer.get('tekst_eng', '')

    #print(f"po splicie a: {input_text}")
    data = {
        "input_text": input_text, 
        "translation": translate_text
    }

    try:
        with open(out_file_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(data)
 
    with open(out_file_path, "w") as json_file:
          json.dump(existing_data, json_file, indent=4)
    print(f"Translation saved: {out_file_path}")


    pass    

def main():

    print(f"------------------")
    data_to_translate = pars_input_file(input_file_path)
    for record in data_to_translate:
        if "input_text" in record:
            input_text = record["input_text"]
            result = gpt_run_translation(input_text)
            print(f"To będziesz chciał sparsować: {result}")
            save_translation(result, output_file_path)

    pass


main()