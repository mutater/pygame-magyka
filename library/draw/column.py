from library.common import Surface
from ..common import *

from . import Draw

class Column(Draw):
    def __init__(self, color: ColorValue, width: float, dest: Coordinate = (0, 0)):
        super().__init__((width, 1), dest)
        self.surface.fill("white")
        self.color = color
        self._width = width
        self._height = 1

    @property
    def width(self) -> float:
        return self.surface.get_width()
    
    @width.setter
    def width(self, value: float):
        if value != self._width:
            surface = pygame.Surface((value, self.height), pygame.SRCALPHA)
            surface.fill("white")
            self.update_surface(surface)
    
    @property
    def height(self) -> float:
        return self.surface.get_height()
    
    @height.setter
    def height(self, value: float):
        if value != self._height:
            surface = pygame.Surface((self.width, value), pygame.SRCALPHA)
            surface.fill("white")
            self.update_surface(surface)
    
    def draw(self, surface: Surface):
        self.height = surface.get_height()
        super().draw(surface)