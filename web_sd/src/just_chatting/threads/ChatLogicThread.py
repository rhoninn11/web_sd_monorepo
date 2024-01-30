
from core.utils.utils_thread import ThreadWrap

from misc.prompt import load_conversation

class ChatLogicThread(ThreadWrap):
    def __init__(self, name="chat_logic"):
        ThreadWrap.__init__(self,name)

        self.request_name = "chat"
        self.run_cond == True

        self.conversation = load_conversation()

    def ask_user_for_response(self):
        try:
            usr_msg = input("User:")
            self.conversation.append({"role": "user", "content": usr_msg})
            print(f"!!! conv {self.conversation}")
        except EOFError:
            pass

    def handle_response(self, response):
        if response['type'] == "progress":
            progress = response['data']['progress']
            print(progress['token'], end='', flush=True)
            return 0

        if response['type'] == "chat":
            print("!!! Chat")
            chat = response['data']['chat']
            messeges = chat['messages']
            self.conversation = messeges
            return 1

        return 0


        
    def prepare_chat_request(self):
        chat = {
            "id": 1,
            "messages": self.conversation
        }

        request = {
            "type": self.name,
            "data": { self.name: chat }
        }

        return request
 
    def run(self):

        chat_req = self.prepare_chat_request()
        self.out_queue.queue_item(chat_req)
        print(f"Logic request: {chat_req}")

        while self.run_cond == True:
            ready_for_user_msg = 0
            
            if self.in_queue.queue_len() !=0:
                response = self.in_queue.dequeue_item()
                ready_for_user_msg = self.handle_response(response)

            if ready_for_user_msg:
                self.ask_user_for_response()
                chat_req = self.prepare_chat_request()
                self.out_queue.queue_item(chat_req)


        
#-----------------------------
        # request = {
        #     "type": "progress",
        #     "data": { "progress": token }
        # }

        # request = {
        #     "type": self.name,
        #     "data": { self.name: chat }
        # }



