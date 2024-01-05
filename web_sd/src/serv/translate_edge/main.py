
from core.threads.DiffusionServerThread import ServerThread
from serv.translate_edge.TranslatorThread import TranslatorThread
from core.system.MultiThreadingApp import MultiThreadingApp


import argparse

 
class TranslatorEdgeServer(MultiThreadingApp):
    def __init__(self):
        MultiThreadingApp.__init__(self)
    
    def run(self):
        print(f"+++ translator app start")
        parser = argparse.ArgumentParser(description="port (eg. 6203)")
        parser.add_argument("port", help="Twoje imię", type=int)
        args = parser.parse_args()
        print(f"+++ app start {args}")

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