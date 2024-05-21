from ..common import *
from ..fonts import *
from ..valueContainer import ValueContainer

from .. import draw
from . import Component

class Life(Component, ValueContainer):
    def __init__(self, value: int = 30):
        Component.__init__(self)
        ValueContainer.__init__(self, value)

    def get_draw(self, dest: Coordinate, length: int = 32) -> draw.Bar:
        return draw.Bar(self, length, dest, color_filled="crimson")
