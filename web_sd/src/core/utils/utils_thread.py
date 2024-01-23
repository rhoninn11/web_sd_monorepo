import threading, time, queue, select
from core.utils.utils import *
from core.utils.utils_logging import my_print

class pipe_queue():
    def __init__(self, name):
        self.queue = queue.Queue()
        self.name = name

    def queue_item(self, item):
        self.queue.put(item)

    def dequeue_item(self):
        item = self.queue.get()
        return item

    def queue_len(self):
        return self.queue.qsize()

class ThreadWrap():
    def __init__(self, name="noneame", blocking=False):
        self.name = name.upper()
        self.run_cond = True
        self.in_queue = pipe_queue("input")
        self.out_queue = pipe_queue("output")

        self.blocking = blocking
        self.thread = threading.Thread(target=self.run)

    def is_blocking(self):
        return self.blocking

    def ask_to_stop(self):
        self.run_cond = False

    def start(self):
        print(f"--> {self.name}: thread started")
        # Blocking
        if self.is_blocking():
            self.run()
            return

        # non-blocking
        self.thread.start()

    def join(self):
        # Blocking
        if self.is_blocking():
            return

        # non-blocking
        self.thread.join()

    def run(self):
        print(f"??? {self.name}: run not implemented")

    def stop(self):
        self.ask_to_stop()
        self.join()
        print(f"<-- {self.name}: thread stopped")