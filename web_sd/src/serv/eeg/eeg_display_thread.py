
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from core.utils.utils_thread import ThreadWrap

from data_history import data_history

class eeg_display_thread(ThreadWrap):
    def __init__(self, name="eeg_display"):
        ThreadWrap.__init__(self, name=name)
        self.history_ref = data_history()

        self.fps = 2
        self.frame_time = 1/self.fps
        self.last_frame_timestamp = time.time()

    def bind_history(self, history):
        self.history_ref = history

    def update_display(self):
        now = time.time()
        update_cond = now - self.last_frame_timestamp > self.frame_time

        if update_cond:
            self.last_frame_timestamp += self.frame_time

            shape = self.history_ref.history.shape
            print(f"+++ {self.name}: history shape: {shape}, last value: {self.last_frame_timestamp}")

    def plot_test(self):

        num_points = 30  # Liczba punktów na wykresie
        x = np.linspace(0, 2 * np.pi, num_points)

        plt.ion()
        fig, ax = plt.subplots()
        lines = [ax.plot([], [], lw=2)[0] for _ in range(3)]

        def init():
            ax.set_xlim(0, 2 * np.pi)
            ax.set_ylim(-1, 1)
            return lines

        def update(_):
            current_time = time.time()
            
            lines[0].set_data(x, np.sin(2 * np.pi * 2 * x - current_time))
            lines[1].set_data(x, np.sin(2 * np.pi * 1 * x - current_time))
            lines[2].set_data(x, np.sin(2 * np.pi * 3 * x - current_time))

            lines[0].set_color('blue')
            lines[1].set_color('green')
            lines[2].set_color('red')

            return lines

        ani = FuncAnimation(fig, update, frames=10, init_func=init, blit=True)

        plt.draw()
            
    def run(self):
        print(f"+++ {self.name}: thread ready")

        # self.plot_test()



        while self.run_cond:
            self.update_display()
            time.sleep(0.00333)