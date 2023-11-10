import mazeGen
import os

#Level details for the standard levels
BEGINNER = mazeGen.gameParameters(x = 9, y = 9, mines = 10)

INTERMEDIATE = mazeGen.gameParameters(x = 16, y = 16, mines = 40)

EXPERT = mazeGen.gameParameters(x = 30, y = 16, mines = 99)

#Constants for the dimensions of the buttons in the header of the screen
WIDE_BUTTON_WIDTH = 80
TOP_BUTTON_HEIGHT = 40

#Constants for the gaps between items
SPACING = 10
SEPARATOR = 2

#Set the size of each game square
SQUARE_SIZE = 30

#Define the colours of the different features
BUTTON_GREY = (200, 200, 200)
BUTTON_YELLOW = (160, 160, 0)
BACKGROUND = (255, 255, 255)
HIDDEN_COLOR = (180, 180, 180)
REVEALED_COLOR = (230, 230, 230)
MINE_COLOR = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)
COMPLETE_COLOR = (0, 255, 0)

#Directory names
ASSETS_DIR = 'Assets'
MAZE_SAVE_DIR = 'Mazes'

#Filenames/paths for the images required
FLAG_PATH = os.path.join(ASSETS_DIR, 'flag.png')
MINE_PATH = os.path.join(ASSETS_DIR, 'mine.png')
FACE_PATH = os.path.join(ASSETS_DIR, 'face.png')

#Speed of the agent
DELAY = 1

# Constants mapping cardinal directions to numbers
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3