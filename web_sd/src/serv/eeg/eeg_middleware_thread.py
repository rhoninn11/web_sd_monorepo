
import math
import time

from core.utils.utils_thread import ThreadWrap

from data_history import data_history


class eeg_middleware_thread(ThreadWrap):
    def __init__(self, name="eeg_middleware"):
        ThreadWrap.__init__(self, name=name)
        self.fps = 30
        self.tm_trhld = 1/self.fps
        self.last_data_gen_tp = time.time()

        self.buffered_data_flag = False
        self.history = data_history()

        self.dp_per_sec = 0
        self.dp_mesure_tp = time.time()
    
    def data_gen(self):
        pos_list = []
        scale_list = []
        color_list = []
        samples = 10
        f1 = 1 #Hz
        f2 = f1/1.68
        f3 = f2/1.68
        for i in range(samples):
            tp = i/(samples-1) + self.last_data_gen_tp
            pos_val = (math.sin(2*3.14*f1*tp) + 1) * 0.5
            scale_val = (math.sin(2*3.14*f2*tp) + 1) * 0.5
            color_val = (math.sin(2*3.14*f3*tp) + 1) * 0.5
            pos_list.append(pos_val)
            scale_list.append(scale_val)
            color_list.append(color_val)

        return [pos_list, scale_list, color_list]
    
    def pass_data(self, data):
        if len(self.history) == 0:
            self.history.populate_history(data)

        self.history.store_data_point(data)
        return self.history.get_history_copy()
    
    def control_data_gen(self):
        now = time.time()
        generate_next_data = now - self.last_data_gen_tp > self.tm_trhld
        self.stream_gating()

        progress = 0
        if generate_next_data:
            self.last_data_gen_tp += self.tm_trhld
            if self.buffered_data_flag:
                data_point = self.in_queue.dequeue_item()
                self.dp_per_sec += 1

                # new_data = self.data_gen() # previous method
                new_data = self.pass_data(data_point)
                self.out_queue.queue_item(new_data)

                progress += 1

        return progress
    
    def stream_gating(self):
        if not self.buffered_data_flag and self.in_queue.queue_len() > 10:
            self.buffered_data_flag = True
            print(f"+++ {self.name}: eeg buffered")

        if self.buffered_data_flag and self.in_queue.queue_len() == 0:
            self.buffered_data_flag = False
            print(f"+++ {self.name}: eeg buffer drained")

    def stat_log(self):
        now = time.time()
        if now - self.dp_mesure_tp > 1:
            self.dp_mesure_tp += 1
            print(f"+++ {self.name}: data points per sec: {self.dp_per_sec}")
            self.dp_per_sec = 0

    def run(self):
        print(f"+++ {self.name}: thread ready")
        in_queue = self.in_queue
        while self.run_cond:
            progress = self.control_data_gen()
            self.stat_log()
            if progress == 0:
                time.sleep(0.00333)



