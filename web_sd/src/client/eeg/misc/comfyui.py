
import json
import numpy as np

'''general offtop for free u node and comfy ui experiment workflow compiled to python'''

def comfy_ui_u2_lut(signals):
    buckets = signals[0]
    free_u_lut = []
    for fub in buckets:
        free_u_lut.append(fub.copy())

    fu_lut_baseline = {"delta": 1.3, "theta": 1.4, "alfa": 0.9, "beta": 0.2}

    amp = 0.8
    for fub in free_u_lut:
        plot_data = fub["plot"]
        name = fub["name"]
        u_value_evol = [max(x*amp - amp/2.0 + fu_lut_baseline[name], 0) for x in plot_data]
        fub["plot"] = np.array(u_value_evol)

    return free_u_lut


def save_free_u_lut2json(free_u_buckets, file_name):
    delta_b1 = free_u_buckets[0]["plot"]
    theta_b2 = free_u_buckets[1]["plot"]
    alfa_s1 = free_u_buckets[2]["plot"]
    beta_s2 = free_u_buckets[3]["plot"]

    zip_data = zip(delta_b1, theta_b2, alfa_s1, beta_s2)
    out_data = {
        "names": ["b1", "b2", "s1", "s2"],
        "data": []
    }
    for i, data in enumerate(zip_data):
        out_data["data"].append(data)

    # write to json
    with open(file_name, 'w') as outfile:
        json.dump(out_data, outfile)