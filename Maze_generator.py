
import matplotlib.pyplot as plt # keep this import for CI to work
from zanj import ZANJ # saving/loading data
from muutils.mlutils import pprint_summary # pretty printing as json

# maze_dataset imports
from maze_dataset import LatticeMaze, SolvedMaze, MazeDataset, MazeDatasetConfig
from maze_dataset.generation import LatticeMazeGenerators, GENERATORS_MAP
from maze_dataset.generation.default_generators import DEFAULT_GENERATORS
from maze_dataset.dataset.configs import MAZE_DATASET_CONFIGS
from maze_dataset.plotting import plot_dataset_mazes, print_dataset_mazes


from maze_dataset.plotting import MazePlot
from maze_dataset.tokenization import MazeTokenizer, TokenizationMode
from maze_dataset.plotting.print_tokens import display_color_maze_tokens_AOTP, color_maze_tokens_AOTP
from maze_dataset.dataset.rasterized import process_maze_rasterized_input_target

"""
 Code adapted from https://pypi.org/project/maze-dataset/0.4.5/
 maze-dataset 0.4.5
 v 0.4.5
 Dec 5, 2023
"""

# check the configs
print(MAZE_DATASET_CONFIGS.keys())
# for saving/loading things
LOCAL_DATA_PATH: str = "mazes/"
zanj: ZANJ = ZANJ(external_list_threshold=256)


cfg: MazeDatasetConfig = MazeDatasetConfig(
	name="test_002", # name is only for you to keep track of things
	grid_n=6, # number of rows/columns in the lattice
	n_mazes=4, # number of mazes to generate
	maze_ctor=LatticeMazeGenerators.gen_dfs, # algorithm to generate the maze
    # there are a few more arguments here, to be discussed later
)

# each config will use this function to get the name of the dataset
# it contains some basic info about the algorithm, size, and number of mazes
# at the end after "h" is a stable hash of the config to avoid collisions
print(cfg.to_fname())


# to create a dataset, just call MazeDataset.from_config
dataset: MazeDataset = MazeDataset.from_config(cfg,local_base_path=LOCAL_DATA_PATH, do_generate=False)

#plot_dataset_mazes(dataset, count=None) # for large datasets, set the count to some int to just plot the first few



maze: SolvedMaze = dataset[0]

# first, initialize a tokenizer -- more about this in the `notebooks/demo_tokenization.ipynb` notebook
tokenizer: MazeTokenizer = MazeTokenizer(tokenization_mode=TokenizationMode.AOTP_UT_rasterized, max_grid_size=100)
maze_tok = maze.as_tokens(maze_tokenizer=tokenizer)

# you can view the tokens directly
print("\nRaw tokens:\n")
print(" ".join(maze_tok))

print("\nColored tokens, raw html:\n")
print(color_maze_tokens_AOTP(maze_tok, fmt="html"))



