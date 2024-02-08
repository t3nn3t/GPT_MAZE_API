import random as r
from openai import OpenAI
from Maze import Maze
from Visualizer import Visualizer
from Response_handler import Response_handler as rh
from TestManager import TestManager as tm

# TO DO
# - Make Random path bot as a control
# - Improve Prompts to get best result
# - Increase X shot testing 



#3: 1,3,4,6,7,9
#4: 2,4,8?,9,
#5: 5,9
def run_single(index, size):
  broker = rh()
  mazes = Maze(size,10)
  simulation = Visualizer(mazes)
  INDEX = index

  maze_dataset = mazes.get_dataset()
  gpt_adjlist = mazes.get_adjlist_nopath(maze_dataset[INDEX])

  prompt_path = str(gpt_adjlist)

  response_basic = broker.ask_gpt(prompt_path)

  print ("ChatGPT Response: "+str(response_basic))

  gpt_path = broker.clean_basic(str(response_basic))

  simulation.view_paths(gpt_path, INDEX)


def run_test(n_mazes, size, repeats):
  broker = rh()
  test_mazes = Maze(size,n_mazes)

  simulation = Visualizer(test_mazes)

  return tm.test(test_mazes, repeats, simulation, broker)




#run_single(0,4)
  
test_score, gpt_total_moves, random_total_moves = run_test(n_mazes=15, size=3, repeats=3)
print(str(round(test_score,2))+"%")
print("gpt moves: "+ str(gpt_total_moves))
print("random moves: "+ str(random_total_moves))


#response_basic_fake = "Start (1,3), next move (1,4), next move (4,3), next move (4,4), End (2,3)"
#gpt_path_fake = [(1,3),(0,3),(0,2),(1,2),(2,2),(2,1), (2,0), (3,0), (4,0), (4,1), (4,2), (4,3), (4,4), (3,4), (2,4), (2,3)]








