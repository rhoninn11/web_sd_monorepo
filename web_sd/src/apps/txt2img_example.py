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
        self.name = "txt2img"

        self.sample_num = 3
        self.result_count = 0
        self.start_moment = time.perf_counter()

    def bind_wrapper(self, wrapper):
        self.client_wrapper = wrapper
    
    def bind_on_finish(self, callback):
        self.on_finish = callback

    def prepare_command(self):
        sub_command = { self.name: { 
                "metadata": { "id": "from txt2img.py"},
                "config": {
                    "prompt": "John rambo just chilling out in itally",
                    "prompt_negative": "boring skyscape",
                    "seed": 0,
                    "samples": self.sample_num,
                },
            } 
        }

        command = { 
            "type": self.name,
            "data": json.dumps(sub_command)
        }

        return command
    
    def generation_process(self, result):
        if self.process_result(result):
            self.result_count += 1

    def process_result(self, result):
        if result:
            if result["type"] == "progress":
                result = json.loads(result["data"])
                print("Progress: ", result["progress"])
                return False

            if result["type"] == self.name:
                result = json.loads(result["data"])

                metadata = result[self.name]["metadata"]
                print(f"+++ eee yoo {metadata}")

                bulk_data = result[self.name]["bulk"]
                simple_data_img = bulk_data["img"]
                img_file = f"fs/out/{self.name}_{self.result_count}.png"
                pil_img = simple_data2pil(simple_data_img)
                pil_img.save(img_file)
                print(f"+++ Img saved to {img_file}")
                return True

        return False
    
    
    def do_finished(self):
        finished_flag = self.result_count >= self.sample_num
        return finished_flag
    
    def script(self):
        if self.client_wrapper == None:
            return

        command = self.prepare_command()
        self.client_wrapper.send_to_server(command)
        
        while self.run_cond and not self.do_finished():
            result = self.client_wrapper.get_server_info()
            self.generation_process(result)

            time.sleep(0.01)

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