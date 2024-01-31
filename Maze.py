import random as r

class Maze:
  def __init__(self, size):
    self.size = size
    coordinates = self.get_coords(2)
    self.start = coordinates[0]
    self.exit = coordinates[1]
    self.ai = self.start

  def update_maze(position):
    return 0


  def get_coords(self, amount):
    coords = []
    for n in range (0,amount):
        #get random ints within size
        point = (r.randint(0, self.size-1), r.randint(0, self.size-1))
        while (point in coords):
            point = (r.randint(0, self.size-1), r.randint(0, self.size-1))
        coords.append(point)
    return coords
  

  def print_maze(self):
    for y in range (self.size-1,-1,-1):
        for x in range (0,self.size):
            if (self.start==(x,y)):
                print("S ", end="")
            elif (self.exit==(x,y)):
                print("E ", end="")
            else:
                print("# ", end="")
        print("")
