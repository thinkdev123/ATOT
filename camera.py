import pygame as pg
from settings import *


class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pg.display.get_surface()
        self.offset = pg.math.Vector2(0,0)

    def customDraw(self,player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH//2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT//1.5

        for sprite in self.sprites():
            self.offsetPos = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image,self.offsetPos)
            

        # pg.draw.rect(self.displaySurface, "blue", player.rect)
