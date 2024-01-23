
import time

class MultiThreadingApp():
    def __init__(self):
        self.exit = False
        self.thread_list_ref = []

    def exit_fn(self):
        self.exit = True

    def start_threads(self):
        print("+++ starting threads...")
        for t in self.thread_list_ref: 
            t.start()

    def stop_threads(self):
        print("+++ stoping threads...")
        for t in self.thread_list_ref:
            t.stop()

    def bind_threads(self, thread_list: list):
        self.thread_list_ref = thread_list
        blocking_list = []
        for i, t in enumerate(self.thread_list_ref):
            if t.is_blocking():
                blocking_list.append({"i": i, "t": t})

        blc_num = len(blocking_list)
        if blc_num == 0:
            return
        
        if blc_num > 1:
            print(f"!!! CRITICAL: no more then one! | blocking thread num [{blc_num}]")
            return
            
        block = blocking_list[0]
        self.thread_list_ref.pop(block["i"])
        self.thread_list_ref.append(block["t"])

    def blocking(self):
        last_thread = self.thread_list_ref[-1]
        if last_thread.is_blocking() == False:
            try:
                while True and not self.exit:
                    time.sleep(0.1)
            except:
                print("+++ Keyboard interrupt")

    def thread_launch(self, thread_list):
        self.bind_threads(thread_list)
        self.start_threads()
        self.blocking()
        self.stop_threads()

    def ayncio_thread_launch(self, thread_list):
        self.bind_threads(thread_list)
        self.start_threads()

    def ayncio_thread_stop(self):
        self.stop_threads()
        