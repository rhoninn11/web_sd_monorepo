
import socket, time, select
from core.threads.ConnectionThread import ConnectionThread

class ServerThread(ConnectionThread):
    def __init__(self, name):
        ConnectionThread.__init__(self, name)
        self.data_in_q = None
        self.data_out_q = None
        self.host = 'localhost'
        self.port = None

    def bind_worker(self, in_data_stream, out_data_stream):
        self.data_in_q = in_data_stream
        self.data_out_q = out_data_stream

    def config_host(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if self.port is None:
            raise Exception("!!! port not set")
        
        server_address = (self.host, self.port)
        tcp_socket.bind(server_address)
        
        tcp_socket.listen(1)
        print(f"+++ Waiting for connection on port: {self.host}:{self.port}")
        while self.run_cond:
            time.sleep(0.1)
            readable, _w, _e = select.select([tcp_socket], [], [], 1)
            for s in readable:
                connection, client = s.accept()
                try:
                    print(f"+++ new client ({self.name})")
                    self.connection_loop(connection, self.data_in_q, self.data_out_q)
                    print(f"+++ client left ({self.name})")
                finally:
                    connection.close()
                    time.sleep(0.5)
                    print(f"+++ client connection closed?")

        tcp_socket.close()
        time.sleep(0.5)
        print(f"+++ tcp socket closed ?")