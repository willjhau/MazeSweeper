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

# Create defult difficulties
EASY_DIFFICULTY = gameParameters(x = 9, y = 9, mines = 10)
MEDIUM_DIFFICULTY = gameParameters(x = 16, y = 16, mines = 40)
EXPERT_DIFFICULTY = gameParameters(x = 30, y = 16, mines = 99)


class mazeGenerator:
    def __init__(self, width, height, difficulty):
        self.width = width
        self.height = height
        self.maze = [[0 for i in range(width)] for j in range(height)]