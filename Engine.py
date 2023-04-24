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