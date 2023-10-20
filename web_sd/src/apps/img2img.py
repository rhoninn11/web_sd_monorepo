import time
import numpy
import json
from PIL import Image

from core.utils.utils_thread import ThreadWrap
from core.threads.DiffusionClientThread import DiffusionClientThread
from core.utils.utils import pil2simple_data, simple_data2pil

from core.system.MultiThreadingApp import MultiThreadingApp

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
    def __init__(self, **kwargs):
        ThreadWrap.__init__(self)
        self.client_wrapper = None
        self.on_finish = None
        self.name = "img2img"

    def bind_wrapper(self, wrapper):
        self.client_wrapper = wrapper
    
    def bind_on_finish(self, callback):
        self.on_finish = callback

    def prepare_command(self):
        init_img = Image.open('fs/in/img.png').convert('RGB')

        sub_command = { self.name: {
                "metadata": { "id": "from img2img.py"},
                "config": {
                    "prompt": "Abstract vase with flowers",
                    "prompt_negative": "monochromatic",
                    "power": 0.15,
                    "seed": numpy.random.randint(0, 100),
                },
                "bulk": {
                    "img": pil2simple_data(init_img),
                }
            }
        }

        command = { 
            "type": self.name,
            "data": json.dumps(sub_command)
        }

        return command
    
    def process_result(self, result):
        if result:
            if result["type"] == "progress":
                result = json.loads(result["data"])

                print("Progress: ", result["progress"])
                return False

            if result["type"] == self.name:
                result = json.loads(result["data"])

                simple_data_img = result[self.name]["bulk"]["img"]
                pil_img = simple_data2pil(simple_data_img)
                pil_img.save(f'fs/out/{self.name}.png')
                return True

        return False
    
    def script(self):
        if self.client_wrapper == None:
            return

        command = self.prepare_command()
        self.client_wrapper.send_to_server(command)
        
        loop_cond = lambda r: not self.process_result(r) and self.run_cond

        result = self.client_wrapper.get_server_info()
        while loop_cond(result):
            time.sleep(0.1)
            result = self.client_wrapper.get_server_info()

        print("+++ task finished +++")

    def run(self):
        self.script()
        if self.on_finish:
            self.on_finish()
        
class ExampleClient(MultiThreadingApp):
    def __init__(self):
        MultiThreadingApp.__init__(self)
    
    def run(self):
        client_thread = DiffusionClientThread(name="client-central")
        client_thread.config_host_dst('localhost', 6500)
        logic_thread = ClientLogicThread()

        client_wrapper = ClientWrapper()
        client_wrapper.bind_client_thread(client_thread)
        logic_thread.bind_wrapper(client_wrapper)
        logic_thread.bind_on_finish(self.exit_fn)

        threads = [client_thread, logic_thread]
        self.thread_launch(threads) 

def main():
    app = ExampleClient()
    app.run()

main()


