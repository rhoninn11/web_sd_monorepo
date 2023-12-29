
import mne
import re
import numpy as np
import matplotlib.pyplot as plt
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

def plot_data(ranges):
        for r in ranges:
            plt.plot(r["plot"], label=r["name"])

        plt.legend()
        plt.show()

def normalize(ranges):
    max_glob = max([max(r["plot"]) for r in ranges])
    for r in ranges:
        amp = 1/max_glob
        r["plot"] = [x*amp for x in r["plot"]]

    return ranges

def data_interpolation(ranges):
    for r in ranges:
        plot_data = r["plot"]
        name = r["name"]
        print(f"+++ ({name}) plot data shape: {len(plot_data)}")

        interp_data = []
        for i in range(len(plot_data)-1):
            this_val = plot_data[i]
            next_val = plot_data[i+1]
            delta = next_val - this_val
            interp_data.extend([this_val, this_val+delta/3, this_val+delta*2/3])

        r["plot"] = interp_data

    return ranges



def load_eeg_data():
    data_file = "fs/eeg_data.edf"
    eeg = mne.io.read_raw_edf(data_file, preload=True)
    # mne_test(eeg)
    ours_ch = get_relevent_channesl(eeg.ch_names)
    print(f"+++ ours ch: {ours_ch}")
    data, times = cli_preview_data(eeg, ours_ch)
    sfreq = eeg.info['sfreq']
    print(f"+++ sfreq: {sfreq}")
    driving_signals = calculate_mel(ours_ch, data, times) #10 Hz signal
    # plot_data(driving_signals)
    driving_signals = normalize(driving_signals)
    # plot_data(driving_signals)
    driving_signals = data_interpolation(driving_signals) #30 Hz signal
    # plot_data(driving_signals)

    return driving_signals

    
