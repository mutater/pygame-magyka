from library.common import Surface
from ..common import *

from . import DrawSurface

class Column(DrawSurface):
    def __init__(self, color: ColorValue, width: float, left: float = 0):
        super().__init__((width, 1), (left, 0))
        self.color = color
    
    def draw(self, surface: Surface):
        self.height = surface.get_height()
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, "black", pygame.Rect(self.rect.left, -2, self.width, self.height + 4), 2)
