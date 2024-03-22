# LLM Maze Solving Benchmark

## Overview
This project is designed to integrate maze-solving capabilities with language models from OpenAI and potentially other providers. It uses various prompts and language models to generate solutions for mazes, visualizes these solutions, and compares them to optimal and random paths.

## Key Components
- **Maze Generation:** Generate mazes of specified sizes.
- **Language Model Integration:** Utilize OpenAI's and Google Gemini Pro language models to solve mazes.
- **Visualization:** Visualize the model's path against the optimal path.
- **Testing and Evaluation:** Test the language model's maze-solving capabilities against random and optimal solutions.

## Prerequisites
- Python 3
- `openai` Python package for OpenAI GPT
- `vertexai` Python package for Google Gemini 
- `maze-dataset` Python package for generating maze files
- `matplotlib` Python package for visualising maze paths
- `zanj` Python package for storing maze files
- Custom modules: `Maze`, `Maze_generator`, `Visualizer`, `Response_handler`, `TestManager`

## Installation
1. Clone the repository or download the project files.
2. Ensure Python 3.x is installed on your system.
3. Install the prequisites Python package using pip:
   ```
   pip install <Prerequisite package>
   ```

## Usage
The project's main functionalities are the Visualisation (`run_single`) and the Test (`run_test`) functions.

### Running the Visualiser
To run a simulation with a visualiser, use the `run_single` function:

```python
run_single(index, size, supplier, model, prompt, reflexion=False, debug=True)
```

- `index`: Index of the maze to solve within the generated dataset of 121 mazes (0-120)
- `size`: Size of the maze to use (3: 3x3, 4: 4x4, 5: 5x5...)
- `supplier`: Language model provider ("openai", "google")
- `model`: Specific language model to use ("gpt-3.5-turbo-0125", "gpt-3.5-turbo-0613", "gpt-4", "gemini-1.0-pro")
- `prompt`: The prompt file to use for querying the model ("system_prompt_" + "basic", "cot", "stepback")
- `self_refine`: Enable or disable self reflection, default is `False`
- `debug`: Enable or disable debug mode to output responses in terminal, default is `True`

### Running Tests
To evaluate the language model's performance over multiple mazes, use the `run_test` function:

```python
run_test(n_mazes, size, repeats, supplier, model, prompt, shots, temperature, reflexion, debug)
```

- `n_mazes`: Number of mazes to generate for the test.
- `size`: Size of each maze (3: 3x3, 4: 4x4, 5: 5x5...)
- `repeats`: Number of times to run the test. (repeat=1) will run through once
- `supplier`: Language model provider ("openai", "google")
- `model`: Specific language model to use ("gpt-3.5-turbo-0125", "gpt-3.5-turbo-0613", "gpt-4", "gemini-1.0-pro")
- `prompt`: The prompt file to use ("system_prompt_" + "basic", "cot", "stepback")
- `shots`: Number of examples used in the prompt for the language model (0-5) (note: only avaliable for maze size 3-5)
- `temperature`: Temperature setting for the language model Google: (0.0-1.0) OpenAI: (0.0 - 2.0)
- `reflexion`: Enable or disable reflexion mode
- `debug`: Enable or disable debug mode
- `random_max`: Maximum moves afforded to the random agent (default=25)

## Output

Running the visualiser will open a pop up window using MatPlotLib. This window will display a maze with the optimal path as well as the path given my the model.

Running tests will return the solve rate of the model, the solve rate of a random agent, the extra moves used by the model over the optimal solution, and the extra moves used by the random agent over the optimal solution

If `debug` is enable the prompts sent to the model aswell as the reponses from the model will be printed in the terminal.

## Example
Here's an example of running a test with the project:

```python
test_score, gpt_total_moves, random_total_moves, opt_moves_model, opt_moves_random, rand_score = run_test(
    n_mazes=100, 
    size=5, 
    repeats=1, 
    supplier="openai", 
    model="gpt-3.5-turbo-0125", 
    prompt="system_prompt_basic.txt", 
    shots=0, 
    temperature=1.0,
    reflexion=False, 
    debug=False
)

print("Solve rate: " + str(round(test_score, 2)) + "%")
print("Random solve rate: " + str(round(rand_score, 2)) + "%")
print("Extra LLM moves: " + str(gpt_total_moves - opt_moves_model))
print("Extra random moves: " + str(random_total_moves - opt_moves_random))
```

This script will run a maze-solving test using the OpenAI GPT-3.5 0125 model and provide its performance metrics 

## Adding Your Own Models
