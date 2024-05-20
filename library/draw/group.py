from library.common import Surface
from ..common import *
from ..valueContainer import ValueContainer

from . import Draw, Font

class Group(Draw):
    def __init__(self, dest: Coordinate = (0, 0)):
        self.name = ""
        
        self.rect = pygame.Rect(dest, (0, 0))
        self._align = "topleft"

        self._draws: list[Draw] = []
    
    # Getters / Setters

    @property
    def dest(self) -> tuple[int, int]:
        return getattr(self.rect, self.align)
    
    @dest.setter
    def dest(self, dest: Coordinate):
        dest = int_coords(dest)
        if dest != self.dest:
            for draw in self._draws:
                draw.move(sub_coords(dest, self.dest))

            setattr(self.rect, self.align, int_coords(dest))

    def add_draw(self, draws: Draw | list[Draw]):
        if not isinstance(draws, list):
            draws = [draws]
        
        for draw in draws:
            draw.move(self.dest)
            self._draws.append(draw)
    
    def draw(self, surface: Surface):
        for draw in self._draws:
            draw.draw(surface)
