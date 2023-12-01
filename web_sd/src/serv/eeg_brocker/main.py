from core.threads.DiffusionServerThread import ServerThread
from serv.eeg_brocker.brocker_thread import brocker_logic_thread

from core.system.MultiThreadingApp import MultiThreadingApp

import argparse

 
class EdgeServer(MultiThreadingApp):
    def __init__(self):
        MultiThreadingApp.__init__(self)
    
    def run(self):
        print(f"+++ app start")
        parser = argparse.ArgumentParser(description="port (eg. 6203)")
        parser.add_argument("port", help="Twoje imię", type=int)
        args = parser.parse_args()
        print(f"+++ app start {args}")

        stableD_thread = brocker_logic_thread()
        tcp_thread = ServerThread("edge_server")

        tcp_thread.bind_worker(stableD_thread)
        tcp_thread.config_host("localhost", args.port)

        # gradio thread block main thread - must be last on the list
        threads = [stableD_thread, tcp_thread]
        self.thread_launch(threads)

        print("+++ edge server exit")

def main():
    edge_server = EdgeServer()
    edge_server.run()

main()