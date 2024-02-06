import random as r
from openai import OpenAI
from Maze import Maze
from Visualizer import Visualizer
from Response_handler import Response_handler as rh
from TestManager import TestManager as tm



client = OpenAI()

f = open("maze_instruction_v2.4", "r")
instruction = f.read()


def ask_gpt(question):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": instruction},
      {"role": "user", "content": question}
    ]
  )
  return completion.choices[0].message.content


#3: 1,3,4,6,7,9
#4: 2,4,8?,9,
#5: 5,9
def run_single(index, size):
  mazes = Maze(size,10)
  simulation = Visualizer(mazes)
  INDEX = index

  maze_dataset = mazes.get_dataset()
  gpt_adjlist = mazes.get_adjlist_nopath(maze_dataset[INDEX])

  pre_prompt = "Here is an adjaceny list of a maze, aswell as the origin point and target point, Solve it: "

  prompt = pre_prompt + str(gpt_adjlist)

  print("Asking ChatGPT: "+prompt)

  response_basic = ask_gpt(prompt)

  print ("ChatGPT Response: "+str(response_basic))

  gpt_path = rh.clean_basic(str(response_basic))

  simulation.view_paths(gpt_path, INDEX)


def run_test(n_mazes, size, repeats):

  test_mazes = Maze(size,n_mazes)
  test_maze_dataset = test_mazes.get_dataset()

  return tm.test(test_maze_dataset, repeats)








#run_single(3,3)
  
test_score = run_test(5, 3, 5)


#response_basic_fake = "Start (1,3), next move (1,4), next move (4,3), next move (4,4), End (2,3)"
#gpt_path_fake = [(1,3),(0,3),(0,2),(1,2),(2,2),(2,1), (2,0), (3,0), (4,0), (4,1), (4,2), (4,3), (4,4), (3,4), (2,4), (2,3)]








