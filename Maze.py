import random as r
from zanj import ZANJ

from maze_dataset import MazeDataset, MazeDatasetConfig, LatticeMazeGenerators, SolvedMaze

class Maze:
  def __init__(self, size, number):
    self.CFG: MazeDatasetConfig = MazeDatasetConfig(
      name="test",
      grid_n=size, #5
      n_mazes=number, #5
      maze_ctor=LatticeMazeGenerators.gen_dfs,
    )

  

  def get_dataset(self):
     DATASET: MazeDataset = MazeDataset.from_config(self.CFG, local_base_path="mazes/")
     return DATASET
