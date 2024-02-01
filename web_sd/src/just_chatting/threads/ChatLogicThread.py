
from core.utils.utils_thread import ThreadWrap
from core.utils.utils import obj2json2file
from misc.prompt import load_conversation


class ChatLogicThread(ThreadWrap):
    def __init__(self, name="chat_logic", output_file_path = "just_chatting_out.json"):
        ThreadWrap.__init__(self,name)

        self.request_name = "chat"
        self.run_cond == True
        self.conversation = load_conversation()
        self.output_file_path = output_file_path

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

    def handle_response(self, response):
        if response['type'] == "progress":
            progress = response['data']['progress']
            print(progress['token'], end='', flush=True)
            return 0

        if response['type'] == "chat":
            chat = response['data']['chat']
            messeges = chat['messages']
            self.conversation = messeges
            obj2json2file(response, self.output_file_path)
            return 1

        return 0
    
    def ask_user_for_response(self):
        try:
            usr_msg = input("User input:")
            self.conversation.append({"role": "user", "content": usr_msg})
            # print(f"!!! conv {self.conversation}")
        except EOFError:
            pass
    
 
    def run(self):

        chat_req = self.prepare_chat_request()
        self.out_queue.queue_item(chat_req)
        # print(f"Logic request: {chat_req}")

        while self.run_cond == True:
            ready_for_user_msg = 0
            
            if self.in_queue.queue_len() !=0:
                response = self.in_queue.dequeue_item()
                ready_for_user_msg = self.handle_response(response)

            if ready_for_user_msg:
                self.ask_user_for_response()
                chat_req = self.prepare_chat_request()
                obj2json2file(chat_req, self.output_file_path)
                self.out_queue.queue_item(chat_req)



