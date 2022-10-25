import pygame

from const import *

class DraggablePiece:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0 

    #show methods / blit methods
    def update_blit(self, surface):
        #texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture

        #image
        img = pygame.image.load(texture)

        #rectangle
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        
        #blit
        surface.blit(img, self.piece.texture_rect)

    #other methods
    def updateMouse(self, position):
        self.mouseX, self.mouseY = position #x-coordinates and y-coordinates

    def saveInitial(self, position):
        self.initial_row = position[1] // sqSize #row number
        self.initial_col = position[0] // sqSize #col number

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None 
        self.dragging = False
