import ollama
from core.utils.utils_thread import ThreadWrap


class ChatExecutionThread(ThreadWrap):

    
    def __init__(self, name="chat_execution"):
        ThreadWrap.__init__(self,name)

        self.request_name = "chat"
        self.model = "notus"
    
    def process_by_ollama(self, conv, put_token_here_fn):
        stream = ollama.chat(
                model=self.model,
                messages=conv,
                stream=True,
            )
        
        message_builder = []
        for chunk in stream:
            try:
                token = chunk['message']['content']
                message_builder.append(token)
                put_token_here_fn(token)
            except:
                pass

        return "".join(message_builder)
    
    def send_token_to_clinet(self, token):


        token_info = {
            "id": 1,
            "token": token
        }

        response = {
            "type": "progress",
            "data": {"progress": token_info}
        }

        self.out_queue.queue_item(response)
        
        print(f"________{response}")

    def process_request(self, data):

        conv = data[self.request_name]["messages"]

        per_token_fn = lambda tok: self.send_token_to_clinet(tok)
        msg = self.process_by_ollama(conv, per_token_fn)

        conv.append({"role": "assistnt", "content": msg})

        print(f"##########{conv}")

    def run(self):

        
        while self.run_cond:
            if self.in_queue.queue_len():
                request = self.in_queue.dequeue_item()

                data = request["data"]
                self.process_request(data)

                self.out_queue.queue_item(request)


                




