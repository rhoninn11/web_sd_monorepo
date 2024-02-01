import os, time
import uuid, json

from core.utils.utils_thread import ThreadWrap
from core.threads.DiffusionClientThread import DiffusionClientThread
from core.system.MultiThreadingApp import MultiThreadingApp
from core.utils.utils import obj2json2file, file2json2obj

from threads.ChatExecutionThread import ChatExecutionThread
from threads.ChatLogicThread import ChatLogicThread

script_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.abspath(os.path.join(script_directory, "..", ".."))
output_file_path = os.path.join(project_directory, "fs", "just_chatting_out.json")

class ChatClient(MultiThreadingApp):
    def __init__(self):
        MultiThreadingApp.__init__(self)


    def run(self):
        print(f"+++ ollama app start")

        logic_thread = ChatLogicThread(name="chat", output_file_path=output_file_path)
        exec_thread = ChatExecutionThread(model="phi")

        logic_thread.out_queue = exec_thread.in_queue
        logic_thread.in_queue = exec_thread.out_queue

        threads = [exec_thread, logic_thread]
        self.thread_launch(threads)
           

def main():
    print("#####################################")

    app = ChatClient()
    app.run()

 
main()