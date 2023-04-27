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
import copy
class GameState:
    def __init__(self):
        """
        board is initialized with 8x8 elements , each has 2 characters
        the first character represents the color : 'b','w'
        the second character represents the type of the piece :'K','Q','R','B','N','p'
        the remaining is for empty
        """
        self.board = [
            ["bR", "--", "--", "--", "bK", "--", "--", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "bQ", "--", "--", "--", "--", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "--", "wp", "wp", "wp", "wp", "--"],
            ["wR", "--", "--", "--", "wK", "--", "--", "wR"],
        ]
        # To determine white is able to move first
        self.whiteToMove = True
        # To determine whose turn
        self.player = 'w' if self.whiteToMove == True else 'b'
        # To capture the movement of each piece
        self.moveLog = []
        # just for brief and subtle coding 
        self.translate = {'w': True,
                          'b': False,
                          '-': None}
        self.moveFunction = {'p' : self.getPawnMoves, 
                             'N': self.getKnightMoves, 
                             'R': self.getRookMoves, 
                             'B': self.getBishopMoves,
                             'Q': self.getQueenMoves,
                             'K': self.getKingMoves}
        #KING'coordinates and the bool check if KING'motion has occurred or not
        self.kingInfo = {'w': [(7, 4), 0],
                        'b': [(0, 4), 0]}
        #Includes all the enemie-pieces that are threatening the respective KING
        self.checker = {'w' : [], 'b' : []}

        
    def makeMove(self, move):
        r, c = move.startRow, move.startCol
        r_des, c_des = move.endRow, move.endCol
        print(r, c,"->",r_des, c_des)
        piece = self.board[r][c][1]
        #get all possible moves that the piece of interested is capable of doing
        possibleMoves = [(i.endRow, i.endCol) for i in self.getAllPossibleMoves(piece, r, c)]

        if (r_des, c_des) in possibleMoves:
            #create temporary board and kingInfo to assump an event and see if KING is endangered 
            temp_board = copy.deepcopy(self.board)
            temp_kingInfo = copy.deepcopy(self.kingInfo)

            #check if KING can castle with ROOK
            if piece == 'K' and self.kingInfo[self.player][-1] == 0:
                if (r_des, c_des) in [(7, 2), (7, 6), (0, 2), (0, 6)]:
                    self.castling(r_des, c_des)
                    return
                
            #check if PAWN can En-passant 
            if piece == 'p' and (r_des, c_des) in [(r+1, c+1), (r-1, c-1), (r-1, c+1), (r+1, c-1)] and self.board[r_des][c_des] == '--':
                self.en_passant(r, c, r_des, c_des)
                return

            temp_board[r][c] = "--" #we want to move so leave the square
            temp_board[r_des][c_des] = move.pieceMoved

            #update KING's infomation
            if piece == 'K':
                if self.whiteToMove == True:
                    temp_kingInfo['w']= [(r_des, c_des), 1]
                else:
                    temp_kingInfo['b'] = [(r_des, c_des), 1]

            r_K, c_K = temp_kingInfo['w'][0]
            r_Kb, c_Kb = temp_kingInfo['b'][0]
            #make an assumption and see if the move is valid or not
            self.checker['w'] = self.Check(r_K, c_K, temp_board)
            self.checker['b'] = self.Check(r_Kb, c_Kb, temp_board)
            
            # If the move is valid, assign the assumption to reality
            if self.checker[self.player] == []:
                self.board = copy.deepcopy(temp_board)
                print(move.getChessNotation())
                self.kingInfo = copy.deepcopy(temp_kingInfo)
                self.moveLog.append(move) #log the move in order to  undo if necessary
                self.whiteToMove = not self.whiteToMove #swap player
                self.player = 'w' if self.whiteToMove == True else 'b'
            else:
            #If not, do it again
                temp_board = copy.deepcopy(self.board)

    def castling(self, r, c):
        row = 7 if self.player == 'w' else 0
        temp_board = copy.deepcopy(self.board)
        rK, cK = self.kingInfo[self.player][0]
        temp_board[rK][cK] = '--'

        if (r, c) == (row, 2):
            #check if castling is valid
            check_1 = self.Check(row, 2, temp_board)
            check_2 = self.Check(row, 3, temp_board)
            check_3 = self.Check(row, 4, temp_board)
            if check_1 == [] and check_2 == [] and check_3 == []:
                self.moveLog.append([Move((rK, cK), (row, 2), self.board), Move((row, 0), (row, 3), self.board)])
                temp_board[row][2] = self.player + 'K'
                temp_board[row][0] = '--'
                temp_board[row][3] = self.player + 'R'
                self.board = copy.deepcopy(temp_board)
                self.kingInfo[self.player][0] = (row, 2)
                self.whiteToMove = not self.whiteToMove
                self.player = 'w' if self.whiteToMove == True else 'b'
            else:
                self.temp_board = copy.deepcopy(self.board)
        else:
            check_1 = self.Check(row, 5, temp_board)
            check_2 = self.Check(row, 6, temp_board)
            check_3 = self.Check(row, 4, temp_board)
            if check_1 == [] and check_2 == [] and check_3 == []:
                self.moveLog.append([Move((rK, cK), (row, 6), self.board), Move((row, 7), (row, 5), self.board)])
                temp_board[row][6] = self.player + 'K'
                temp_board[row][7] = '--'
                temp_board[row][5] = self.player + 'R'
                self.board = copy.deepcopy(temp_board)
                self.kingInfo[self.player][0] = (row, 6)
                self.whiteToMove = not self.whiteToMove
                self.player = 'w' if self.whiteToMove == True else 'b'
            else:
                self.temp_board = copy.deepcopy(self.board)

    def en_passant(self, r, c, r_des, c_des):
        temp_board = copy.deepcopy(self.board)
        rK, cK = self.kingInfo[self.player][0]
        action = Move((r, c), (r_des, c_des), self.board)
        action.pieceCaptured = temp_board[r][c_des]
        temp_board[r][c] = '--'
        temp_board[r_des][c_des] = self.player + 'p'
        temp_board[r][c_des] = '--'
        if self.Check(rK, cK, temp_board) == []:
            self.moveLog.append(action)
            self.board = copy.deepcopy(temp_board)
            self.whiteToMove = not self.whiteToMove
            self.player = 'w' if self.whiteToMove == True else 'b'
        else:
            self.temp_board = copy.deepcopy(self.board)






    def promote(self, r, c):
        pass



            
        

            
                

#Check
    def Check(self, r, c, board):
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1), 
                      (0, 1), (1, 0), (-1, 0), (0, -1),
                      (r+1, c+2), (r+2, c+1), (r-1, c+2), (r+2, c-1), (r-2, c+1), (r+1, c-2), (r-1, c-2), (r-2, c-1)]
        checker = []

        for idx, dir in enumerate(directions):
            for step in range(1, 8):
                if idx < 8:
                    new_r, new_c = r+dir[0]*step, c+dir[1]*step
                else:
                    new_r, new_c = dir[0], dir[1]
                if 0 <= new_r < 8 and 0 <= new_c < 8:     
                    if board[new_r][new_c][0] != '-':
                        #if the piece of interested is not belong to our side, check their threating 
                        if board[new_r][new_c][0] != self.player:
                            if idx < 4:
                                #for enemie' PAWN
                                if step == 1:
                                    if self.player == 'w':
                                        if 0 <= r-1 < 8 and 0 <= c-1 < 8 and 0 <= c+1 < 8: 
                                            if board[r-1][c+1][1] == 'p' or board[r-1][c-1][1] == 'p':
                                                checker.append([(r-1, c+1), board[r-1][c-1]])
                                    else:
                                        if 0 <= r+1 < 8 and 0 <= c-1 < 8 and 0 <= c+1 < 8: 
                                            if board[r+1][c+1][1] == 'p' or board[r+1][c-1][1] == 'p':
                                                checker.append([(r+1, c+1), board[r+1][c-1]])     
                                #for enemie' BISHOP, QUEEN, KING
                                if board[new_r][new_c][1] == 'B' or board[new_r][new_c][1] == 'Q' or (step == 1 and board[new_r][new_c][1] == 'K'):
                                    checker.append([(new_r, new_c), board[new_r][new_c]])
                                break
                            elif 4 <= idx < 8:
                                #for enemie' ROOK, QUEEN, KING
                                if board[new_r][new_c][1] == 'R' or board[new_r][new_c][1] == 'Q' or (step == 1 and board[new_r][new_c][1] == 'K'):
                                    checker.append([(new_r, new_c), board[new_r][new_c]])
                                break
                        #if the piece of interested is our team, check the other directions 
                        else:
                            break 
            #for enemie's KNIGHT
            if 8 <= idx < 16:
                if 0 <= dir[0] < 8 and 0 <= dir[1] < 8:
                    if board[dir[0]][dir[1]][0] != '-':
                        if board[new_r][new_c][0] != board[r][c][0]:
                            if board[new_r][new_c][1] == 'N':
                                checker.append([(dir[0], dir[1]), board[dir[0]][dir[1]]])           
        return checker       



#Movement of each piece
    #get all possible moves of the specified piece, including ILLEGAL moves
    def getAllPossibleMoves(self, piece, r, c):
        moves = []
        if piece != '-':
            self.moveFunction[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        #check if the player has selected the correct piece regarding to their team
        if self.whiteToMove == self.translate[self.board[r][c][0]]:
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
                    #check if the pawn can do en-passant
                    if r == 3:
                        pre_move = self.moveLog[-1]
                        if pre_move.pieceMoved[1] == 'p':
                            if pre_move.startRow == 1 and pre_move.endRow == 3:
                                if pre_move.startCol == c+1:
                                    moves.append(Move((r, c), (2, c+1), self.board))
                                elif pre_move.startCol == c-1:
                                    moves.append(Move((r, c), (2, c-1), self.board))
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
                    #check if the pawn can do en-passant
                    if r == 4:
                        pre_move = self.moveLog[-1]
                        if pre_move.pieceMoved[1] == 'p':
                            if pre_move.startRow == 6 and pre_move.endRow == 4:
                                if pre_move.startCol == c+1:
                                    moves.append(Move((r, c), (5, c+1), self.board))
                                elif pre_move.startCol == c-1:
                                    moves.append(Move((r, c), (5, c-1), self.board))
            return moves

    def getKnightMoves(self, r, c, moves):
        assumption = [(r+1, c+2), (r+2, c+1), (r-1, c+2), (r+2, c-1), (r-2, c+1), (r+1, c-2), (r-1, c-2), (r-2, c-1)]
        
        #check if the player has selected the correct piece regarding to their team
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
                if 0 <= new_r < 8 and 0 <= new_c < 8:     
                    if self.board[new_r][new_c][0] == '-':
                        moves.append(Move((r, c), (new_r, new_c), self.board))
                    else:
                        if self.translate[self.board[new_r][new_c][0]] != self.whiteToMove:
                            moves.append(Move((r, c), (new_r, new_c), self.board))
            #check if KING can do castling
            if self.kingInfo[self.player][-1] == 0:
                row = 7 if self.player == 'w' else 0
                if self.board[row][2] == '--' and self.board[row][3] == '--' and self.board[row][0][1] == 'R' and self.player == self.board[row][0][0]:
                    moves.append(Move((r, c), (row, 2), self.board))
                if self.board[row][5] == '--' and self.board[row][6] == '--' and self.board[row][7][1] == 'R' and self.player == self.board[row][7][0]:
                    moves.append(Move((r, c), (row, 6), self.board))



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
    

