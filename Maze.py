import random as r
from zanj import ZANJ
import re

from maze_dataset import MazeDataset, MazeDatasetConfig, LatticeMazeGenerators, SolvedMaze
from maze_dataset.tokenization import MazeTokenizer, TokenizationMode

class Maze:
  def __init__(self, size, number):
    self.size = size
    self.CFG: MazeDatasetConfig = MazeDatasetConfig(
      name="test",
      grid_n=size, #5
      n_mazes=number, #5
      maze_ctor=LatticeMazeGenerators.gen_dfs,
    )

  

  def get_dataset(self):
     DATASET: MazeDataset = MazeDataset.from_config(self.CFG, local_base_path="mazes/")
     return DATASET
  
  def get_adjlist(self, maze):
    
    tokenizer: MazeTokenizer = MazeTokenizer(tokenization_mode=TokenizationMode.AOTP_UT_rasterized, max_grid_size=100)
    maze_tok = maze.as_tokens(maze_tokenizer=tokenizer)

    return (" ".join(maze_tok))
  
  def get_adjlist_nopath(self, maze):

    adjlist = self.get_adjlist(maze)
    adjlist = re.sub(r'<PATH_START>.*?<PATH_END>', '', adjlist)
    return adjlist
  
  def get_size(self):
    return self.size
