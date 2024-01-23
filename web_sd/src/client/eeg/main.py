import argparse
import re

from misc.eeg import load_eeg_data
from eeg_source_thread import eeg_source_thread


from src.core.system.MultiThreadingApp import MultiThreadingApp
from src.core.threads.ClientThread import ClientThread
from src.core.utils.utils_thread import pipe_queue


class EegClient(MultiThreadingApp):
    def __init__(self):
        MultiThreadingApp.__init__(self)
    
    def run(self, eeg_data):
        print(f"+++ app start")
        parser = argparse.ArgumentParser(description="Eeg client that sends eeg data from file")
        parser.add_argument("serv_port", help="server port to connect to", type=int)
        args = parser.parse_args()
        print(f"+++ app start {args}")

        eeg_client = ClientThread("eeg_sender")
        eeg_client.config_host_dst("localhost", args.serv_port)

        eeg_source = eeg_source_thread("eeg_data_source")
        eeg_source.attach_data_to_stream(eeg_data)
        eeg_source.bind_worker(pipe_queue("empty"), eeg_client.in_queue)

        threads = [eeg_client, eeg_source]

        self.thread_launch(threads)

        print("+++ edge server exit")


def main():
    eeg_data = load_eeg_data()
    edge_server = EegClient()
    edge_server.run(eeg_data)

main()
