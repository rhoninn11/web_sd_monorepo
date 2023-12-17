from web_sd.src.core.threads.ServerThread import ServerThread
from serv.eeg_brocker.brocker_thread import brocker_logic_thread

from core.system.MultiThreadingApp import MultiThreadingApp
from core.utils.utils_thread import pipe_queue

import argparse

 
class EdgeServer(MultiThreadingApp):
    def __init__(self):
        MultiThreadingApp.__init__(self)
    
    def run(self):
        print(f"+++ app start")
        parser = argparse.ArgumentParser(description="port (eg. 6203)")
        parser.add_argument("send_port", help="sender port", type=int)
        parser.add_argument("recv_port", help="reciver port", type=int)
        args = parser.parse_args()
        print(f"+++ app start {args}")

        data_gen_thread = brocker_logic_thread()

        tcp_thread_to_blender = ServerThread("edge_server")
        tcp_thread_to_blender.bind_worker(data_gen_thread.out_queue, pipe_queue("empty"))
        tcp_thread_to_blender.config_host("localhost", args.send_port)

        tcp_thread_from_eeg = ServerThread("edge_server")
        tcp_thread_from_eeg.bind_worker(pipe_queue("empty"), data_gen_thread.in_queue)
        tcp_thread_from_eeg.config_host("localhost", args.recv_port)

        # gradio thread block main thread - must be last on the list
        threads = [data_gen_thread, tcp_thread_to_blender, tcp_thread_from_eeg]
        self.thread_launch(threads)

        print("+++ edge server exit")

def main():
    edge_server = EdgeServer()
    edge_server.run()

main()