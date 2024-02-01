import pandas as pd
import matplotlib.pyplot as plt
from itertools import count

class Visualizer:
    def __init__(self):
        
        plt.style.use('fivethirtyeight')

    def start_simul(self):
        self.draw_window()


    def draw_window(self):
        x_vals = [0,1,2,3,4,5]
        y_vals = [0,1,2,3,4,5]
        print("plotting...")
        plt.plot(x_vals, y_vals)

        plt.tight_layout()
        plt.show()







