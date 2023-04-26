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
from abc import abstractclassmethod

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
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "wR", "--", "--", "--", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "--"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        # To determine white is able to move first
        self.whiteToMove = True

        # To capture the movement of each piece
        self.moveLog = []
        self.translate = {'w': True,
                          'b': False}
        self.moveFunction = {'p' : self.getPawnMoves, 
                             'N': self.getKnightMoves, 
                             'R': self.getRookMoves, 
                             'B': self.getBishopMoves,
                             'Q': self.getQueenMoves,
                             'K': self.getKingMoves}

    def makeMove(self, move):
        r, c = move.startRow, move.startCol
        r_des, c_des = move.endRow, move.endCol
        recentPiece = self.board[r][c][1]
        possibleMoves = [(i.endRow, i.endCol) for i in self.getAllPossibleMoves(recentPiece, r, c)]
        
        if (r_des, c_des) in possibleMoves:
            self.board[move.startRow][move.startCol]="--" #we want to move so leave the square
            self.board[move.endRow][move.endCol]=move.pieceMoved
            print(move.getChessNotation())

            self.moveLog.append(move) #log the move in order to  undo if necessary
            self.whiteToMove=  not self.whiteToMove #swap player

#Movement of each piece
    def getAllPossibleMoves(self, piece, r, c):
        moves = []
        if piece != '-':
            self.moveFunction[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove == True:
            if self.board[r][c][0] == 'w' and r != 0:
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r, c), (r-2, c), self.board))
                if self.board[r-1][c] == '--':
                    moves.append(Move((r, c), (r-1, c), self.board))
                if c - 1 >= 0:
                    if self.board[r-1][c-1][0] == 'b':
                        moves.append(Move((r, c), (r-1, c-1), self.board))
                if c + 1 <= 7:
                    if self.board[r-1][c+1][0] == 'b':
                        moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            if self.board[r][c][0] == 'b' and r != 7:
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r, c), (r+2, c), self.board))
                if self.board[r+1][c] == '--':
                    moves.append(Move((r, c), (r+1, c), self.board))
                if c - 1 >= 0:
                    if self.board[r+1][c-1][0] == 'w':
                        moves.append(Move((r, c), (r+1, c-1), self.board))
                if c + 1 <= 7:
                    if self.board[r+1][c+1][0] == 'w':
                        moves.append(Move((r, c), (r+1, c+1), self.board))
        return moves

    def getKnightMoves(self, r, c, moves):
        assumption = [(r+1, c+2), (r+2, c+1), (r-1, c+2), (r+2, c-1), (r-2, c+1), (r+1, c-2), (r-1, c-2), (r-2, c-1)]
        
        if self.whiteToMove == self.translate[self.board[r][c][0]]:
            for ele in assumption:
                if ele[0] < 8 and ele[1] < 8:
                    if self.board[ele[0]][ele[1]][0] == '-' or self.whiteToMove != self.translate[self.board[ele[0]][ele[1]][0]]:
                        moves.append(Move((r, c), (ele[0], ele[1]), self.board))


    def getRookMoves(self, r, c, moves):
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        if self.whiteToMove == self.translate[self.board[r][c][0]]:
            for dir in directions:
                for step in range(1, 8):
                    new_r, new_c = r+dir[0]*step, c+dir[1]*step
                    if new_r < 8 and new_c < 8:     
                        if self.board[new_r][new_c][0] == '-':
                            moves.append(Move((r, c), (new_r, new_c), self.board))
                        else:
                            if self.translate[self.board[new_r][new_c][0]] != self.whiteToMove:
                                moves.append(Move((r, c), (new_r, new_c), self.board))
                            break


    def getBishopMoves(self, r, c, moves):
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        if self.whiteToMove == self.translate[self.board[r][c][0]]:
            for dir in directions:
                for step in range(1, 8):
                    new_r, new_c = r+dir[0]*step, c+dir[1]*step
                    if new_r < 8 and new_c < 8:     
                        if self.board[new_r][new_c][0] == '-':
                            moves.append(Move((r, c), (new_r, new_c), self.board))
                        else:
                            if self.translate[self.board[new_r][new_c][0]] != self.whiteToMove:
                                moves.append(Move((r, c), (new_r, new_c), self.board))
                            break

    def getQueenMoves(self, r, c, moves):
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1), (0, 1), (1, 0), (-1, 0), (0, -1)]
        if self.whiteToMove == self.translate[self.board[r][c][0]]:
            for dir in directions:
                for step in range(1, 8):
                    new_r, new_c = r+dir[0]*step, c+dir[1]*step
                    if new_r < 8 and new_c < 8:     
                        if self.board[new_r][new_c][0] == '-':
                            moves.append(Move((r, c), (new_r, new_c), self.board))
                        else:
                            if self.translate[self.board[new_r][new_c][0]] != self.whiteToMove:
                                moves.append(Move((r, c), (new_r, new_c), self.board))
                            break

    def getKingMoves(self, r, c, moves):
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1), (0, 1), (1, 0), (-1, 0), (0, -1)]
        if self.whiteToMove == self.translate[self.board[r][c][0]]:
            for dir in directions:
                new_r, new_c = r+dir[0], c+dir[1]
                if new_r < 8 and new_c < 8:     
                    if self.board[new_r][new_c][0] == '-':
                        moves.append(Move((r, c), (new_r, new_c), self.board))
                    else:
                        if self.translate[self.board[new_r][new_c][0]] != self.whiteToMove:
                            moves.append(Move((r, c), (new_r, new_c), self.board))
                        break
        

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
    

