#Level details for the standard levels
BEGINNER = {
    'rows': 9,
    'columns': 9,
    'mines':9
}

INTERMEDIATE = {
    'rows': 16,
    'columns': 16,
    'mines':40    
}

EXPERT = {
    'rows': 16,
    'columns': 30,
    'mines':99
}

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

#Filenames/paths for the images required
FLAG_PATH = 'flag.png'
MINE_PATH = 'mine.png'
FACE_PATH = 'face.png'

#Speed of the agent
DELAY = 1