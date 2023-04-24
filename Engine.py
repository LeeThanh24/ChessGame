"""
This class is responsible for storing all the information about the current
state of the game .
Responsible for determining the valid moves at the current state
"""

"""
Translation :
pawn (p): con tot 
knight (N) : con ma 
rook (R): con xe 
bishop (B): con tuong 
queen (Q): con hau 
king (K): con vua 
"""


class GameState:
    def __init__(self):
        """
        board is initialized with 8x8 elements , each has 2 characters
        the first character represents the color : 'b','w'
        the second character represents the type of the piece :'K','Q','R','B','N','p'
        the remaining is for empty
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        # To determine white is able to move first
        self.whiteToMove = True

        # To capture the movement of each piece
        self.moveLog = []

    def makeMove (self,move ) :
        self.board[move.startRow][move.startCol]="--" #we want to move so leave the square
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move) #log the move in order to  undo if necessary
        self.whiteToMove=  not self.whiteToMove #swap player

"""Movement of each piece"""


class Move():
    # the ranks are called rows (1-8) , columns are called files(A-H)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}  # index of matrix
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    #get the whole notation movement of a piece :example player 1 go from a6 to c6 -> a6 c6
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) +" "+ self.getRankFile(self.endRow, self.endCol)

    # example : c6 a8 ...
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
