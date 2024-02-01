import random as r
from openai import OpenAI
from Maze import Maze
from Visualizer import Visualizer
from maze_dataset import MazeDataset, MazeDatasetConfig


client = OpenAI()

f = open("maze_instruction_v1.1", "r")
instruction = f.read()


def ask_gpt(question):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": instruction},
      {"role": "user", "content": question}
    ]
  )
  return completion.choices[0].message


      
  
#maze_size = int(input("Size of the square maze? (eg.'5' -> (5x5): "))


#test_maze = Maze(maze_size)
  
mazes = Maze(5,5)

maze_dataset = mazes.get_dataset()

simulation = Visualizer(maze_dataset[0])



simulation.start_simul()



#print("Solve the following maze: Your Starting coordinate is",test_maze.start,". Your Exit coordinate is",test_maze.exit,". The Size of the maze is",test_maze.size,".")

#test_maze.print_maze()

#print(instruction)









