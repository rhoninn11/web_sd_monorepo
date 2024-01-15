
import re
import mne
import numpy as np
import matplotlib.pyplot as plt

from misc.mel import calculate_mel
from misc.comfyui import comfy_ui_u2_lut, save_free_u_lut2json

def get_c_channels(all_channels):
    regex = r"C[0-9]+"
    channels = []
    for name in all_channels:
        if re.match(regex, name):
            channels.append(name)

    return channels

def unpack_channels(eeg, few_ch, verbose=False):
    few_eeg = eeg.pick(few_ch)
    data, times = few_eeg[:]

    return data, times

def plot_data(buckets):
    for b in buckets:
        plt.plot(b["plot"], label=b["name"])

    plt.legend()
    plt.show()

def normalize(processed_signals):
    per_signal_max = []
    for buckets in processed_signals:
        signal_max = max([max(b["plot"]) for b in buckets])
        per_signal_max.append(signal_max)

    global_max = max(per_signal_max)
    global_amp = 1/global_max
    for buckets in processed_signals:
        for b in buckets:
            b["plot"] = b["plot"]*global_amp    

    return processed_signals


def simple_inp(data):
    ''' interpolation of np.array data x3 from 10fps -> 30fps'''
    interpolated_data = np.array([])
    for i in range(len(data)-1):
        this_val = data[i]
        next_val = data[i+1]
        delta = next_val - this_val

        interpolated_chunk = [this_val, this_val+delta/3, this_val+delta*2/3]
        interpolated_data = np.append(interpolated_data, interpolated_chunk)

    return interpolated_data

def signal_inp(signals):
    for buckets in signals:
        for b in buckets:
            b["plot"] = simple_inp(b["plot"])
        
    return signals

def load_eeg_data():
    data_file = "fs/eeg_data.edf"
    eeg = mne.io.read_raw_edf(data_file, preload=True)
    sr = eeg.info['sfreq']
    c_chann = get_c_channels(eeg.ch_names)
    print(f"+++ sfreq: {sr}")
    print(f"+++ ours ch: {c_chann}")
    ch_data, times = unpack_channels(eeg, c_chann)
    all_electrodes_signal = calculate_mel(c_chann, ch_data, times) #10 Hz signal

    # all_electrodes_signal = all_electrodes_signal[0:1]
    all_electrodes_signal = normalize(all_electrodes_signal)
    final_driving_signals = signal_inp(all_electrodes_signal) #30 Hz signal
    print(f"+++ final driving signals: {len(final_driving_signals)}")
    # comfy = comfy_ui_u2_lut(all_electrodes_signal)
    # save_free_u_lut2json(comfy, "fs/comfy.json")

    return final_driving_signals

    
