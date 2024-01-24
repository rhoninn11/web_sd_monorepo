import time
import json
import os

from core.utils.utils_thread import ThreadWrap

from GPTTranslatorInstance import GPTTranlatorInstation


class TranslatorThread(ThreadWrap):
    def __init__(self):
        ThreadWrap.__init__(self)
        self.api_key = os.getenv("OPENAI_API_KEY")

    def process_request(self, request):

        request = json.loads(request)
        request_data = request['data']

        uuid = request_data['pol2ang']['metadata']['id']
        src_lang = request_data['pol2ang']['config']['input_language']
        dst_lang = request_data['pol2ang']['config']['goal_language']
        text  = request_data['pol2ang']['config']['text_to_translate']

        print(f"uuid: {uuid}")
        print(f"src_lang: {src_lang}")
        print(f"dst_lang: {dst_lang}")
        print(f"text: {text}")

        new_goal = {
                'type': 'progress',
                'data': 'translating'
        }
        self.out_queue.queue_item(new_goal)

        translator = GPTTranlatorInstation(self.api_key)
        goal = translator.gpt_run_translation(text)
        print("#######################################")
        print(f">>>>>>>>Translated: {goal}")

        #print(type(goal))
        
                
        new_goal = {
                'type': 'pol2ang',
                'data': { 'pol2ang': {
                            'metadata': { 'id' : uuid},
                            'config' : {
                                 'input_language': 'PL', 
                                 'goal_language': 'ENG', 
                                 'text_to_translate': goal['text_pl'], 
                                 'translated_text': goal['text_eng'] 
        }}}}

        print(f"+++ Full request :")
        print(json.dumps(new_goal, indent=4))
        print("#######################################")

        # Dane z request:
        # {'type': 'pol2ang', 
        #  'data': {'pol2ang': {
        #          'metadata': {'id': '2e7155a2-83fb-4940-9c4e-e41af3c599ba'},
        #          'config': {'input_language': 'PL', 
        #                     'goal_language': 'ENG', 
        #                     'text_to_translate': 'Ale bym zjadĹ‚ ciastko', 
        #                     'translated_text': ''
        # }}}}

       
        self.out_queue.queue_item(new_goal)
        
        return

    def run(self):
        print(f"+++ translator thread ready")
        in_queue = self.in_queue
        while self.run_cond:
            if in_queue.queue_len() == 0:
                time.sleep(0.1)
                continue
            
            new_request = in_queue.dequeue_item()
            self.process_request(new_request)
