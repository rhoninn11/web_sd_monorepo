
import time, re
from src.core.utils.utils_thread import ThreadWrap

class eeg_source_thread(ThreadWrap):
    def __init__(self, name="eeg_data_source"):
        ThreadWrap.__init__(self, name)
        self.last_data_gen_tp = time.time()
        fps = 30
        self.ttreshold = 1/fps
        self.stream_flag = False
        
        self.eeg_data = None
        self.data_len = 0
        self.data_idx = 0

        self.queue_data_out = None
        self.queue_data_in = None

        self.data_points_per_sec = 0
        self.data_points_per_sec_tp = time.time()

    def bind_worker(self, in_data_stream, out_data_stream):
        self.queue_data_in = in_data_stream
        self.queue_data_out = out_data_stream

    def read_data_point(self):
        data_point = []
        for f_range in self.eeg_data[0:3]:
            name = f_range["name"]
            plot = f_range["plot"]
            data_point.append(plot[self.data_idx])

        self.data_idx += 1
        if self.data_idx >= self.data_len:
            print(f"+++ {self.name}: data looped")
            self.data_idx = 0

        return data_point

    def control_data_streaming(self):
        now = time.time()
        generate_next_data = now - self.last_data_gen_tp > self.ttreshold
        progress = 0
        if generate_next_data and self.eeg_data:
            self.last_data_gen_tp += self.ttreshold

            self.data_points_per_sec += 1
            self.queue_data_out.queue_item(self.read_data_point())
            progress += 1

        return progress
    
    def attach_data_to_stream(self, data):
        self.eeg_data = data
        self.data_len = len(data[0]["plot"])
        self.data_idx = 0

    def stat_log(self):
        now = time.time()
        if now - self.data_points_per_sec_tp > 1:
            self.data_points_per_sec_tp += 1
            print(f"+++ {self.name}: data points per sec: {self.data_points_per_sec}")
            self.data_points_per_sec = 0

    def run(self):
        print(f"+++ {self.name}: eeg streaming thread ready")
        while self.run_cond:
            progress = self.control_data_streaming()
            self.stat_log()
            if progress == 0:
                time.sleep(0.00333)
        
