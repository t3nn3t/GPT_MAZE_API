

class TestManager:

    def test(mazes, repeats, simul, broker, supplier):
        maze_dataset = mazes.get_dataset()
        solved = 0
        llm_moves = 0
        random_moves = 0
        optimal_moves = 0
        total = len(maze_dataset) * repeats

        for i in range(0,repeats):
            for index in range(0, len(maze_dataset)):
                print("Mazes done: "+str(((i*len(maze_dataset))+index))+"/"+str(total))

                llm_adjlist = mazes.get_adjlist_nopath(maze_dataset[index])
                optimal_path = mazes.get_best_path(maze_dataset[index])

                prompt_path = str(llm_adjlist)


                if str.lower(supplier)=="openai":
                    llm_response_basic = broker.ask_gpt(prompt_path)
                elif str.lower(supplier)=="google":
                    llm_response_basic = broker.ask_gemini(prompt_path)
                else:
                    raise Exception("Error: Supplier not recognised")
                
                
                llm_path = broker.clean_adv(str(llm_response_basic))
                #gpt_path = broker.clean_cot(str(gpt_response_basic))
                #gpt_path = broker.clean_quoted(str(gpt_response_basic))


                random_result = simul.check_random(index, 50)
                result = simul.check_paths(llm_path, index)

                if result > 0:
                    solved += 1
                    llm_moves += result
                    random_moves += random_result
                    optimal_moves += optimal_path
                print("solved: "+ str(solved))
                

        
        
        print("total: " +str(total))
        print("sovled: "+ str(solved))

        score = (solved/total) * 100

        return score, llm_moves, random_moves, optimal_moves
    

     