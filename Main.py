import random as r
from openai import OpenAI
from Maze import Maze
from Visualizer import Visualizer
from Response_handler import Response_handler as rh



client = OpenAI()

f = open("maze_instruction_v2.1", "r")
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



mazes = Maze(4,5)
simulation = Visualizer(mazes)
INDEX = 0

maze_dataset = mazes.get_dataset()
gpt_adjlist = mazes.get_adjlist_nopath(maze_dataset[INDEX])


pre_prompt = "Here is an adjaceny list of a maze, aswell as the origin point and target point, Solve it: "

prompt = pre_prompt + str(gpt_adjlist)

print("Asking ChatGPT: "+prompt)

#response_basic = ask_gpt(prompt)

#response_basic_fake = "Start (1,3), next move (1,4), next move (4,3), next move (4,4), End (2,3)"

#print ("ChatGPT Response: "+str(response_basic))

#gpt_path = rh.clean_basic(str(response_basic))


gpt_path_fake = [(1,3),(0,3),(0,2),(1,2),(2,2),(2,1), (2,0), (3,0), (4,0), (4,1), (4,2), (4,3), (4,4), (3,4), (2,4), (2,3)]

simulation.view_paths(gpt_path_fake, INDEX)





