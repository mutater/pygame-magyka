from ..common import *

from . import Draw

class Rect(Draw):
    def __init__(self, color: ColorValue, size: Coordinate, dest: Coordinate = (0, 0)):
        super().__init__(size, dest)
        self.color = color
    
    # Getters / Setters

    def draw(self, surface: Surface):
        pygame.draw.rect(surface, self.color, self.rect)
