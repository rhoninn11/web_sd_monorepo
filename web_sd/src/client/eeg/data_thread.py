
import time, re
from src.core.utils.utils_thread import ThreadWrap

class eeg_source_thread(ThreadWrap):
    def __init__(self, name="eeg_data_source"):
        ThreadWrap.__init__(self, name)
        self.last_data_gen_tp = time.time()
        fps = 30
        self.ttreshold = 1/fps

        self.stream_flag = False

    def control_data_streaming(self):
        now = time.time()
        generate_next_data = now - self.last_data_gen_tp > self.ttreshold
        progress = 0
        if generate_next_data:
            self.last_data_gen_tp += self.ttreshold
            # new_data = self.data_gen()
            # self.out_queue.queue_item(new_data)
            # print(f"+++ eeg data generated")
            # print(f"+++ eeg data: file read simulated")
            progress += 1

        return progress
    

    def run(self):
        print(f"+++ stable diffusion thread ready")
        self.preview_data()
        while self.run_cond:
            progress = self.control_data_streaming()
            if progress == 0:
                time.sleep(0.01)
        
