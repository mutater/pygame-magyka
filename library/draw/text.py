from library.common import *
from library.draw.draw import Draw

class Text(Draw):
    def __init__(self, dest: Coordinate, size: Coordinate):
        super().__init__(dest, size)
