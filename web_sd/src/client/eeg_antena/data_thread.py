
import mne
import time, re
from src.core.utils.utils_thread import ThreadWrap


def get_relevent_channesl(all_channels):
    regex = r"C[0-9]+"
    channels = []
    for name in all_channels:
        if re.match(regex, name):
            channels.append(name)

    return channels

def load_eeg_data():
    data_file = "fs/eeg_data.edf"
    eeg = mne.io.read_raw_edf(data_file, preload=True)
    few_ch = get_relevent_channesl(eeg.ch_names)

    few_eeg = eeg.pick_channels(few_ch)

    data, times = few_eeg[:]

    preview_samples = 50

    print(f"+++ time preview: {times[:preview_samples]}")
    for i, channel in enumerate(few_ch):
        min_val = min(data[i])
        max_val = max(data[i])
        print(f"+++ channel {channel} preview: {data[i][:preview_samples]} range: {min_val} - {max_val}")



class eeg_source_thread(ThreadWrap):
    def __init__(self, name="eeg_data_source"):
        ThreadWrap.__init__(self, name)
        self.last_data_gen_tp = time.time()
        fps = 30
        self.ttreshold = 1/fps

    def control_data_streaming(self):
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
        while self.run_cond:
            progress = 0
            if progress == 0:
                time.sleep(0.01)

    def preview_data(self):
        load_eeg_data()
        
