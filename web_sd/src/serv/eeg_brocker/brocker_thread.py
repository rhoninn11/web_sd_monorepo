
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
        pos_list = []
        scale_list = []
        color_list = []
        samples = 10
        f1 = 1 #Hz
        f2 = 2.13
        f3 = 3.13
        for i in range(samples):
            tp = i/(samples-1) + self.last_data_gen_tp
            pos_val = (math.sin(2*3.14*f1*tp) + 1) * 0.5
            scale_val = (math.sin(2*3.14*f2*tp) + 1) * 0.5
            color_val = (math.sin(2*3.14*f3*tp) + 1) * 0.5
            pos_list.append(pos_val)
            scale_list.append(scale_val)
            color_list.append(color_val)

        return [pos_list, scale_list, color_list]


    
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



