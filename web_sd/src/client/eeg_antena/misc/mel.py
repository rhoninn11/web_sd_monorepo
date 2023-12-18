

def normalize(data):
    min_val = min(data)
    max_val = max(data)
    delta = max_val - min_val
    amp = 1/delta

    data = [(x - min_val)*amp for x in data]
    return data

def calculate_mel(ch_namse, data, times):
    print(f"+++ mel calculation")

    ch = ch_namse[0]
    ch_data = normalize(data[0])

    print(f"+++ data for {ch}: {ch_data}")