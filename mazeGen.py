import constants as c
import random
from icecream import ic
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
# Generates a maze to be saved as an image

# Object containing all the information to construct a maze
class gameParameters:
    def __init__(self, x:int, y:int, mines:int = None, mineRatio:float = None, destroyWallRatio:float = 0.2, powerupCost = 0):
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
        self.destroyWallRatio = destroyWallRatio
        self.powerupCost = powerupCost
        if mines != None:
            self.mines = mines
        elif mineRatio != None:
            self.mineRatio = mineRatio
            self.mines = int(x * y * mineRatio)
        self.mineRatio = mineRatio
    
    def getMineRatio(self):
        return self.mineRatio
    
    def setMineRatio(self, ratio: float):
        self.mineRatio = ratio
        self.mines = int(self.x * self.y * ratio)
    
    def getDestroyWallRatio(self):
        return self.destroyWallRatio
    
    def setDestroyWallRatio(self, ratio: float):
        self.destroyWallRatio = ratio

    def __str__(self):
        return "x (width): " + str(self.x) + ",\ny (height): " + str(self.y) + ",\nmines: " + str(self.mines)

class Square:
    def __init__(self, isWall = True, isMine = False, isStart = False, 
    isEnd = False):
        self.isWall = isWall
        self.isMine = isMine and not isWall
        self.isStart = False
        self.isEnd = False

    def encodeSteganography(self, bin:str):
        # If the square is the start, make the last 3 bits 100
        # If the square is the end, make the last 3 bits 010
        # If the square is a wall, make the last 3 bits 001
        # If the square is not a wall, make the last 3 bits 000
        if self.isStart:
            return ic(f"{bin[:-3]}100")
        elif self.isEnd:
            return ic(f"{bin[:-3]}010")
        elif self.isWall:
            return f"{bin[:-3]}001"
        else:
            return f"{bin[:-3]}000"
        
    def decodeSteganography(self, bin:str):
        # If the last 3 bits are 100, the square is the start
        # If the last 3 bits are 010, the square is the end
        # If the last 3 bits are 001, the square is a wall
        # If the last 3 bits are 000, the square is not a wall
        if bin[-3:] == "100":
            self.isStart = ic(True)
        elif bin[-3:] == "010":
            self.isEnd = ic(True)
        elif bin[-3:] == "001":
            self.isWall = True
        else:
            self.isWall = False

    def makeStart(self):
        self.isStart = True

    def makeEnd(self):
        self.isEnd = True

    def makeWall(self):
        self.isWall = True
    
    def carveWall(self):
        self.isWall = False
    
    def makeMine(self):
        self.isMine = True
    
    def removeMine(self):
        self.isMine = False
    
    def getColour(self):        
        if self.isStart:
            return [0, 255, 0]
        elif self.isEnd:
            return [0, 0, 255]
        elif self.isWall:
            return [0, 0, 0]
        elif self.isMine:
            return [255, 0, 0]

        else:
            return [255, 255, 255]



class Maze:
    def __init__(self, params):
        self.params = params
        self.maze = [[Square() for i in range(params.x)] for j in range(params.y)]
        self.wallList = []
        self.passageList = []
        self.nonPassageList = [(i, j) for i in range(params.x) for j in range(params.y)]
        self.startPoint = None
        self.endPoint = None
    
    def adjacentSquares(self, x, y):
        # Returns a list of the coordinates of the adjacent squares
        template = (
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1)
        )
        return [(a, b) for (a, b) in template if a >= 0 and a < self.params.x and b >= 0 and b < self.params.y]
    
    def immediateAdjacent(self, x, y):
        template = (
            (x, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x, y + 1)

        )
        return [(a, b) for (a, b) in template if a >= 0 and a < self.params.x and b >= 0 and b < self.params.y]


    def generateMazeFromParams(self):
        # Implements the Randomized Prim's algorithm
        for row in self.maze:
            for square in row:
                square.makeWall()
        
        # Choose a random starting point
        x = random.randint(0, self.params.x - 1)
        y = random.randint(0, self.params.y - 1)
        self.maze[y][x].carveWall()
        self.passageList.append((x, y))
        self.nonPassageList.remove((x, y))
        self.maze[y][x].makeStart()

        self.startPoint = (x, y)

        # Add the adjacent squares to the wall list
        self.wallList.extend(self.immediateAdjacent(x, y))

        # While there are still walls to be carved
        while len(self.wallList) > 0:
            # Choose a random wall
            wall = random.choice(self.wallList)
            # Get the adjacent squares
            adjacent = self.immediateAdjacent(wall[0], wall[1])
            # Count the number of adjacent squares that are walls
            passageCount = 0
            for square in adjacent:
                if not self.maze[square[1]][square[0]].isWall:
                    passageCount += 1
            # If there are 2 or more adjacent walls, carve the wall
            if passageCount == 1:
                self.maze[wall[1]][wall[0]].carveWall()
                self.passageList.append(wall)
                self.nonPassageList.remove(wall)
                self.wallList.remove(wall)
                # Add the adjacent squares to the wall list
                adjacent = [w for w in self.immediateAdjacent(wall[0], wall[1]) if w not in self.wallList and self.maze[w[1]][w[0]].isWall]
                self.wallList.extend(adjacent)
            else:
                self.wallList.remove(wall)
            
        # Choose a random end point that is not a wall and is not the starting point or if the point is less than half of the maze away from the start
        x = random.randint(0, self.params.x - 1)
        y = random.randint(0, self.params.y - 1)

        while self.maze[y][x].isWall or self.maze[y][x].isStart or (abs(x - self.startPoint[0]) < self.params.x / 2 or abs(y - self.startPoint[1]) < self.params.y / 2):
            x = random.randint(0, self.params.x - 1)
            y = random.randint(0, self.params.y - 1)

        self.maze[y][x].makeEnd()
        self.endPoint = (x, y)

        # Choose a number of random walls to destroy
        random.shuffle(self.nonPassageList)
        destroyCount = int(len(self.nonPassageList) * self.params.destroyWallRatio)
        for i in range(destroyCount):
            (x ,y) = self.nonPassageList.pop()
            self.maze[y][x].carveWall()
            self.passageList.append((x, y))


        self.saveMazeAsImage("maze")

        self.showMaze()
        
    
    def saveMazeAsImage(self, imageName):
        # Create a 2D array noise the size of the maze, stored as a string of binary
        out = np.zeros((self.params.y, self.params.x))
        for i, row in enumerate(self.maze):
            for j, square in enumerate(row):
                noiseV = random.randint(0, 255)
                noiseV = f"{noiseV:08b}"
                encoded = square.encodeSteganography(noiseV)
                out[i][j] = int(encoded, 2)
        cv2.imwrite(os.path.join(c.MAZE_SAVE_DIR,f"{imageName}.png"), out)

    def loadMazeFromImage(self, imageName):
        # Load the image then decode the maze
        image = cv2.imread(os.path.join(c.MAZE_SAVE_DIR,f"{imageName}.png"), cv2.IMREAD_GRAYSCALE)
        for i, row in enumerate(image):
            for j, pixel in enumerate(row):
                # convert this to binary
                pixel = f"{pixel:08b}"
                self.maze[i][j].decodeSteganography(pixel)
        
        self.showMaze()
        
    
    def showMaze(self):
        image = [s.getColour() for row in self.maze for s in row]
        image = np.array(image)
        image = image.reshape(self.params.y, self.params.x, 3)
        plt.imshow(image)
        plt.show()

    


def main():
    maze = Maze(c.INTERMEDIATE)
    maze.generateMazeFromParams()
    input()
    maze.loadMazeFromImage('maze')

if __name__ == "__main__":
    main()