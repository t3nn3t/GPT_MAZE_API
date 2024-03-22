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
def run_single(index, size, supplier, model, prompt, reflexion=False, debug=True):

  broker = rh(model = model, prompt = prompt)
  mazes = Maze(size,121)
  simulation = Visualizer(mazes)
  INDEX = index

  basic_prompts = ["system_prompt_astar.txt", "system_prompt_basic.txt", "system_prompt_printfirst.txt"]
  cot_prompts = ["system_prompt_cot.txt"]


  maze_dataset = mazes.get_dataset()
  llm_adjlist = mazes.get_adjlist_nopath(maze_dataset[INDEX])

  prompt_path = str(llm_adjlist)

  if str.lower(supplier)=="openai":
    response_basic = broker.ask_gpt(prompt_path, reflexion=reflexion, debug=debug)
  elif str.lower(supplier)=="google":
    response_basic = broker.ask_gemini(prompt_path,reflexion=reflexion, debug=debug)
  else:
    raise Exception("Error: Supplier not recognised")

  print ("\n"+str(model)+" Response: "+str(response_basic)+"\n")

  

  if prompt in basic_prompts:
    llm_path = broker.clean_adv(str(response_basic))
  elif prompt in cot_prompts:
    llm_path = broker.clean_cot(str(response_basic))
  else:
    raise Exception("Error: Failed to clean response, prompt path not found in prompt types")


  simulation.view_paths(llm_path, INDEX)


def test_llm(prompt):
  broker = rh()

  response_basic = broker.ask_gemini(prompt)

  print ("LLM Response: "+str(response_basic))


def run_test(n_mazes, size, repeats, supplier, model, prompt, shots, temperature, reflexion, debug, random_max=25):
  broker = rh(model = model, prompt = prompt, temperature=temperature)
  test_mazes = Maze(size,n_mazes)

  simulation = Visualizer(test_mazes)

  return tm.test(test_mazes, repeats, simulation, broker, supplier=supplier, prompt_file=prompt, shots=shots, reflexion=reflexion, debug=debug, random_max=random_max)


#supplier = "openai", "google"
#model = "gpt-3.5-turbo-0613", "gpt-3.5-turbo-0125", "gpt-4" | "gemini-1.0-pro"
#shots = 0,1,2,3,4,5

#run_single(index=1,size=5, supplier = "openai", model = "gpt-3.5-turbo-0125", prompt = "system_prompt_cot.txt", reflexion=False)


test_score, gpt_total_moves, random_total_moves, opt_moves_model, opt_moves_random, rand_score = run_test(n_mazes=100, size=5, repeats=1, supplier = "google", model = "gpt-3.5-turbo-0125", prompt = "system_prompt_basic.txt", shots=0, temperature=0.0,reflexion=False, debug=False)

print("\n")

print("Solve rate: "+str(round(test_score,2))+"%")
print("Random solve rate: "+str(round(rand_score,2))+"%")

print("\n")

print("extra LLM moves: "+ str(gpt_total_moves - opt_moves_model))
print("extra random moves: "+ str(random_total_moves - opt_moves_random))

print("\n")


#test_llm("what is the meaning of life?")
#response_basic_fake = "Start (1,3), next move (1,4), next move (4,3), next move (4,4), End (2,3)"
#gpt_path_fake = [(1,3),(0,3),(0,2),(1,2),(2,2),(2,1), (2,0), (3,0), (4,0), (4,1), (4,2), (4,3), (4,4), (3,4), (2,4), (2,3)]





