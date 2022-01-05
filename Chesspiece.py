import pygame as p

# hello


class ChessPiece:
    def __init__(self, color):
        self.color = color
        self.row = None
        self.col = None
        self.img = None

    def step_movements(self, board_state, movements):  # for King, Knight
        moves = []
        for x, y in movements:
            if self.row + x in range(len(board_state)) and self.col + y in range(len(board_state[0])):
                element = board_state[self.row + x][self.col + y]
                if element is None or element.color != self.color:
                    moves.append((self.row + x, self.col + y))
        return moves

    def linear_movements(self, board_state, directions):  # for Rook, Bishop, Queen, should be fine now
        moves = []
        for direction in directions:
            row_sum, col_sum = 0, 0
            for i in range(len(board_state)):
                row_sum += direction[0]
                col_sum += direction[1]  # increment by + direction at every iter step
                if self.row + row_sum in range(len(board_state)) and self.col + col_sum in range(len(board_state[0])):
                    element = board_state[self.row + row_sum][self.col + col_sum]
                    if element is None:
                        moves.append((self.row + row_sum, self.col + col_sum))
                    else:
                        if element.color != self.color:
                            moves.append((self.row + row_sum, self.col + col_sum))
                        break
        return moves

    def get_all_moves(self, board_state):  # dispatch all moves accordingly to what type of piece they are.
        if isinstance(self, Pawn):
            return self.pawn_movements(board_state, self.color)
        elif isinstance(self, Rook) or isinstance(self, Bishop) or isinstance(self, Queen):
            return self.linear_movements(board_state, self.directions)
        elif isinstance(self, King) or isinstance(self, Knight):
            return self.step_movements(board_state, self.movements)

    def get_legal_moves(self, board):
        all_moves = self.get_all_moves(board.board_state)
        legal_moves = []
        pos = (self.row, self.col) #original piece pos
        for move in all_moves:
            temp_state = board.copy() #original board pos
            board.move_piece(pos, move)
            if not board.is_under_check():
                legal_moves.append(move)
            board.board_state = temp_state # board_state now points to the copied board_state
        return legal_moves


class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # up down left right
        self.first_move = True  # for castling
        self.img = p.image.load("Images/wR.png") if color == "White" else p.image.load("Images/bR.png")


class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # all 4 diagonals
        self.img = p.image.load("Images/wB.png") if color == "White" else p.image.load("Images/bB.png")


class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.movements = [(2, -1), (2, 1), (1, -2), (1, 2), (-1, -2), (-1, 2), (-2, -1), (-2, 1)]  # 8 movements
        self.img = p.image.load("Images/wN.png") if color == "White" else p.image.load("Images/bN.png")


class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.movements = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # 8 movements
        self.first_move = True  # for castling
        self.img = p.image.load("Images/wK.png") if color == "White" else p.image.load("Images/bK.png")


class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # rook + bishop
        self.img = p.image.load("Images/wQ.png") if color == "White" else p.image.load("Images/bQ.png")


class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True  # pawn can move 1 or 2 squares in first move
        self.img = p.image.load("Images/wP.png") if color == "White" else p.image.load("Images/bP.png")
        self.enpassantable = False
        self.enpassant_move = None

    def pawn_movements(self, board_state, color):  # should be correct now
        moves = []
        forward_one = -1 if color == "White" else 1  # White moves -1 direction, black +1.
        if board_state[self.row + forward_one][self.col] is None:
            moves.append((self.row + forward_one, self.col))
            if self.first_move:
                if board_state[self.row + (forward_one * 2)][self.col] is None:
                    moves.append((self.row + forward_one * 2, self.col))
        for i in [-1, 1]:  # check left and right diagonal for enemy piece to eat.
            if self.col + i in range(len(board_state[0])):  # prevent out of range error
                piece = board_state[self.row + forward_one][self.col + i]
                if piece is not None and piece.color != self.color:
                    moves.append((self.row + forward_one, self.col + i))
                en_piece = board_state[self.row][self.col + i]  # for enpassant checks
                if isinstance(en_piece, Pawn) and en_piece.enpassantable == True and en_piece.color != self.color:
                    self.enpassant_move = (self.row + forward_one, self.col + i)  # can capture enpassant pawn
                    print(self.enpassant_move)
        return moves
