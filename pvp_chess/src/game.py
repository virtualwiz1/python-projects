import pygame

from const import *
from board import Board
from draggable_piece import DraggablePiece
from config import Config
from square import Square

class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.draggable_piece = DraggablePiece()
        self.config = Config()

    #Show methods/blit methods

    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(rows):
            for col in range(cols):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * sqSize, row * sqSize, sqSize,sqSize)
                # show / blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    label = self.config.font.render(str(rows - row), 1, color)
                    label_pos = (5,5+row*sqSize)
                    # blit / show
                    surface.blit(label,label_pos)
                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    label = self.config.font.render(Square.get_alphacol(col), 1, color)
                    label_pos = (col * sqSize + sqSize - 15, height - 25)
                    # blit / show
                    surface.blit(label,label_pos)

    def show_pieces(self,surface):
        for row in range(rows):
            for col in range(cols):
                #piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    #all pieces except dragging pieces
                    if piece is not self.draggable_piece.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * sqSize + sqSize // 2, row * sqSize + sqSize // 2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme

        if self.draggable_piece.dragging:
            piece = self.draggable_piece.piece

            #loop all valid moves
            for move in piece.moves:
                #color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                #rect
                rect = (move.final.col * sqSize, move.final.row * sqSize, sqSize, sqSize)
                #show / blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme
        
        if self.board.last_move:
            initial  = self.board.last_move.initial
            final  = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * sqSize, pos.row * sqSize, sqSize,sqSize)
                # show / blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180,180,180)
            # rect
            rect = (self.hovered_sqr.col * sqSize, self.hovered_sqr.row * sqSize,sqSize,sqSize)
            # show / blit
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()