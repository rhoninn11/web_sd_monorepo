
import mne
import re

from misc.mel import calculate_mel

def get_relevent_channesl(all_channels):
    regex = r"C[0-9]+"
    channels = []
    for name in all_channels:
        if re.match(regex, name):
            channels.append(name)

    return channels

def cli_preview_data(eeg, few_ch, verbose=False):
    few_eeg = eeg.pick(few_ch)
    data, times = few_eeg[:]

    sample_num = len(times)
    print(f"+++ sample num: {sample_num}")
    if verbose:
        preview_samples = 160 # 160 smpl/s
        print(f"+++ time preview: {times[:preview_samples]}")
        for i, channel in enumerate(few_ch):
            min_val = min(data[i])
            max_val = max(data[i])
            print(f"+++ channel {channel} preview: {data[i][:preview_samples]} range: {min_val} - {max_val}")

    return data, times


def load_eeg_data():
    data_file = "fs/eeg_data.edf"
    eeg = mne.io.read_raw_edf(data_file, preload=True)
    ours_ch = get_relevent_channesl(eeg.ch_names)
    print(f"+++ ours ch: {ours_ch}")
    data, times = cli_preview_data(eeg, ours_ch)
    calculate_mel(ours_ch, data, times)
    
