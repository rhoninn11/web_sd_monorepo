
import numpy as np

class data_history():
    def __init__(self, history_len=10):
        self.history = np.array([])
        self.history_len = history_len

    def __len__(self):
        return len(self.history)

    def populate_history(self, data):
        self.history = np.tile(data, (self.history_len, 1, 1))
        # print(f"+++ history populated: {self.history}")

    def store_data_point(self, data):
        data2fit = np.expand_dims(data, 0)
        self.history = np.concatenate((self.history, data2fit), axis=0)
        self.history = self.history[1:]
        # print(f"+++ history updated: {self.history}")
    
    def get_last_value(self):
        last_value = self.history[-1]
        # print(f"+++ history last value: {last_value}")
        return last_value