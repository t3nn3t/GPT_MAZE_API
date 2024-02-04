import random as r
from openai import OpenAI
from Maze import Maze
from Visualizer import Visualizer
from Response_handler import Response_handler as rh



client = OpenAI()

f = open("maze_instruction_v2.0", "r")
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

  
mazes = Maze(5,5)
simulation = Visualizer(mazes)

maze_dataset = mazes.get_dataset()
gpt_adjlist = mazes.get_adjlist_nopath(maze_dataset[0])

pre_prompt = "Here is an adjaceny list of a maze, aswell as the start point and target point, Solve it: "

prompt = pre_prompt + str(gpt_adjlist)

#response_basic = ask_gpt(prompt)

#gpt_path = rh.clean_basic(response_basic)


gpt_path_fake = [(1,3),(0,3),(0,2),(1,2),(2,2),(2,1), (2,0), (3,0), (4,0), (4,1), (4,2), (4,3), (4,4), (3,4), (2,4), (2,3)]

simulation.view_paths(gpt_path_fake)





