# Generates a maze to be saved as an image

# Constants mapping cardinal directions to numbers
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# Object containing all the information to construct a maze
class gameParameters:
    def __init__(self, x:int, y:int, mines:int = None, mineRatio:float = None):
        # Check for valid input
        if type(x) != int or type(y) != int:
            raise ValueError("x and y must be integers")
        if x < 1 or y < 1:
            raise ValueError("x and y must be positive")
        if mines != None and mineRatio != None:
            raise ValueError("Only one of mines and mineRatio can be specified")
        if mines is None and mineRatio is None:
            raise ValueError("Either mines or mineRatio must be specified")

        self.x = x
        self.y = y
        if mines != None:
            self.mines = mines
        elif mineRatio != None:
            self.mineRatio = mineRatio
            self.mines = int(x * y * mineRatio)
        self.mineRatio = mineRatio

    def __str__(self):
        return "x (width): " + str(self.x) + ",\ny (height): " + str(self.y) + ",\nmines: " + str(self.mines)

# Create defult difficulties
EASY_DIFFICULTY = gameParameters(x = 9, y = 9, mines = 10)
MEDIUM_DIFFICULTY = gameParameters(x = 16, y = 16, mines = 40)
EXPERT_DIFFICULTY = gameParameters(x = 30, y = 16, mines = 99)

class Maze:
    def __init__(self, params):
        self.params = params
        self.maze = [[Square() for i in range(params.x)] for j in range(params.y)]


class Square:
    def __init__(
        self,
        north = True,
        east = True,
        south = True,
        west = True,
        mine = False
        ):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
    
    def makeMine(self):
        self.mine = True
    
    def __str__(self):
        return f"north: {self.north},\neast: {self.east},\nsouth: {self.south},\nwest: {self.west},\nmine: {self.mine}"