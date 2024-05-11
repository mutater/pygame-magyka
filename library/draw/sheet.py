import pygame
import math

from ..common import *

class Sheet:
    def __init__(self, file: str, size: Coordinate, padding: Coordinate = (0, 0)):
        self.size = size
        self.sprites = []

        image = pygame.image.load(file)

        rows = math.floor(image.get_height() / (size[1] + padding[1] * 2))
        cols = math.floor(image.get_width() / (size[0] + padding[0] * 2))

        for row in range(0, rows):
            for col in range(0, cols):
                x = col * (size[0] + padding[0] * 2) + padding[0]
                y = row * (size[1] + padding[1] * 2) + padding[1]
                self.sprites.append(image.subsurface((x, y, size[0], size[1])))
    
    def sprite(self, i: int) -> Surface:
        if i >= len(self.sprites):
            i = 0
        
        return self.sprites[i]
