from Visualizer import Visualizer

class TestManager:

    def test(maze_dataset, repeats, simul, broker):
        solved = 0
        total = len(maze_dataset) * repeats

        
        for index in range(0, len(maze_dataset)):
            gpt_path = 0
            prompt=""
            response_basic = broker.ask_gpt(prompt)
            simul.check_paths(gpt_path, index)

        



        score = (solved/total) * 100

        return score