import re

class TestManager:

    def test(mazes, repeats, simul, broker, supplier, prompt_file, shots, reflexion, debug):

        maze_dataset = mazes.get_dataset()
        maze_size = mazes.get_size()
        solved = 0
        llm_moves = 0
        random_moves = 0
        optimal_moves = 0
        total = len(maze_dataset) * repeats

        e = open("examples_prefix.txt", "r")
        examples_prefix = e.read()

        #prompt files
        basic_prompts = ["system_prompt_astar.txt", "system_prompt_basic.txt", "system_prompt_printfirst.txt"]
        cot_prompts = ["system_prompt_cot.txt"]
        quoted_prompts = [""]

        #prompt type
        pattern = r"system_prompt_(.*?)\.txt"
        prompt_type = re.search(pattern, prompt_file).group(1)

        for i in range(0,repeats):
            for index in range(0, len(maze_dataset)):
                print("Mazes done: "+str(((i*len(maze_dataset))+index))+"/"+str(total))

                llm_adjlist = mazes.get_adjlist_nopath(maze_dataset[index])
                optimal_path = mazes.get_best_path(maze_dataset[index])

                prompt_path = str(llm_adjlist)

                examples = ""
                for x in range (1,shots+1):
                    if (x==1):
                        examples += (examples_prefix+"\n")
                    f = open(("fewshot_examples/"+str(maze_size)+"x"+str(maze_size)+"_examples_"+str(prompt_type)+"/example_"+str(x)+".txt"), "r")
                    example = f.read()
                    examples += ("\n"+example+"\n\n")

                if str.lower(supplier)=="openai":
                    llm_response_basic = broker.ask_gpt(prompt_path, examples, reflexion, debug)
                elif str.lower(supplier)=="google":
                    llm_response_basic = broker.ask_gemini(prompt_path, examples, debug)
                else:
                    raise Exception("Error: Supplier not recognised")
                

                if prompt_file in basic_prompts:
                    llm_path = broker.clean_adv(str(llm_response_basic))
                elif prompt_file in cot_prompts:
                    llm_path = broker.clean_cot(str(llm_response_basic))
                elif prompt_file in quoted_prompts:
                    llm_path = broker.clean_quoted(str(llm_response_basic))
                else:
                    raise Exception("Error: Failed to clean response, prompt path not found in prompt types")
                
                print("CLEANED PATH")
                print(llm_path)


                random_result = simul.check_random(index, 50)
                result = simul.check_paths(llm_path, index)

                if result > 0:
                    solved += 1
                    llm_moves += result
                    random_moves += random_result
                    optimal_moves += optimal_path
                print("Mazes solved: "+ str(solved))
                
        print("")
        print("total: " +str(total))
        print("sovled: "+ str(solved))

        score = (solved/total) * 100

        return score, llm_moves, random_moves, optimal_moves
    

     