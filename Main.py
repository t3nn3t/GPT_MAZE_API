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
def run_single(index, size, supplier, model, prompt):
  broker = rh(model = model, prompt = prompt)
  mazes = Maze(size,121)
  simulation = Visualizer(mazes)
  INDEX = index

  maze_dataset = mazes.get_dataset()
  llm_adjlist = mazes.get_adjlist_nopath(maze_dataset[INDEX])

  prompt_path = str(llm_adjlist)

  if str.lower(supplier)=="openai":
    response_basic = broker.ask_gpt(prompt_path)
  elif str.lower(supplier)=="google":
    response_basic = broker.ask_gemini(prompt_path)
  else:
    raise Exception("Error: Supplier not recognised")

  print ("\n"+str(model)+" Response: "+str(response_basic)+"\n")

  #gpt_path = broker.clean_cot(str(response_basic))
  gpt_path = broker.clean_adv(str(response_basic))

  simulation.view_paths(gpt_path, INDEX)

def test_llm(prompt):
  broker = rh()

  response_basic = broker.ask_gemini(prompt)

  print ("LLM Response: "+str(response_basic))



def run_test(n_mazes, size, repeats):
  broker = rh()
  test_mazes = Maze(size,n_mazes)

  simulation = Visualizer(test_mazes)

  return tm.test(test_mazes, repeats, simulation, broker)


#model = gpt-3.5-turbo-0125, gpt-4 | gemini-1.0-pro
run_single(index=119,size=4, supplier = "google", model = "gemini-1.0-pro", prompt = "system_prompt_v1.0")

#test_llm("what can you do?")
  
#model, prompt
"""
test_score, gpt_total_moves, random_total_moves, opt_moves = run_test(n_mazes=15, size=5, repeats=3)
print(str(round(test_score,2))+"%")
print("gpt moves: "+ str(gpt_total_moves))
print("random moves: "+ str(random_total_moves))
print("optimal moves: "+ str(opt_moves))

print("\n\n")

print("extra gpt moves: "+ str(gpt_total_moves - opt_moves))
print("extra random moves: "+ str(random_total_moves - opt_moves))




#response_basic_fake = "Start (1,3), next move (1,4), next move (4,3), next move (4,4), End (2,3)"
#gpt_path_fake = [(1,3),(0,3),(0,2),(1,2),(2,2),(2,1), (2,0), (3,0), (4,0), (4,1), (4,2), (4,3), (4,4), (3,4), (2,4), (2,3)]

"""




