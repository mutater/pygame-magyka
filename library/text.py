import pygame as pg

from library.common import *

class Text:
    def __init__(self, size: Coordinate):
        self.surface = pg.Surface(size)
        self.surface.fill((255, 0, 255))
        self.surface.set_colorkey((255, 0, 255))
    
    def blit(self, surface: pg.Surface, dest: Coordinate):
        self.surface.blit(surface, dest)

    def draw(self, surface: pg.Surface, dest: Coordinate):
        surface.blit(self.surface, dest)
    
    def get_width(self) -> int:
        return self.surface.get_width()
    
    def get_height(self) -> int:
        return self.surface.get_height()
