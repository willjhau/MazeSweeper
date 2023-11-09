import constants
import square
import random

class Board():
    """
    This class allows the game instance to easily access all the information that might be needed during execution.

    It uses a 2D array for Square objects to collate all information within the board instance.
    """
    def __init__(self, difficulty):
        self.DIFFICULTY = difficulty # The difficulty can be inputted as a dictionary containing the mines, rows, and columns
                                     # or as a string of a preset
        if type(difficulty) == str:  # Checks the valid string preset names
            if difficulty.upper() == "BEGINNER":
                difficulty = constants.BEGINNER
            elif difficulty.upper() == "INTERMEDIATE":
                difficulty = constants.INTERMEDIATE
            elif difficulty.upper() == "EXPERT":
                difficulty = constants.EXPERT
        
        # Initialise the attributes
        self.isComplete = False
        self.ROWS = difficulty['rows']
        self.COLS = difficulty['columns']
        self.MINES = difficulty['mines']
        self.flags = 0

        # Create the board attribute of Square objects
        self.board = [[square.Square(r, c) for c in range(self.COLS)] for r in range(self.ROWS)]
    
    def getDifficulty(self):
        return self.DIFFICULTY
    
    def addFlag(self):
        self.flags += 1

    def removeFlag(self):
        self.flags -= 1

    def getCols(self):
        return self.COLS

    def getRows(self):
        return self.ROWS

    def getMines(self):
        return self.MINES

    # Randomly adds mines to the board object, excluding the starting position
    def addMines(self, n, excludeIndex):
        allIndices = [(r,c) for c in range(self.COLS) for r in range(self.ROWS) if (r,c) != excludeIndex] # This holds all valid mine squares
        random.shuffle(allIndices) # Randomise the list
        for r,c in allIndices[:self.MINES]: # Then truncate the list to the correct length and make mines
            self.board[r][c].makeMine()
        for row in self.board:
            for sq in row:
                sq.calculateValue(self) # Now update each squares adjacent mine value

    # Displays in the console all the visible information in ASCII form
    def displayTerminal(self):
        for row in self.board:
            line = ''
            for sq in row:
                if sq.isVisible():
                    line = f'{line} {sq.getValue()}'
                elif sq.isFlag():
                    line = f'{line} F'
                else:
                    line = f'{line}  '
            print(line)
    
    # Displays in the console ALL information in ASCII form - for use in development
    def displayAllTerminal(self):
        for row in self.board:
            line = ''
            for sq in row:
                if sq.isMine():
                    line = f'{line} X'
                else:
                    line = f'{line} {sq.getValue()}'
            print(line)
    
    # Reveals a square
    # Input is a list of indices as multiple squares may be revealed by a single click
    def reveal(self, indices):
        index = indices[0]
        if not self.board[index[0]][index[1]].isFlag() and not self.board[index[0]][index[1]].isVisible(): # Only reveal a square if it not already revealed
            indices.pop(0) # Remove the square to be revealed
            self.board[index[0]][index[1]].makeVisible() # Reveal this square
            if self.board[index[0]][index[1]].isMine(): # Check if this is a mine
                print('Game Over')
                return False
            else:
                if self.board[index[0]][index[1]].getValue() == 0: # If the square has no adjacent mines, reveal all adjacent squares automatically 
                    adjacent = [
                        (r,c) for r in range(self.getRows()) for c in range(self.getCols()) # All squares on the board
                        if abs(r-index[0]) <= 1 and abs(c-index[1]) <= 1 # No further than 1 square away from the revealed square
                        and (r,c) != index # That isn't the revealed square
                        and (r,c) not in indices # And isn't already in the list of squares to be revealed
                        and not self.board[r][c].isVisible() 
                        and not self.board[r][c].isFlag()
                    ]
                    indices.extend(adjacent) # Then add all these to the list of squares to be revealed
                if indices != []: # If this list isn't empty, there are more squares to reveal, so call this method again on the next square
                    self.reveal(indices)
                if self.testComplete(): # Check if the game is won from this game. A True return means the game is not over
                    print('You Win!')
                    self.isComplete = True
                    return False
                return True
        else:
            return True

    # def firstReveal(self, index):

    #     self.addMines(self.MINES, index)
    #     print(index)
    #     self.reveal([index])
    #     return True
    
    def testComplete(self): # Tests if the game is won by making sure every non-mine is visible
        for row in self.board:
            for sq in row:
                if (not sq.isMine()) and (not sq.isVisible()):
                    return False
        return True

    @staticmethod
    def createParams(rows, cols, mines): # Allows a way to create custom boards
        return {
            'rows': rows,
            'columns': cols,
            'mines': mines
        }

    
