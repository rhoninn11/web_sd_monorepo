from src.core.threads.ServerThread import ServerThread
from eeg_middleware_thread import eeg_middleware_thread

from core.system.MultiThreadingApp import MultiThreadingApp
from core.utils.utils_thread import pipe_queue

import argparse


class EegServParams():
    def __init__(self, varbossa=False):
        help_desc = '''
        send_port - for blender (eg. 4444)
        recv_port - for headset (eg. 3333)
        '''
        parser = argparse.ArgumentParser(description=help_desc)
        parser.add_argument("send_port", help="port for data sending server", type=int)
        parser.add_argument("recv_port", help="port for data reciveing server", type=int)
        args = parser.parse_args()

        self.send_port = args.send_port
        self.recv_port = args.recv_port

        if varbossa:
            print(f"+++ server params:{args}")
 
class EdgeServer(MultiThreadingApp):
    def __init__(self):
        MultiThreadingApp.__init__(self)
    
    def run(self):
        print(f"+++ app start")

        params = EegServParams(True)
        data_gen_thread = eeg_middleware_thread()

        tcp_thread_to_blender = ServerThread("edge_server")
        tcp_thread_to_blender.bind_worker(data_gen_thread.out_queue, pipe_queue("empty"))
        tcp_thread_to_blender.config_host("localhost", params.send_port)

        tcp_thread_from_eeg = ServerThread("edge_server")
        tcp_thread_from_eeg.bind_worker(pipe_queue("empty"), data_gen_thread.in_queue)
        tcp_thread_from_eeg.config_host("localhost", params.recv_port)

        threads = [data_gen_thread, tcp_thread_to_blender, tcp_thread_from_eeg]
        self.thread_launch(threads)

        print("+++ edge server exit")

def main():
    edge_server = EdgeServer()
    edge_server.run()

main()