
import math
import time
import numpy as np

from core.utils.utils_thread import ThreadWrap

from data_history import data_history

class stat_counter():
    def __init__(self, name="noname_counter"):
        self.name = name
        self.stat_val = 0
        self.messure_timepoint = time.time()
    
    def stat_log(self, prefix):
        now = time.time()
        if now - self.messure_timepoint > 1:
            self.messure_timepoint += 1
            print(f"+++ {prefix}| {self.name}: {self.stat_val}")
            self.stat_val = 0

    def count(self):
        self.stat_val += 1

class eeg_middleware_thread(ThreadWrap):
    def __init__(self, name="eeg_middleware"):
        ThreadWrap.__init__(self, name=name)
        self.fps = 30
        self.frame_time = 1/self.fps
        self.last_frame_timestamp = time.time()

        self.safe_sample_num = 10
        self.buffered_data_flag = False
        self.history = data_history(120)

        self.frames_per_sec = stat_counter(name="frames_per_sec")
        self.elo = 0
    
    def pass_data(self, data):
        if len(self.history) == 0:
            self.history.populate_history(data)

        self.history.store_data_point(data)
        return self.history.get_last_value().tolist()
    
    def control_data_gen(self):
        now = time.time()
        generate_next_data = now - self.last_frame_timestamp > self.frame_time
        self.stream_gating()

        progress = 0
        if generate_next_data:
            self.last_frame_timestamp += self.frame_time
            if self.buffered_data_flag:
                data_point = self.in_queue.dequeue_item()
                self.frames_per_sec.count()

                np_data = np.array(data_point)
                py_data = self.pass_data(np_data)
                self.out_queue.queue_item(py_data)

                progress += 1

        return 1
    
    def stream_gating(self):
        if not self.buffered_data_flag and self.in_queue.queue_len() > self.safe_sample_num:
            self.buffered_data_flag = True
            print(f"+++ {self.name}: eeg buffered")

        if self.buffered_data_flag and self.in_queue.queue_len() == 0:
            self.buffered_data_flag = False
            print(f"+++ {self.name}: eeg buffer drained")

    def run(self):
        print(f"+++ {self.name}: thread ready")
        in_queue = self.in_queue

        while self.run_cond:
            progress = self.control_data_gen()
            self.frames_per_sec.stat_log(prefix=self.name)
            if progress == 0:
                time.sleep(0.00333)