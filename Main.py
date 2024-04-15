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
def run_single(index, size, supplier, model, prompt, self_refine=False, debug=True):

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
    response_basic = broker.ask_gpt(prompt_path, self_refine=self_refine, debug=debug)
  elif str.lower(supplier)=="google":
    response_basic = broker.ask_gemini(prompt_path,self_refine=self_refine, debug=debug)
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


def run_test(n_mazes, size, repeats, supplier, model, prompt, shots, temperature, self_refine, debug, random_max=20):
  broker = rh(model = model, prompt = prompt, temperature=temperature)
  test_mazes = Maze(size,n_mazes)

  simulation = Visualizer(test_mazes)

  return tm.test(test_mazes, repeats, simulation, broker, supplier=supplier, prompt_file=prompt, shots=shots, self_refine=self_refine, debug=debug, random_max=random_max)


#supplier = "openai", "google"
#model = "gpt-3.5-turbo-0613", "gpt-3.5-turbo-0125", "gpt-4" | "gemini-1.0-pro"
#shots = 0,1,2,3,4,5

#run_single(index=3,size=4, supplier = "openai", model = "gpt-3.5-turbo-0125", prompt = "system_prompt_cot.txt", self_refine=False)


#test_score, gpt_total_moves, random_total_moves, opt_moves_model, opt_moves_random, rand_score = run_test(n_mazes=100, size=4, repeats=1, supplier = "openai", model = "gpt-3.5-turbo-0613", prompt = "system_prompt_cot.txt", shots=2, temperature=0.2,self_refine=True, debug=True)
test_score2, gpt_total_moves2, random_total_moves2, opt_moves_model2, opt_moves_random2, rand_score2 = run_test(n_mazes=100, size=4, repeats=1, supplier = "google", model = "gemini-1.5-pro-preview-0409", prompt = "system_prompt_cot.txt", shots=0, temperature=0.0,self_refine=False, debug=True)
#test_score3, gpt_total_moves3, random_total_moves3, opt_moves_model3, opt_moves_random3, rand_score3 = run_test(n_mazes=100, size=4, repeats=1, supplier = "openai", model = "gpt-4-0125-preview", prompt = "system_prompt_cot.txt", shots=2, temperature=0.2,self_refine=True, debug=False)
#print("extra LLM moves: "+ str(gpt_total_moves - opt_moves_model))
#test_score4, gpt_total_moves4, random_total_moves4, opt_moves_model4, opt_moves_random4, rand_score4 = run_test(n_mazes=100, size=4, repeats=1, supplier = "google", model = "gemini-1.0-pro", prompt = "system_prompt_basic.txt", shots=0, temperature=0.0,self_refine=True, debug=True)
#test_score5, gpt_total_moves5, random_total_moves5, opt_moves_model5, opt_moves_random5, rand_score5 = run_test(n_mazes=100, size=4, repeats=1, supplier = "google", model = "gemini-1.0-pro", prompt = "system_prompt_basic.txt", shots=0, temperature=0.0,self_refine=True, debug=False)

print("\n")
#print("Solve rate 1: "+str(round(test_score,2))+"%")
#print("extra LLM moves 1: "+ str(gpt_total_moves - opt_moves_model))


print("\n")

print("Solve rate 2: "+str(round(test_score2,2))+"%")
print("extra LLM moves 2: "+ str(gpt_total_moves2 - opt_moves_model2))


print("\n")

#print("Solve rate 3: "+str(round(test_score3,2))+"%")
#print("extra LLM moves 3: "+ str(gpt_total_moves3 - opt_moves_model3))


print("\n")

#print("Solve rate 4: "+str(round(test_score4,2))+"%")
#print("extra LLM moves 4: "+ str(gpt_total_moves4 - opt_moves_model4))

print("\n")

#print("Solve rate 5: "+str(round(test_score5,2))+"%")
#print("extra LLM moves 5: "+ str(gpt_total_moves5 - opt_moves_model5))

print("\n")

#print("random solve rate: "+str(round(rand_score4,2))+"%")
#print("random extra moves: "+ str(random_total_moves4- opt_moves_random4))

print("\n")

#print("random solve rate: "+str(round(rand_score3,2))+"%")
#print("random extra moves: "+ str(random_total_moves3- opt_moves_random3))

print("\n")



#test_llm("what is the meaning of life?")
#response_basic_fake = "Start (1,3), next move (1,4), next move (4,3), next move (4,4), End (2,3)"
#gpt_path_fake = [(1,3),(0,3),(0,2),(1,2),(2,2),(2,1), (2,0), (3,0), (4,0), (4,1), (4,2), (4,3), (4,4), (3,4), (2,4), (2,3)]





