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
    self.DATASET: MazeDataset = MazeDataset.from_config(self.CFG, local_base_path="mazes/")
    self.tokenizer: MazeTokenizer = MazeTokenizer(tokenization_mode=TokenizationMode.AOTP_UT_rasterized, max_grid_size=100)

  

  def get_dataset(self):
     return self.DATASET
  
  def get_size(self):
    return self.size
  
  def get_adjlist(self, maze):
    
    
    
    maze_tok = maze.as_tokens(maze_tokenizer=self.tokenizer)

    
    return (" ".join(maze_tok))
  
  
  def get_adjlist_nopath(self, maze):
    adjlist = self.get_adjlist(maze)
    
    adjlist = re.sub(r'<PATH_START>.*?<PATH_END>', '', adjlist)

    adjlist = self.update_adjacency_list(adjlist)
    
    return adjlist
  
  
  def update_adjacency_list(self,input_string):
    # Split the input string into parts
    adj_list_start = "<ADJLIST_START>"
    adj_list_end = "<ADJLIST_END>"
    origin_start = "<ORIGIN_START>"
    origin_end = "<ORIGIN_END>"
    target_start = "<TARGET_START>"
    target_end = "<TARGET_END>"

    adj_list_str = input_string.split(adj_list_start)[1].split(adj_list_end)[0].strip()
    origin_str = input_string.split(origin_start)[1].split(origin_end)[0].strip()
    target_str = input_string.split(target_start)[1].split(target_end)[0].strip()

    # Process the adjacency list
    edges = [edge.strip() for edge in adj_list_str.split(";")]

    # Create a set to store unique edges
    unique_edges = set()

    # Update the adjacency list with both forward and backward edges
    for edge in edges:
        # Use regular expression to extract integer values between parentheses
        edge_tuple = tuple(map(int, re.findall(r'\d+', edge)))

        # Check if edge_tuple has enough elements
        if len(edge_tuple) >= 4:
            forward_edge = f"({edge_tuple[0]},{edge_tuple[1]}) <--> ({edge_tuple[2]},{edge_tuple[3]})"
            backward_edge = f"({edge_tuple[2]},{edge_tuple[3]}) <--> ({edge_tuple[0]},{edge_tuple[1]})"
            unique_edges.add(forward_edge)
            unique_edges.add(backward_edge)

    # Build the updated adjacency list string
    updated_adj_list = f"{adj_list_start} {' ; '.join(unique_edges)} {adj_list_end}"

    # Build the final output string
    output_string = f"{updated_adj_list} {origin_start} {origin_str} {origin_end} {target_start} {target_str} {target_end}"

    return output_string


  
  def get_adjacency_dict(self, maze):

    input_string = self.get_adjlist_nopath(maze)

    # Extracting adjacency list from the input string
    adj_list_match = re.search(r'<ADJLIST_START>(.*?)<ADJLIST_END>', input_string, re.DOTALL)
    if adj_list_match:
        adjacency_list = adj_list_match.group(1).strip()
    else:
        raise ValueError("No adjacency list found in the input string.")

    # Creating a dictionary to store the possible moves
    moves_dict = {}

    # Parsing the adjacency list
    edges = re.findall(r'\((\d+,\d+)\) <--> \((\d+,\d+)\)', adjacency_list)
    for edge in edges:
        source, target = edge
        if source not in moves_dict:
            moves_dict[source] = []
        moves_dict[source].append(target)

    return moves_dict
      

  def get_size(self):
      return self.size
