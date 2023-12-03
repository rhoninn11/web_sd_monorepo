
import math
import time

from core.utils.utils_thread import ThreadWrap


class brocker_logic_thread(ThreadWrap):
    def __init__(self):
        ThreadWrap.__init__(self)
        self.last_data_gen_tp = time.time()
        fps = 30
        self.ttreshold = 1/fps

    def process_request(self, request):
        si = self.script_index
        if si.has_script(request):
            si.run_script(request, self.out_queue)

        return
    
    def data_gen(self):
        data_list = []
        samples = 10
        f = 1 #Hz
        for i in range(samples):
            off = i/(samples-1) + self.last_data_gen_tp
            sv = math.sin(2*3.14*f+off)
            data_list.append(sv)

        return data_list


    
    def control_data_gen(self):
        now = time.time()
        generate_next_data = now - self.last_data_gen_tp > self.ttreshold
        progress = 0
        if generate_next_data:
            self.last_data_gen_tp += self.ttreshold
            new_data = self.data_gen()
            self.out_queue.queue_item(new_data)
            # print(f"+++ eeg data generated")
            progress += 1

        return progress
    

    def run(self):
        print(f"+++ stable diffusion thread ready")
        in_queue = self.in_queue
        while self.run_cond:
            progress = self.control_data_gen()
            if progress == 0:
                time.sleep(0.01)



