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
from abc import abstractmethod
import copy
from tkinter import *


def submitFunc():
    global finalResult
    finalResult = entry.get()

    window.destroy()


def create_ui():
    global window
    window = Tk()
    window.title("Promotion")
    window.geometry("+500+400")

    submit = Button(window, text="submit", command=submitFunc)
    submit.grid(row=1, column=1)

    label = Label(window, text="R:Rook, B:Bishop, Knight:N, Queen:Q ")
    label.config(font=("Arial", 30))
    label.grid(row=0, column=0)

    global entry
    entry = Entry()
    entry.config(font=('Arial', 50))  # change font
    entry.config(width=10)  # width displayed in characters
    entry.grid(row=0, column=1)


class GameState:
    def __init__(self):
        """
        board is initialized with 8x8 elements , each has 2 characters
        the first character represents the color : 'b','w'
        the second character represents the type of the piece :'K','Q','R','B','N','p'
        the remaining is for empty
        """
        characterW = Character('w')
        characterW.create()
        characterB = Character('b')
        characterB.create()
        self.teams = {'w': characterW.listCharacter,
                      'b': characterB.listCharacter}

        self.achievement = {'w': [],
                            'b': []}
        self.board = [
            [self.teams['b']['R'][0], self.teams['b']['N'][0], self.teams['b']['B'][0], self.teams['b']['Q'][0],
             self.teams['b']['K'][0], self.teams['b']['B'][1], self.teams['b']['N'][1], self.teams['b']['R'][1]],
            [self.teams['b']['p'][0], self.teams['b']['p'][1], self.teams['b']['p'][2], self.teams['b']['p'][3],
             self.teams['b']['p'][4], self.teams['b']['p'][5], self.teams['b']['p'][6], self.teams['b']['p'][7]],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            [self.teams['w']['p'][0], self.teams['w']['p'][1], self.teams['w']['p'][2], self.teams['w']['p'][3],
             self.teams['w']['p'][4], self.teams['w']['p'][5], self.teams['w']['p'][6], self.teams['w']['p'][7]],
            [self.teams['w']['R'][0], self.teams['w']['N'][0], self.teams['w']['B'][0], self.teams['w']['Q'][0],
             self.teams['w']['K'][0], self.teams['w']['B'][1], self.teams['w']['N'][1], self.teams['w']['R'][1]],
        ]
        # update position
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != '--':
                    self.board[r][c].updatePosition((r, c))

        # To determine white is able to move first
        self.whiteToMove = True
        # To determine whose turn
        self.player = 'w' if self.whiteToMove == True else 'b'
        # To capture the movement of each piece
        self.moveLog = [None]

        # Includes all the enemie-pieces that are threatening the respective KING
        self.checker = {'w': [],
                        'b': []}

    def makeMove(self, move):
        piece = move.pieceMoved
        piece_captured = move.pieceCaptured

        if piece == '--':
            return
        if piece.team != self.player:
            return

        r, c = move.startRow, move.startCol
        r_des, c_des = move.endRow, move.endCol

        # get all valid moves that the piece of interested is capable of doing
        valid_Moves = piece.getAllValidMoves(self)

        if (r_des, c_des) in valid_Moves:

            # check if KING can castle with ROOK
            if piece.type == 'K' and (r_des, c_des) in [(7, 2), (7, 6), (0, 2), (0, 6)]:
                if piece.can_castling(r_des, c_des, self):
                    self.castling(r_des, c_des)
                    return

            # check if PAWN can En-passant
            if piece.type == 'p' and (r_des, c_des) in [(r + 1, c + 1), (r - 1, c - 1), (r - 1, c + 1),
                                                        (r + 1, c - 1)] and self.board[r_des][c_des] == '--':
                if piece.can_en_passant(r, c, r_des, c_des, self):
                    self.en_passant(r, c, r_des, c_des)
                    return

            self.board[r][c] = "--"  # we want to move so leave the square
            self.board[r_des][c_des] = move.pieceMoved

            if piece.type == 'K':
                piece.had_MOVED = 1

            # check if PAWN can Promote
            if piece.type == 'p':
                if self.player == 'w' and r_des == 0:
                    self.promote(r_des, c_des)
                elif self.player == 'b' and r_des == 7:
                    self.promote(r_des, c_des)

            # add the piece_captured to achievement list and remove it in enemy team list
            if piece_captured != '--':
                self.achievement[self.player].append(piece_captured)
                self.teams[piece_captured.team][piece_captured.type].remove(piece_captured)
            piece.updatePosition((r_des, c_des))
            print(move.pieceMoved.name, move.getChessNotation())

            self.moveLog.append(move)  # log the move in order to  undo if necessary

            self.whiteToMove = not self.whiteToMove  # swap player
            self.player = 'w' if self.whiteToMove == True else 'b'

    def castling(self, r, c):
        row = 7 if self.player == 'w' else 0
        king = self.teams[self.player]['K'][0]
        rK, cK = king.position
        self.board[rK][cK] = '--'

        if (r, c) == (row, 2):
            self.moveLog.append([Move((rK, cK), (row, 2), self.board), Move((row, 0), (row, 3), self.board)])
            self.board[row][2] = king
            self.board[row][0] = '--'
            self.board[row][3] = self.teams[self.player]['R'][0]
            king.updatePosition((row, 2))
            self.teams[self.player]['R'][0].updatePosition((row, 3))
        else:
            self.moveLog.append([Move((rK, cK), (row, 6), self.board), Move((row, 7), (row, 5), self.board)])
            self.board[row][6] = king
            self.board[row][7] = '--'
            self.board[row][5] = self.teams[self.player]['R'][1]
            king.updatePosition((row, 6))
            self.teams[self.player]['R'][1].updatePosition((row, 5))

        king.had_MOVED = 1
        self.whiteToMove = not self.whiteToMove
        self.player = 'w' if self.whiteToMove == True else 'b'

    def en_passant(self, r, c, r_des, c_des):
        piece = self.board[r][c]
        piece_captured = self.board[r_des][c_des]
        action = Move((r, c), (r_des, c_des), self.board)
        action.pieceCaptured = self.board[r][c_des]

        self.board[r][c] = '--'
        self.board[r_des][c_des] = piece
        self.board[r][c_des] = '--'

        self.moveLog.append(action)
        piece.updatePosition((r_des, c_des))
        self.achievement[self.player].append(piece_captured)
        self.teams[piece_captured.team][piece_captured.type].remove(piece_captured)

        self.whiteToMove = not self.whiteToMove
        self.player = 'w' if self.whiteToMove == True else 'b'

    def promote(self, r, c):
        create_ui()
        window.mainloop()
        option = finalResult

        piece = self.board[r][c]
        if option == 'Q':
            opt = Queen(self.player)
            opt.updatePosition((r, c))
            self.teams[self.player]['Q'].append(opt)

        elif option == 'N':
            opt = Knight(self.player)
            opt.updatePosition((r, c))
            self.teams[self.player]['N'].append(opt)

        elif option == 'B':
            opt = Bishop(self.player)
            opt.updatePosition((r, c))
            self.teams[self.player]['B'].append(opt)

        elif option == 'R':
            opt = Rook(self.player)
            opt.updatePosition((r, c))
            self.teams[self.player]['R'].append(opt)
        self.board[r][c] = opt
        self.teams[self.player]['p'].remove(piece)

    # Check
    def Check(self, r, c, board):
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1),
                      (0, 1), (1, 0), (-1, 0), (0, -1),
                      (r + 1, c + 2), (r + 2, c + 1), (r - 1, c + 2), (r + 2, c - 1), (r - 2, c + 1), (r + 1, c - 2),
                      (r - 1, c - 2), (r - 2, c - 1)]
        checker = []

        for idx, dir in enumerate(directions):
            for step in range(1, 8):
                if idx < 8:
                    new_r, new_c = r + dir[0] * step, c + dir[1] * step
                else:
                    new_r, new_c = dir[0], dir[1]
                if 0 <= new_r < 8 and 0 <= new_c < 8:
                    if board[new_r][new_c] != '--':
                        # if the piece of interested is not belong to our side, check their threating
                        if board[new_r][new_c].team != self.player:
                            if idx < 4:
                                # for enemie' PAWN
                                if step == 1:
                                    if self.player == 'w':
                                        if 0 <= r - 1 < 8 and 0 <= c - 1 < 8 and 0 <= c + 1 < 8:
                                            if board[r - 1][c + 1] != '--':
                                                if board[r - 1][c + 1].type == 'p':
                                                    checker.append([(r - 1, c + 1), board[r - 1][c + 1]])
                                            if board[r - 1][c - 1] != '--':
                                                if board[r - 1][c - 1].type == 'p':
                                                    checker.append([(r - 1, c - 1), board[r - 1][c - 1]])
                                    else:
                                        if 0 <= r + 1 < 8 and 0 <= c - 1 < 8 and 0 <= c + 1 < 8:
                                            if board[r + 1][c + 1] != '--':
                                                if board[r + 1][c + 1].type == 'p':
                                                    checker.append([(r + 1, c + 1), board[r + 1][c + 1]])
                                            if board[r + 1][c - 1] != '--':
                                                if board[r + 1][c - 1].type == 'p':
                                                    checker.append([(r + 1, c - 1), board[r + 1][c - 1]])
                                                    # for enemie' BISHOP, QUEEN, KING
                                if board[new_r][new_c].type == 'B' or board[new_r][new_c].type == 'Q' or (
                                        step == 1 and board[new_r][new_c].type == 'K'):
                                    checker.append([(new_r, new_c), board[new_r][new_c]])
                                break
                            elif 4 <= idx < 8:
                                # for enemie' ROOK, QUEEN, KING
                                if board[new_r][new_c].type == 'R' or board[new_r][new_c].type == 'Q' or (
                                        step == 1 and board[new_r][new_c].type == 'K'):
                                    checker.append([(new_r, new_c), board[new_r][new_c]])
                                break
                        # if the piece of interested is our team, check the other directions
                        else:
                            break
                            # for enemie's KNIGHT
            if 8 <= idx < 16:
                if 0 <= dir[0] < 8 and 0 <= dir[1] < 8:
                    if board[dir[0]][dir[1]] != '--':
                        if board[new_r][new_c].team != self.player:
                            if board[new_r][new_c].type == 'N':
                                checker.append([(dir[0], dir[1]), board[dir[0]][dir[1]]])

        return checker

    def End_Game(self):
        for type in self.teams[self.player]:
            for piece in self.teams[self.player][type]:
                if piece.getAllValidMoves(self) != []:
                    return 0
        return 1

    def RESULT(self):
        if self.End_Game():
            print('END GAME ROI')
            r_K, c_K = self.teams[self.player]['K'][0].position
            if self.Check(r_K, c_K, self.board) != []:
                return 'WHITE WIN' if self.player == 'b' else 'win'
            return 'DRAW'
        print('CHUA END GAME')
        return None


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

    # get the whole notation movement of a piece :example player 1 go from a6 to c6 -> a6 c6
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + " " + self.getRankFile(self.endRow, self.endCol)

    # example : c6 a8 ...
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


class Character():
    def __init__(self, team):
        self.listCharacter = {'p': [], 'R': [], 'N': [], 'B': [], 'Q': [], 'K': []}
        self.team = team
        self.team_bool = True if self.team == 'w' else False
        self.position = ()

    def create(self):
        self.listCharacter['p'] = [Pawn(self.team) for i in range(8)]
        self.listCharacter['R'] = [Rook(self.team) for i in range(2)]
        self.listCharacter['N'] = [Knight(self.team) for i in range(2)]
        self.listCharacter['B'] = [Bishop(self.team) for i in range(2)]
        self.listCharacter['Q'] = [Queen(self.team)]
        self.listCharacter['K'] = [King(self.team)]

    def updatePosition(self, pos):
        self.position = pos

    def getAllValidMoves(self, gs):
        king = gs.teams[self.team]['K'][0]
        lastMove = gs.moveLog[-1]
        board = gs.board
        r_K, c_K = king.position

        valid_moves = []
        (r, c) = self.position

        if self.type == 'p':
            possibleMoves = [(i.endRow, i.endCol) for i in self.getAllPossibleMoves(board, lastMove)]
        else:
            possibleMoves = [(i.endRow, i.endCol) for i in self.getAllPossibleMoves(board)]

        for move in possibleMoves:
            (r_des, c_des) = move
            temp_board = copy.deepcopy(board)

            # check if KING can castle with ROOK
            if self.type == 'K' and self.had_MOVED == 0:
                if (r_des, c_des) in [(7, 2), (7, 6), (0, 2), (0, 6)]:
                    if self.can_castling(r_des, c_des, gs):
                        valid_moves.append(move)

            # check if PAWN can En-passant
            if self.type == 'p' and (r_des, c_des) in [(r + 1, c + 1), (r - 1, c - 1), (r - 1, c + 1),
                                                       (r + 1, c - 1)] and board[r_des][c_des] == '--':
                if self.can_en_passant(r, c, r_des, c_des, gs):
                    valid_moves.append(move)

            piece_moved = temp_board[r][c]
            temp_board[r][c] = "--"  # we want to move so leave the square
            temp_board[r_des][c_des] = piece_moved

            if self.type == 'K':
                r_K, c_K = (r_des, c_des)

            # make an assumption and see if the move is valid or not
            checker = GameState.Check(gs, r_K, c_K, temp_board)

            # If the move is valid, add new move to list
            if checker == []:
                valid_moves.append(move)

        return valid_moves

    @abstractmethod
    def getAllPossibleMoves(self):
        pass


class Pawn(Character):
    def __init__(self, team):
        super().__init__(team)
        self.type = 'p'
        self.name = self.team + 'p'


    def getAllPossibleMoves(self, board, pre_move):
        r, c = self.position
        moves = []

        if self.team == 'w' and r != 0:
            if r == 6 and board[r - 2][c] == '--':
                moves.append(Move((r, c), (r - 2, c), board))
            if board[r - 1][c] == '--':
                moves.append(Move((r, c), (r - 1, c), board))
            if c - 1 >= 0:
                if board[r - 1][c - 1] != '--':
                    if board[r - 1][c - 1].team == 'b':
                        moves.append(Move((r, c), (r - 1, c - 1), board))
            if c + 1 <= 7:
                if board[r - 1][c + 1] != '--':
                    if board[r - 1][c + 1].team == 'b':
                        moves.append(Move((r, c), (r - 1, c + 1), board))
            # check if the pawn can do en-passant
            if r == 3:
                if pre_move.pieceMoved.type == 'p':
                    if pre_move.startRow == 1 and pre_move.endRow == 3:
                        if pre_move.startCol == c + 1:
                            moves.append(Move((r, c), (2, c + 1), board))
                        elif pre_move.startCol == c - 1:
                            moves.append(Move((r, c), (2, c - 1), board))
        else:
            if self.team == 'b' and r != 7:
                if r == 1 and board[r + 2][c] == '--':
                    moves.append(Move((r, c), (r + 2, c), board))
                if board[r + 1][c] == '--':
                    moves.append(Move((r, c), (r + 1, c), board))
                if c - 1 >= 0:
                    if board[r + 1][c - 1] != '--':
                        if board[r + 1][c - 1].team == 'w':
                            moves.append(Move((r, c), (r + 1, c - 1), board))
                if c + 1 <= 7:
                    if board[r + 1][c + 1] != '--':
                        if board[r + 1][c + 1].team == 'w':
                            moves.append(Move((r, c), (r + 1, c + 1), board))
                # check if the pawn can do en-passant
                if r == 4:
                    if pre_move.pieceMoved.type == 'p':
                        if pre_move.startRow == 6 and pre_move.endRow == 4:
                            if pre_move.startCol == c + 1:
                                moves.append(Move((r, c), (5, c + 1), board))
                            elif pre_move.startCol == c - 1:
                                moves.append(Move((r, c), (5, c - 1), board))
        return moves

    def can_en_passant(self, r, c, r_des, c_des, gs):
        temp_board = copy.deepcopy(gs.board)
        piece = temp_board[r][c]

        rK, cK = gs.teams[self.team]['K'][0].position

        temp_board[r][c] = '--'
        temp_board[r_des][c_des] = piece
        temp_board[r][c_des] = '--'

        if GameState.Check(gs, rK, cK, temp_board) == []:
            return 1
        return 0


class Knight(Character):
    def __init__(self, team):
        super().__init__(team)
        self.type = 'N'
        self.name = self.team + 'N'

    def getAllPossibleMoves(self, board):
        r, c = self.position
        directions = [(r + 1, c + 2), (r + 2, c + 1), (r - 1, c + 2), (r + 2, c - 1), (r - 2, c + 1), (r + 1, c - 2),
                      (r - 1, c - 2), (r - 2, c - 1)]
        moves = []

        for ele in directions:
            if 0 <= ele[0] < 8 and 0 <= ele[1] < 8:
                if board[ele[0]][ele[1]] == '--' or self.team != board[ele[0]][ele[1]].team:
                    moves.append(Move((r, c), (ele[0], ele[1]), board))
        return moves


class Rook(Character):
    def __init__(self, team):
        super().__init__(team)
        self.type = 'R'
        self.name = self.team + 'R'

    def getAllPossibleMoves(self, board):
        r, c = self.position
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        moves = []

        for dir in directions:
            for step in range(1, 8):
                new_r, new_c = r + dir[0] * step, c + dir[1] * step
                if 0 <= new_r < 8 and 0 <= new_c < 8:
                    if board[new_r][new_c] == '--':
                        moves.append(Move((r, c), (new_r, new_c), board))
                    else:
                        if self.team != board[new_r][new_c].team:
                            moves.append(Move((r, c), (new_r, new_c), board))
                        break
        return moves


class Bishop(Character):
    def __init__(self, team):
        super().__init__(team)
        self.type = 'B'
        self.name = self.team + 'B'

    def getAllPossibleMoves(self, board):
        r, c = self.position
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        moves = []

        for dir in directions:
            for step in range(1, 8):
                new_r, new_c = r + dir[0] * step, c + dir[1] * step
                if 0 <= new_r < 8 and 0 <= new_c < 8:
                    if board[new_r][new_c] == '--':
                        moves.append(Move((r, c), (new_r, new_c), board))
                    else:
                        if self.team != board[new_r][new_c].team:
                            moves.append(Move((r, c), (new_r, new_c), board))
                        break
        return moves


class Queen(Character):
    def __init__(self, team):
        super().__init__(team)
        self.type = 'Q'
        self.name = self.team + 'Q'

    def getAllPossibleMoves(self, board):
        r, c = self.position
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1), (0, 1), (1, 0), (-1, 0), (0, -1)]
        moves = []

        for dir in directions:
            for step in range(1, 8):
                new_r, new_c = r + dir[0] * step, c + dir[1] * step
                if 0 <= new_r < 8 and 0 <= new_c < 8:
                    if board[new_r][new_c] == '--':
                        moves.append(Move((r, c), (new_r, new_c), board))
                    else:
                        if self.team != board[new_r][new_c].team:
                            moves.append(Move((r, c), (new_r, new_c), board))
                        break
        return moves


class King(Character):
    def __init__(self, team):
        super().__init__(team)
        self.type = 'K'
        self.name = self.team + 'K'
        self.had_MOVED = 0

    def can_castling(self, r, c, gs):
        if self.had_MOVED == 1:
            return 0
        board = gs.board
        row = 7 if self.team == 'w' else 0
        if (r, c) == (row, 2):
            if board[row][1] != '--' or board[row][2] != '--' or board[row][3] != '--':
                return 0
        else:
            if board[row][5] != '--' or board[row][6] != '--':
                return 0

        temp_board = copy.deepcopy(board)
        rK, cK = self.position
        temp_board[rK][cK] = '--'

        if (r, c) == (row, 2):
            # check if castling is valid
            check_1 = GameState.Check(gs, row, 2, temp_board)
            check_2 = GameState.Check(gs, row, 3, temp_board)
            check_3 = GameState.Check(gs, row, 4, temp_board)

            if check_1 == [] and check_2 == [] and check_3 == []:
                return 1
        else:
            check_1 = GameState.Check(gs, row, 5, temp_board)
            check_2 = GameState.Check(gs, row, 6, temp_board)
            check_3 = GameState.Check(gs, row, 4, temp_board)
            if check_1 == [] and check_2 == [] and check_3 == []:
                return 1
        return 0

    def getAllPossibleMoves(self, board):
        r, c = self.position
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1), (0, 1), (1, 0), (-1, 0), (0, -1)]
        moves = []

        for dir in directions:
            new_r, new_c = r + dir[0], c + dir[1]
            if 0 <= new_r < 8 and 0 <= new_c < 8:
                if board[new_r][new_c] == '--':
                    moves.append(Move((r, c), (new_r, new_c), board))
                else:
                    if self.team != board[new_r][new_c].team:
                        moves.append(Move((r, c), (new_r, new_c), board))
        # check if KING can do castling
        if self.had_MOVED == 0:
            row = 7 if self.team == 'w' else 0
            if board[row][0] != '--':
                if board[row][1] == '--' and board[row][2] == '--' and board[row][3] == '--' and board[row][
                    0].type == 'R' and self.team == board[row][0].team:
                    moves.append(Move((r, c), (row, 2), board))
            if board[row][0] != '--':
                if board[row][5] == '--' and board[row][6] == '--' and board[row][7].type == 'R' and self.team == \
                        board[row][7].team:
                    moves.append(Move((r, c), (row, 6), board))
        return moves
