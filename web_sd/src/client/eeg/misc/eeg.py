
import mne
import re
import numpy as np
import matplotlib.pyplot as plt
from misc.mel import calculate_mel
import json

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

def comfy_ui_u2_lut(ranges):

    ranges_tmp = []
    for r in ranges:
        ranges_tmp.append(r.copy())

    value = {"delta": 1.3, "theta": 1.4, "alfa": 0.9, "beta": 0.2}

    amp = 0.8
    for r in ranges_tmp:
        plot_data = r["plot"]
        name = r["name"]
        r["plot"] = [max(x*amp - amp/2.0 + value[name], 0) for x in plot_data]

    return ranges_tmp


def save_run_2_json(ranges, file_name):

    delta = ranges[0]["plot"]
    theta = ranges[1]["plot"]
    alfa = ranges[2]["plot"]
    beta = ranges[3]["plot"]

    zip_data = zip(delta, theta, alfa, beta)
    out_data = {
        "names": ["b1", "b2", "s1", "s2"],
        "data": []
    }
    for i, data in enumerate(zip_data):
        # print(f"+++ {i}: {data}")
        out_data["data"].append(data)

    # write to json
    with open(file_name, 'w') as outfile:
        json.dump(out_data, outfile)
    


def load_eeg_data():
    data_file = "fs/eeg_data.edf"
    eeg = mne.io.read_raw_edf(data_file, preload=True)
    # mne_test(eeg)
    ours_ch = get_relevent_channesl(eeg.ch_names)
    print(f"+++ ours ch: {ours_ch}")
    ch_data, times = cli_preview_data(eeg, ours_ch)
    sfreq = eeg.info['sfreq']
    print(f"+++ sfreq: {sfreq}")
    all_electrodes_signal = calculate_mel(ours_ch, ch_data, times) #10 Hz signal

    one_electrod_signal = all_electrodes_signal[0]
    one_electrod_signal = normalize(one_electrod_signal)
    # driving_signals = data_interpolation(driving_signals) #30 Hz signal

    comfy = comfy_ui_u2_lut(one_electrod_signal)
    save_run_2_json(comfy, "fs/comfy.json")

    return one_electrod_signal

    
