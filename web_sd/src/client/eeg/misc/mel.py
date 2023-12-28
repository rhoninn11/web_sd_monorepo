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
    return np.array(data)

ranges = [
    {"name": "delta", "f_s": 0.5, "f_e": 4.0, "idx_s": 0, "idx_e": 0},
    {"name": "theta", "f_s": 4.0, "f_e": 8.0, "idx_s": 0, "idx_e": 0},
    {"name": "alfa", "f_s": 8.0, "f_e": 13.0, "idx_s": 0, "idx_e": 0},
    {"name": "beta", "f_s": 13.0, "f_e": 30.0, "idx_s": 0, "idx_e": 0},
]

def calculate_mel(ch_namse, data, times):
    print(f"+++ mel calculation")

    ch = ch_namse[0]
    ch_data = normalize(data[0])

    sampling_rate = 160
    ch_s_chunk = ch_data

    # plt.plot(times_s_chunk, ch_s_chunk)
    # plt.show()

    signal = librosa.feature.melspectrogram(y=ch_s_chunk, sr=sampling_rate, n_fft=512, hop_length=16)
    signal_db = librosa.power_to_db(signal, ref=np.max)

    print(signal.shape)
    print(signal_db.shape)

    # plt.plot(signal_db)
    # plt.show()

    # clamp lower then -30 db
    signal_db[signal_db < -30] = -30
    signal_db = signal_db + 30


    # mel has 128 bins spread on 80hz
    # for ranges get array indices
    f_delta = 80/128
    for r in ranges:
        r["idx_s"] = math.ceil(r["f_s"]/f_delta)
        r["idx_e"] = math.ceil(r["f_e"]/f_delta)

    for r in ranges:
        proxy = signal_db[r["idx_s"]:r["idx_e"]]
        t_proxy = np.transpose(proxy)
        plot_values = [np.sum(x) for x in t_proxy]
        r["plot"] = plot_values

    # for each range create plot on the singel matplot lib figure

    return ranges


    # # print(ranges)
        

    # plt.figure(figsize=(10, 4))
    # librosa.display.specshow(signal_db, sr=sampling_rate, x_axis='time', y_axis='mel')
    # plt.colorbar(format='%+2.0f dB')
    # plt.title('Mel Spectrogram')
    # plt.tight_layout()
    # plt.show()

    # print(f"from mel calculation")

    # print(f"+++ data for {ch}: {ch_data}")