import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import patches
import pandas as pd
import matplotlib.pyplot as plt
import re
import random
import numpy as np
from matplotlib import transforms
from matplotlib.transforms import Affine2D, Transform



from maze_dataset.plotting import MazePlot
from maze_dataset.tokenization import MazeTokenizer, TokenizationMode
from maze_dataset.dataset.rasterized import process_maze_rasterized_input_target

class Visualizer:
    def __init__(self, s_maze):
        self.mazes = s_maze
        self.maze_dataset = self.mazes.get_dataset()
        self.set_style()
        self.fig, self.ax = plt.subplots(1, 4, figsize=(12, 5))


    def check_paths(self, gpt_path, index):
        adjacency_dict = self.mazes.get_adjacency_dict(self.maze_dataset[index])
        _,target_point = self.mazes.get_target_point(self.maze_dataset[index])
        _,origin_point = self.mazes.get_start_point(self.maze_dataset[index])
        prev_move = 0
        move_count = 0
        still_legal = True
        for move in gpt_path:
            move_count += 1
            #check first move is at start
            if move_count==1:
                if origin_point != move:
                    still_legal = False
                    break

            legal = self.check_legal(prev_move, move, adjacency_dict)

            if not legal:
                still_legal = False
            prev_move = move

            if move==target_point:
                break
            
        if still_legal and prev_move==target_point:
            return (move_count)
        else:
            return -1
        
        
    def check_random(self, index, max):
        adjacency_dict = self.mazes.get_adjacency_dict(self.maze_dataset[index])
        start_point,_ = self.mazes.get_start_point(self.maze_dataset[index])
        target_point,_ = self.mazes.get_target_point(self.maze_dataset[index])

        prev_move = 0

        solved = False
        MAX = max
        move_count = 0
        while not solved:
            move_count += 1
            
            if move_count>=MAX:
                print("Random agent failed to solve in "+str(MAX)+" moves")
                break
            
            #start at the origin point
            if prev_move==0:
                prev_move = start_point
                continue

            #pick random legal move from adjacency list
            prev_move = random.choice(adjacency_dict[prev_move])

            if prev_move==target_point:
                solved = True

        return move_count

            


    def view_paths(self, gpt_path, index):
        self.draw_window(index)
        _,target_point = self.mazes.get_target_point(self.maze_dataset[index])
        pos = 0.15
        spacing = 0.7/len(gpt_path)
        
        adjacency_dict = self.mazes.get_adjacency_dict(self.maze_dataset[index])
        prev_move = 0
        move_count = 0
        still_legal = True

        plt.pause(0.5)
        
        for move in gpt_path:
            move_count += 1
            legal = self.check_legal(prev_move, move, adjacency_dict)
            if not legal:
                still_legal = False

            self.display_move(move, pos, legal)
            pos += spacing
            if move==target_point:
                break
            prev_move = move
            plt.pause(0.5)

        if still_legal:
            self.display_success(move_count)
            print("-----MAZE SOLVED SUCCESSFULLY-----")
            print("\nMOVES USE: "+ str(move_count))
            
        else:
            self.display_fail()
            print("-----FAILED TO SOLVE MAZE-----")
        
        plt.show()

        



    def set_style(self):
        #plt.style.use("dark_background")
        return 0



    def draw_window(self, index):
        print("plotting...")

        maze_size = self.mazes.get_size()
        
        tr = Affine2D().rotate_deg(-90)
        moveax1 = Affine2D().translate(0.0, 0.0)
        moveax2 = Affine2D().translate(0.0, 0.0)

        if (maze_size==5):
            moveax1= Affine2D().translate(0.0, 10.0)
            moveax2= Affine2D().translate(0.0, 23.0)
        if (maze_size==4):
            moveax1= Affine2D().translate(0.0, 8.0)
            moveax2= Affine2D().translate(0.0, 19.0)
        if (maze_size==3):
            moveax1= Affine2D().translate(0.0, 6.0)
            moveax2= Affine2D().translate(0.0, 15.0)
        
        input, target = process_maze_rasterized_input_target(self.maze_dataset[index])
        


        self.ax[0].imshow(self.maze_dataset[index].as_pixels(), transform= tr + moveax1 + self.ax[0].transData)
        self.ax[0].axis('off')
        self.ax[1].imshow(input, transform= tr + moveax2 + self.ax[1].transData)
        self.ax[1].axis('off')


        response = ["Response: "," ",]
        

        text_pos = (0.1, 0.9)


        # Wrap the text based on the width of the rectangle
        adj_list = self.get_clean_adjlist(self.mazes.get_adjlist(self.maze_dataset[index]))
        adj_text = '\n'.join(adj_list)
        response_head = '\n'.join(response)

        self.ax[2].text(text_pos[0], text_pos[1], adj_text, ha='left', va='top', fontsize=8, fontname='monospace', wrap=True)
        self.ax[2].axis('off')

        self.ax[3].text(text_pos[0]-0.5, text_pos[1], response_head, ha='left', va='top', fontsize=8, fontname='monospace', wrap=True)
        self.ax[3].axis('off')


        plt.tight_layout()

        plt.text(-3.8, 0.8, "SHORTEST PATH", c='black', ha='center')
        plt.text(-2.36, 0.8, "GPT PATH", c='black', ha='center')

        plt.draw()

        
    
    def display_move(self, move, pos, legal):
        text = str(move)
        self.ax[3].text(-0.4, 1-pos, text, ha='left', va='top', fontsize=8, fontname='monospace', wrap=True)

        MAZE_RATIO = 2.0
        UNIT = 2.0 * MAZE_RATIO
        BORDER_SIZE = 3.0
        OFFSET = 0.5
        # flip y because the maze coordinates are inversed
        x = move[0] 
        y = ((self.mazes.get_size() - 1) - move[1])

        if (legal):
            self.ax[1].scatter(BORDER_SIZE+(UNIT*x)+OFFSET,BORDER_SIZE+(UNIT*y)+OFFSET,s=40.0,color='blue', marker='o', label='New Point', alpha = 0.4)
        else:
            self.ax[1].scatter(BORDER_SIZE+(UNIT*x)+OFFSET,BORDER_SIZE+(UNIT*y)+OFFSET,s=40.0,color='orange', marker='o', label='New Point', alpha = 0.4)
        
        plt.draw()


    def check_legal(self, prev_move, move, adj_dict):
        
    
        if (prev_move==0):
            if (move[0]>=0 and move[0]< self.mazes.get_size()) and (move[1]>=0 and move[1]< self.mazes.get_size()):
                return True
            else:
                return False
            
        #gpt sometimes reoutputs the target point when solving
        if (prev_move==move):
            return True
        

        prev_move = str(prev_move[0])+','+str(prev_move[1])
        move = str(move[0])+','+str(move[1])

        if prev_move not in adj_dict:
            return False

        for poss_move in adj_dict[prev_move]:
            if poss_move == move:
                return True
        
        return False



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
    

    def display_success(self, n_moves):
        plt.text(-2.36, 0.17, "SUCCESSFULLY SOLVED MAZE IN "+str(n_moves)+" MOVES", c='green', ha='center')
        plt.draw()
        
    def display_fail(self):
        plt.text(-2.36, 0.17, "FAILED TO SOLVE MAZE", c='red', ha='center')
        plt.draw()
    










