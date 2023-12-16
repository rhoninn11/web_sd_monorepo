import mne
import matplotlib.pyplot as plt
import re


def get_relevent_channesl(all_channels):
    regex = r"C[0-9]+"
    channels = []
    for name in all_channels:
        if re.match(regex, name):
            channels.append(name)

    return channels

print("+++ eeg antena started")
data_file = "fs/eeg_data.edf"
eeg = mne.io.read_raw_edf(data_file, preload=True)
few_ch = get_relevent_channesl(eeg.ch_names)

few_eeg = eeg.pick_channels(few_ch)

data, times = few_eeg[:]

fig, axes = plt.subplots(len(few_ch), 1, figsize=(10, 7), sharex=True)

for i, channel in enumerate(few_ch):
    axes[i].plot(times, data[i])
    axes[i].set_title(channel)
    axes[i].set_ylabel('Amplitude')

axes[-1].set_xlabel('Time (s)')
plt.show()