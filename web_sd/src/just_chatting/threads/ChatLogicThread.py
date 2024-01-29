
from core.utils.utils_thread import ThreadWrap

from misc.prompt import load_conversation

class ChatLogicThread(ThreadWrap):
    def __init__(self, name="chat_logic"):
        ThreadWrap.__init__(self,name)

        self.request_name = "chat"

 
    def run(self):
        conv = load_conversation()

        chat = {
            "id": 1,
            "messages": conv
        }

        request = {
            "type": self.name,
            "data": { self.name: chat }
        }

        self.out_queue.queue_item(request)
        print(f"Logic request: {request}")

        
#-----------------------------
        # request = {
        #     "type": "progress",
        #     "data": { "progress": token }
        # }

        # request = {
        #     "type": self.name,
        #     "data": { self.name: chat }
        # }



