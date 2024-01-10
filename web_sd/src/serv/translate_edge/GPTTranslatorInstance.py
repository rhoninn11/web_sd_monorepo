from openai import OpenAI
import os
import json


class GPTTranlatorInstation:
    def __init__(self, api_key) -> None:
        self.client = OpenAI(api_key=api_key)

    def get_translation_tools(self):
        tools = [
            {
                "type": "function",
                "function":{
                    "name": "validate_translation",
                    "description":  "Funkcja oceni czy dane translacje spełniają jej oczekiwania",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text_pl": {
                                "type": "string",
                                "description": "Tłumaczenie wielkiego tłumacza język na polski",
                            },
                            "text_eng": {
                                "type": "string",
                                "description": "Tłumaczenie wielkiego tłumacza język na angielski",
                            }
                        },
                        "required": ["text_pl", "text_eng"],
                    },
                }
            },
        ]
        return tools
    
    def gpt_run_translation(self, input_text):

        #input_text= read_cli_input()

        messages = [
        {"role": "system", "content": "Jesteś wybinym poliglotą, który włada językami niczym czarodziej żywiołami, twoje translacje zotaną poddane obiektywnej ocenie, postaraj się tłumaczyć tak aby sens tekstu został w pełni zachowany uwazględzniając ukryte konteksty. Ludzie zwą cię wielkim tłumaczem"},
        {"role": "user", "content": f"Tekst do przetłumaczenia: '{input_text}', przekaż tłumaczenia do walidacji" }]
        
        translation_result = {
            "text_pl": "brak",
            "text_eng": "missing",
        }
        response_message = self.client.chat.completions.create(model="gpt-3.5-turbo-0613",
            messages=messages,
            tools=self.get_translation_tools(),
        )

        response_message = response_message.choices[0].message
        print(f"+++ resp: {response_message}")
        if response_message.tool_calls:
            tool_call = response_message.tool_calls[0]
            print(f"+++ call: {tool_call}")
            args = tool_call.function.arguments
            print(f"+++ args: {args}")
            translation_result = json.loads(args)



        print(f"+++ <TO_ZWRACAM> +++ {translation_result}")

        return translation_result

    