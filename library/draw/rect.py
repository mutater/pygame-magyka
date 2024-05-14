from ..common import *

from . import Draw

class Rect(Draw):
    def __init__(self, color: ColorValue, size: Coordinate, dest: Coordinate = (0, 0)):
        super().__init__(size, dest)
        self.surface.fill("white")
        self.color = color

    @property
    def size(self) -> Coordinate:
        return self.surface.get_size()
    
    @size.setter
    def size(self, value: Coordinate):
        if value != self.size:
            surface = pygame.Surface(value, pygame.SRCALPHA)
            surface.fill("white")
            self.update_surface(surface)

