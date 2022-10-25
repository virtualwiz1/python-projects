import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (width, height) )
        pygame.display.set_caption('Wiz Chess')
        self.game = Game()

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.draggable_piece

        while True:
            # show / blit methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                #mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.updateMouse(event.pos)

                    clicked_row = dragger.mouseY // sqSize #y-coordinates
                    clicked_col = dragger.mouseX // sqSize #x-coordinates

                    #if clicked square has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.saveInitial(event.pos)
                            dragger.drag_piece(piece)
                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                #mouse move
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // sqSize
                    motion_col = event.pos[0] // sqSize
                    game.set_hover(motion_row, motion_col)
                    if dragger.dragging:
                        dragger.updateMouse(event.pos)
                        #show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                #mouse release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.updateMouse(event.pos)
                        
                        released_row = dragger.mouseY // sqSize
                        released_col = dragger.mouseX // sqSize

                        #create possible moves
                        initial = Square(dragger.initial_row,dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)

                            # sound
                            game.play_sound(captured)
                            # show / blit methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()

                    dragger.undrag_piece()

                # key press
                elif event.type == pygame.KEYDOWN:
                    # changing theme
                    if event.key == pygame.K_t:
                        game.change_theme()
                    # reset game
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.draggable_piece

                #quit app
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()           

            pygame.display.update()

main = Main()
main.mainloop()