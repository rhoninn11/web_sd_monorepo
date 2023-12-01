
import time

from core.utils.utils_thread import ThreadWrap


class brocker_logic_thread(ThreadWrap):
    def __init__(self):
        ThreadWrap.__init__(self)

    def process_request(self, request):
        si = self.script_index
        if si.has_script(request):
            si.run_script(request, self.out_queue)

        return
    
    def generate_eeg_data(self):
        generate_next_data = False
        progress = 0
        if generate_next_data:
            self.out_queue.queue_item("eeg_data")
            progress += 1

        return progress
    

    def run(self):
        print(f"+++ stable diffusion thread ready")
        in_queue = self.in_queue
        while self.run_cond:
            progress = self.generate_eeg_data()
            if progress == 0:
                time.sleep(0.1)



