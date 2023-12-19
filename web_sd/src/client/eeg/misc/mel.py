import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

def normalize(data):
    min_val = min(data)
    max_val = max(data)
    delta = max_val - min_val
    amp = 1/delta

    data = [(x - min_val)*amp for x in data]
    return np.array(data)

def calculate_mel(ch_namse, data, times):
    print(f"+++ mel calculation")

    ch = ch_namse[0]
    ch_data = normalize(data[0])

    sampling_rate = 160
    ch_s_chunk = ch_data[:sampling_rate]
    times_s_chunk = times[:sampling_rate]

    # plt.plot(times_s_chunk, ch_s_chunk)
    # plt.show()

    signal = librosa.feature.melspectrogram(y=ch_data, sr=sampling_rate, n_fft=1024, hop_length=8)
    signal_db = librosa.power_to_db(signal, ref=np.max)

    print(signal.shape)
    print(signal_db.shape)

    # plt.plot(signal_db)
    # plt.show()

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(signal_db, sr=sampling_rate, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    plt.tight_layout()
    plt.show()

    print(f"from mel calculation")

    # print(f"+++ data for {ch}: {ch_data}")