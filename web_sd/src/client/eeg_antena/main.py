import argparse

import matplotlib.pyplot as plt
import re

from src.core.system.MultiThreadingApp import MultiThreadingApp
from src.core.threads.ClientThread import ClientThread

from client.eeg_antena.data_thread import eeg_source_thread

class EegClient(MultiThreadingApp):
    def __init__(self):
        MultiThreadingApp.__init__(self)
    
    def run(self):
        print(f"+++ app start")
        parser = argparse.ArgumentParser(description="port (eg. 6203)")
        parser.add_argument("serv_port", help="server port", type=int)
        args = parser.parse_args()
        print(f"+++ app start {args}")


        eeg_client = ClientThread("eeg data client")
        eeg_client.config_host_dst("localhost", args.serv_port)

        eeg_source = eeg_source_thread()
        eeg_source.preview_data()


        # gradio thread block main thread - must be last on the list
        # threads = [data_gen_thread, eeg_client, tcp_thread_from_eeg]
        # self.thread_launch(threads)

        print("+++ edge server exit")


def main():
    edge_server = EegClient()
    edge_server.run()

main()
