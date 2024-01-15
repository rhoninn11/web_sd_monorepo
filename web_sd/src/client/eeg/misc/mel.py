import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import math

def normalize(data):
    min_val = min(data)
    max_val = max(data)
    delta = max_val - min_val
    amp = 1/delta

    # data = [(x - min_val)*amp for x in data]
    data = data * amp
    return data

def get_buckets_template():
    ranges = [
        {"name": "delta", "f_s": 0.5, "f_e": 4.0, "idx_s": 0, "idx_e": 0},
        {"name": "theta", "f_s": 4.0, "f_e": 8.0, "idx_s": 0, "idx_e": 0},
        {"name": "alfa", "f_s": 8.0, "f_e": 13.0, "idx_s": 0, "idx_e": 0},
        {"name": "beta", "f_s": 13.0, "f_e": 30.0, "idx_s": 0, "idx_e": 0},
    ]
    return ranges

def wave_to_mel_processing(waveform_data, sampling_rate: int):

    # waveform_data = normalize(waveform_data)

    # check waveform
    # plt.plot(waveform_data)
    # plt.show()

    signal = librosa.feature.melspectrogram(y=waveform_data, sr=sampling_rate, n_fft=256, hop_length=16)
    signal_db = librosa.power_to_db(signal, ref=np.max)

    # brutal preprocessing
    treshold_lvl = -40
    signal_db[signal_db < treshold_lvl] = treshold_lvl
    signal_db = signal_db - treshold_lvl
    
    # check mel spectrogram
    # librosa.display.specshow(signal_db, sr=sampling_rate, hop_length=16, x_axis='time', y_axis='mel')
    # plt.colorbar(format='%+2.0f dB')
    # plt.title('Mel spectrogram')
    # plt.show()

    return signal_db


def put_in_neuro_backets(mel_signal):

    f_delta = 80/128
    # mel has 128 bins spread on 80hz
    # (automatic or from n_fft?)
    # for ranges get array indices
    buckets = get_buckets_template()
    for r in buckets:
        r["idx_s"] = math.ceil(r["f_s"]/f_delta)
        r["idx_e"] = math.ceil(r["f_e"]/f_delta)

    for r in buckets:
        proxy = mel_signal[r["idx_s"]:r["idx_e"]]
        t_proxy = np.transpose(proxy)
        plot_values = [np.sum(x) for x in t_proxy]
        r["plot"] = np.array(plot_values)

    return buckets


def calculate_mel(channle_names, channel_data, times):
    print(f"+++ mel calculation")
    sampling_rate = 160

    channel_buckets = []
    for wave_data in channel_data:
        mel_signal = wave_to_mel_processing(wave_data, sampling_rate)
        neuro_buckets = put_in_neuro_backets(mel_signal)
        channel_buckets.append(neuro_buckets)

    return channel_buckets