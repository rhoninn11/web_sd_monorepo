


class data_history():
    def __init__(self, history_len=10):
        self.history = []
        self.history_len = history_len

    def __len__(self):
        return len(self.history)

    def populate_history(self, data):
        for i in range(len(data)):
            self.history.append([data[i]]*self.history_len)

        print(f"+++ history populated: {self.history}")

    def store_data_point(self, data):
        for i in range(len(data)):
            self.history[i].pop(0)
            self.history[i].append(data[i])

    def get_history_copy(self):
        copy_of_history = []
        for i in range(len(self.history)):
            copy_of_history.append(self.history[i].copy())
        return copy_of_history