import os, time
import uuid, json

from core.utils.utils_thread import ThreadWrap
from core.threads.DiffusionClientThread import DiffusionClientThread
from core.system.MultiThreadingApp import MultiThreadingApp
from core.utils.utils import obj2json2file, file2json2obj

from threads.ChatExecutionThread import ChatExecutionThread
from threads.ChatLogicThread import ChatLogicThread

class ChatClient(MultiThreadingApp):
    def __init__(self):
        MultiThreadingApp.__init__(self)


    def run(self):
        print(f"+++ ollama app start")

        logic_thread = ChatLogicThread(name="chat")
        exec_thread = ChatExecutionThread()

        logic_thread.out_queue = exec_thread.in_queue
        logic_thread.in_queue = exec_thread.out_queue

        threads = [exec_thread, logic_thread]
        self.thread_launch(threads)
        
    #     return logic_thread.get_translations()
   

def main():
    print("#####################################")
    app = ChatClient()
    app.run()
    
    #obj2json2file(translations, output_file_path)
 
main()