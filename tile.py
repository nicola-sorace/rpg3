import pygame

class Tile:
    def __init__(self, style, xpos, ypos):
        self.s = style
        self.x = xpos
        self.y = ypos

        self.w = 50
        self.h = 50

    def draw(self, screen, cx, cy):
        #pygame.draw.rect(screen, (100,26,26), pygame.Rect(self.x*self.w-cx,self.y*self.h/2-cy/2,self.w,self.h/2))
        pygame.draw.rect(screen, (100,26,26), pygame.Rect(cx, cy, 50, 50))
