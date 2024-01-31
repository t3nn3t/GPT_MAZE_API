import random as r
from openai import OpenAI
from Maze import Maze


client = OpenAI()

f = open("maze_instruction_v1.1", "r")
instruction = f.read()


def ask_gpt(question):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": instruction},
      {"role": "user", "content": question}
    ]
  )
  return completion.choices[0].message


def get_ai_moves(answer):
  moves = []
  return moves


def ai_solve_maze(maze):
  print("Starting maze solve...")
  print("start: ",maze.start)
  print("exit: ",maze.start)
  #print_maze(maze.size, maze.start, maze.exit)

  print("getting ai moves...")
  moves = get_ai_moves(maze)
  #for move in moves:


      
  
maze_size = int(input("Size of the square maze? (eg.'5' -> (5x5): "))


test_maze = Maze(maze_size)

print("Solve the following maze: Your Starting coordinate is",test_maze.start,". Your Exit coordinate is",test_maze.exit,". The Size of the maze is",test_maze.size,".")

test_maze.print_maze()

print(instruction)









