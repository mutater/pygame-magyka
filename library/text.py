import pygame as pg

from library.common import *

class Text:
    def __init__(self, size: Coordinate):
        self._surface = pg.Surface(size)
        self._surface.fill((255, 0, 255))
        self._surface.set_colorkey((255, 0, 255))
    
    def blit(self, surface: pg.Surface, dest: Coordinate):
        self._surface.blit(surface, dest)

    def draw(self, surface: pg.Surface, dest: Coordinate):
        surface.blit(self._surface, dest)
