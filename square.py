import random

class Square():
    def __init__(self, row, col):
        self.visible = False
        self.mine = False
        self.value = -1
        self.flag = False
        self.row = row
        self.col = col

    def makeMine(self):
        self.mine = True
    
    def changeFlag(self):
        if not self.isVisible():
            self.flag = not self.flag
        
    def isMine(self):
        return self.mine
    
    def makeVisible(self):
        self.visible = True
    
    def isFlag(self):
        return self.flag

    def isVisible(self):
        return self.visible

    def getValue(self):
        return self.value

    def calculateValue(self, board):
        adjacent = [(r,c) for r in range(board.ROWS) for c in range(board.COLS) if abs(r-self.row) <= 1 and abs(c-self.col) <= 1 and (r,c) != (self.row, self.col)]
        count = 0
        for r, c in adjacent:
            if board.board[r][c].isMine():
                count += 1

        self.value = count
    