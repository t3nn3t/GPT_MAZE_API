import pandas as pd
import matplotlib.pyplot as plt
from itertools import count

from maze_dataset.plotting import MazePlot
from maze_dataset.tokenization import MazeTokenizer, TokenizationMode
from maze_dataset.dataset.rasterized import process_maze_rasterized_input_target

class Visualizer:
    def __init__(self, s_maze):
        self.maze = s_maze

    def start_simul(self):
        self.draw_window()


    def draw_window(self):
        print("plotting...")
        
        input, target = process_maze_rasterized_input_target(self.maze)
        fig, ax = plt.subplots(1, 2)
        ax[0].imshow(input)
        ax[1].imshow(target)

        plt.tight_layout()
        plt.show()







