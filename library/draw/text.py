from library.common import *
from . import Draw

class Text(Draw):
    def __init__(self, dest: Coordinate, size: Coordinate):
        super().__init__(dest, size)
