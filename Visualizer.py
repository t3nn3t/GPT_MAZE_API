import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import patches
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
from matplotlib import transforms
from matplotlib.transforms import Affine2D



from maze_dataset.plotting import MazePlot
from maze_dataset.tokenization import MazeTokenizer, TokenizationMode
from maze_dataset.dataset.rasterized import process_maze_rasterized_input_target

class Visualizer:
    def __init__(self, s_maze):
        self.mazes = s_maze
        self.maze_dataset = self.mazes.get_dataset()
        self.maze_adjlist = self.get_clean_adjlist(self.mazes.get_adjlist(self.maze_dataset[0]))
        self.set_style()

        self.input, self.target = process_maze_rasterized_input_target(self.maze_dataset[0])
        self.fig, self.ax = plt.subplots(1, 4, figsize=(12, 5))


    def view_paths(self, gpt_path):
        self.draw_window()

        pos = 0.15
        spacing = 0.7/len(gpt_path)
        
        for move in gpt_path:
            self.display_move(move, pos)
            pos += spacing
            plt.pause(1)

        plt.show()



    def set_style(self):
        plt.style.use("dark_background")
        return 0

        


    def draw_window(self):
        print("plotting...")
        
        tr = Affine2D().rotate_deg(-90)
        moveright = Affine2D().translate(0.0, 23.0)
        scale = Affine2D().scale(1.0,1.0)


        self.ax[0].imshow(self.maze_dataset[0].as_pixels())
        self.ax[0].axis('off')
        self.ax[1].imshow(self.input, transform= tr + moveright + scale + self.ax[1].transData)
        self.ax[1].axis('off')


        response = ["Response: "," ",]
        

        text_pos = (0.1, 0.9)


        # Wrap the text based on the width of the rectangle
        adj_text = '\n'.join(self.maze_adjlist)
        response_head = '\n'.join(response)

        self.ax[2].text(text_pos[0], text_pos[1], adj_text, ha='left', va='top', fontsize=8, fontname='monospace', wrap=True)
        self.ax[2].axis('off')

        self.ax[3].text(text_pos[0]-0.5, text_pos[1], response_head, ha='left', va='top', fontsize=8, fontname='monospace', wrap=True)
        self.ax[3].axis('off')
        #plt.tight_layout()
        plt.ion()
        plt.show(block=False)

        



    
    def display_move(self, move, pos):
        text = str(move)
        self.ax[3].text(-0.4, 1-pos, text, ha='left', va='top', fontsize=8, fontname='monospace', wrap=True)

        # Get the x-axis and y-axis limits of ax[1]
        xlim = self.ax[1].get_xlim()
        ylim = self.ax[1].get_ylim()

        # Calculate width and height
        width = xlim[1] - xlim[0]
        unit = width/((self.mazes.get_size()*2))
        print(width)
        print(unit)
        print(unit*10)
        
        
        OFFSET = 0.5
        MAZE_RATIO = 11/5
        # flip y because the maze coordinates are inversed
        x = move[0] * (MAZE_RATIO)
        y = (4 - move[1]) * (MAZE_RATIO)

        #FIX PLOTTING POSITIONS, i think unit is wrong

        self.ax[1].scatter((unit*1)+OFFSET,(unit*1)+OFFSET, color='red', marker='o', label='New Point')
        plt.draw()



    def get_clean_adjlist(self, adj_list_prev):

        adj_list = ["Adjency List: "] + re.split(" ; ",adj_list_prev)
        adj_list[1] = adj_list[1].replace("<ADJLIST_START> ",'\n')
        
        end_index = next(i for i, v in enumerate(adj_list) if '<ADJLIST_END>' in v)

        result_list = adj_list[0:end_index]

        end_info = adj_list[end_index]
        end_info = re.split(' ',end_info)
        start_pos = ["Start: " + end_info[2]]
        target_pos = ["Target: " + end_info[5]]

        result_list = result_list + [''] + start_pos +  target_pos

        return (result_list)
    










