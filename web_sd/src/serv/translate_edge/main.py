
from core.threads.DiffusionServerThread import ServerThread
from serv.translate_edge.TranslatorThread import TranslatorThread
from core.system.MultiThreadingApp import MultiThreadingApp


import argparse

 
class TranslatorEdgeServer(MultiThreadingApp):
    def __init__(self):
        MultiThreadingApp.__init__(self)
    
    def run(self):
        print(f"+++ translator app start")
        parser = argparse.ArgumentParser(description="Server for translation service based on GPT")
        parser.add_argument("port", help="port os host server on", type=int) #6203
        args = parser.parse_args()
        print(f"+++ app start with args: {args}")

        translator_tread = TranslatorThread()
        tcp_thread = ServerThread("edge_server")

        tcp_thread.bind_worker(translator_tread)
        tcp_thread.config_host("localhost", args.port)

        # gradio thread block main thread - must be last on the list
        threads = [translator_tread, tcp_thread]
        self.thread_launch(threads)

        print("+++ edge server exit")

def main():
    edge_server = TranslatorEdgeServer()
    edge_server.run()

main()