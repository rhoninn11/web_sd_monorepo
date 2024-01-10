import time
import json
import uuid
import os

from core.utils.utils_thread import ThreadWrap
from core.threads.DiffusionClientThread import DiffusionClientThread

from core.system.MultiThreadingApp import MultiThreadingApp

script_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.abspath(os.path.join(script_directory, "..", ".."))
input_file_path = os.path.join(project_directory, "fs", "input.json")


def pars_input_file(in_file_path):
    with open(in_file_path, "r") as json_file:
        parsed_input = json.load(json_file)
    return parsed_input

class ClientWrapper():
    def __init__(self, **kwargs):
        self.client_thread = None
        self.server_stats = None

    def bind_client_thread(self, thread):
        self.client_thread = thread

    def send_to_server(self, command):
        if self.client_thread:
            in_queue = self.client_thread.in_queue
            in_queue.queue_item(command)
    
    def get_server_info(self):
        if self.client_thread:
            out_queue = self.client_thread.out_queue
            if out_queue.queue_len() == 0:
                return {}
            
            return out_queue.dequeue_item()
        return {}

class ClientLogicThread(ThreadWrap):

    def __init__(self, text_to_translate, **kwargs):
        ThreadWrap.__init__(self)
        self.client_wrapper = None
        self.on_finish = None
        self.name = "pol2ang"

        self.sample_num = 1
        self.result_count = 0
        self.start_moment = None

        self.text_to_translate = text_to_translate

    def bind_wrapper(self, wrapper):
        self.client_wrapper = wrapper
    
    def bind_on_finish(self, callback):
        self.on_finish = callback

    def prepare_command(self):

        command = json.dumps({ 
            "type": self.name,
            "data": { self.name: { 
                "metadata": { "id": f"{uuid.uuid4()}"}, #"from pol2ang.py"
                "config": {
                    "input_language": "PL",
                    "goal_language": "ENG",
                    "text_to_translate": self.text_to_translate,
                    "translated_text": ""
                    },
                } 
            }
        })
        return command
    
    def process_result(self, result):
        if result:
            if result["type"] == "progress":
                if self.start_moment == None:
                    self.start_moment = time.perf_counter()
                
                return False

            if result["type"] == self.name:

                real_time = time.perf_counter() - self.start_moment
                translation = result["data"]["pol2ang"]["config"]["translated_text"]
                print(f"+++++++++++++++++++ eee yoo: \n{translation} \ntime: {real_time} \n+++++++++++++++++++\n")

                return True

        return False
    def loop_cond(self, result):
        if self.process_result(result):
            self.result_count += 1

        finished = self.result_count >= self.sample_num
        return not finished and self.run_cond
    
    def script(self):
        if self.client_wrapper == None:
            return

        command = self.prepare_command()
        self.client_wrapper.send_to_server(command)
        
        result = None
        while self.loop_cond(result):
            result = self.client_wrapper.get_server_info()
            time.sleep(0.01)

        print("+++ task finished +++")

    def run(self):
        self.script()
        if self.on_finish:
            self.on_finish()
        
class ExampleClient(MultiThreadingApp):
    def __init__(self, text):
        MultiThreadingApp.__init__(self)
        self.text = text

    def run(self):
        client_thread = DiffusionClientThread(name="translate-client-central")  #powinien się nazywać just ClientThread
        client_thread.config_host_dst('localhost', 6203)              #communication port
        logic_thread = ClientLogicThread(text_to_translate=self.text)                            

        client_wrapper = ClientWrapper()                              #podłącza wątek, wysyła na serwer, zbiera info z serwera
        client_wrapper.bind_client_thread(client_thread)
        logic_thread.bind_wrapper(client_wrapper)
        logic_thread.bind_on_finish(self.exit_fn)

        threads = [client_thread, logic_thread]
        self.thread_launch(threads) 

def main():
    print("#####################################")
    data_to_translate = pars_input_file(input_file_path)
    print("#####################################")
    for it in data_to_translate:
        app = ExampleClient(text = it['input_text'])
        app.run() 
    print("#########THATS_ALL_-_GOODBYE############")
main()



