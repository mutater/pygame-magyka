from ..common import *
from ..fonts import *

from .. import draw
from . import Component

class Info(Component):
    def __init__(self, **kwargs):
        self.name: str = kwargs.get("name", "")
        self.desc: str = kwargs.get("desc", "")
        self.rarity: str = kwargs.get("rarity", "")
    
    def get_draw(self, dest: Coordinate) -> draw.Label:
        return draw.Label(fontm, self.name, dest)