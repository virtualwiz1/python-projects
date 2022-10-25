from const import *
from sound import Sound
from square import Square
from piece import *
from move import Move
import copy
import os

class Board:
    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(cols)]
        self.last_move = None
        self._create()
        self._addPieces('white')
        self._addPieces('black')

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].isempty()

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece


        if isinstance(piece, Pawn):
            # en_passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(os.path.join(
                        'assets/sounds/capture.wav'
                        ))
                    sound.play()

            # pawn promotion
            else:
                self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    # check for valid moves
    def valid_move(self, piece, move):
        return move in piece.moves

    # check for pawn promotion
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    # check if castling is available or not
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return

        for row in range(rows):
            for col in range(cols):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False

        piece.en_passant = True

    # check if the king is in CHECK currently
    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)

        for row in range(rows):
            for col in range(cols):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False


    def calc_moves(self, piece, row, col, bool=True):
        # calculate all the valid moves available of all the pieces
        
        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))

            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create a new move
                        move = Move(initial, final)

                        # check potential CHECK
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)
                    # blocked
                    else: break
                # not in range
                else: break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a new move
                        move = Move(initial, final)
                        # check potential CHECK
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)

            # en_passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # left en_passant
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                            # create a new move
                            move = Move(initial, final)
                            # check potential CHECK
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
            # right en_passant
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            # create a new move
                            move = Move(initial, final)
                            # check potential CHECK
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)


        def knight_moves():
            # total of 8 possible moves
            possible_moves = [
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row - 1, col + 2),
                (row - 1, col - 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col + 2),
                (row + 1, col - 2),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create new move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Move(initial, final)
                        # check potential CHECK
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)
        
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr 
                possible_move_col = col + col_incr 

                while True:
                    if Square.in_range(possible_move_row,possible_move_col):
                        # create initial and final possible move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a new move
                        move = Move(initial, final)

                        # empty = add move
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # check potential CHECK
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # check potential CHECK
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                            break

                        # has own piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_own_piece(piece.color):
                            break
                    else:break

                    # increamenting incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr
        
        def king_moves():
            adjs = [
                (row + 0, col + 1), # right
                (row + 0, col - 1), # left
                (row - 1, col + 0), # up
                (row - 1, col + 1), # up-right
                (row - 1, col - 1), # up-left
                (row + 1, col + 0), # down
                (row + 1, col + 1), # down-right
                (row + 1, col - 1), # down-left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create new move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        # create new move
                        move = Move(initial, final)
                        # check potential CHECK
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece(): # castling not possible pieces in middle 
                                break
                            if c == 3:
                                # adding left_rook to king class
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveRook = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveKing = Move(initial, final)

                                # check potential CHECKS
                                if bool:
                                    if not self.in_check(piece, moveKing) and not self.in_check(left_rook, moveRook):
                                        # append new move to rook
                                        left_rook.add_move(moveRook)
                                        # append new move to king
                                        piece.add_move(moveKing)
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveRook)
                                    # append new move to king
                                    piece.add_move(moveKing)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5,7):
                            if self.squares[row][c].has_piece(): # castling not possible pieces in middle 
                                break
                            if c == 6:
                                # adding right_rook to king class
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveRook = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveKing = Move(initial, final)

                                # check potential CHECKS
                                if bool:
                                    if not self.in_check(piece, moveKing) and not self.in_check(right_rook, moveRook):
                                        # append new move to rook
                                        right_rook.add_move(moveRook)
                                        # append new move to king
                                        piece.add_move(moveKing)
                                    
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveRook)
                                    # append new move to king
                                    piece.add_move(moveKing)

        if isinstance(piece,Pawn): # if piece = 'pawn'
            pawn_moves()
        
        elif isinstance(piece,Knight):
            knight_moves()
        
        elif isinstance(piece,Bishop):
            straightline_moves([
                (-1,1), # up-right diagonal
                (-1,-1), # up-left diagonal
                (1,1), # down-right diagonal
                (1,-1), # down-left diagonal
            ])
        
        elif isinstance(piece,Rook):
            straightline_moves([
                (-1,0), # up
                (1,0), # down
                (0,1), # right
                (0,-1), # left
            ])
        
        elif isinstance(piece,Queen):
            straightline_moves([
                (-1,1), # up-right diagonal
                (-1,-1), # up-left diagonal
                (1,1), # down-right diagonal
                (1,-1), # down-left diagonal
                (-1,0), # up
                (1,0), # down
                (0,1), # right
                (0,-1), # left
            ])
        
        elif isinstance(piece,King):
            king_moves()

    def _create(self):

        for row in range(rows):
            for col in range(cols):
                self.squares[row][col] = Square(row, col)

    def _addPieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(cols):
            self.squares[row_pawn][col] = Square(row_pawn,col,Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other,1,Knight(color))
        self.squares[row_other][6] = Square(row_other,6,Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other,2,Bishop(color))
        self.squares[row_other][5] = Square(row_other,5,Bishop(color))

        # Rooks
        self.squares[row_other][0] = Square(row_other,0,Rook(color))
        self.squares[row_other][7] = Square(row_other,7,Rook(color))

        # Queen
        self.squares[row_other][3] = Square(row_other,3,Queen(color))

        # King
        self.squares[row_other][4] = Square(row_other,4,King(color))
