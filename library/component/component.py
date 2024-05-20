from ..common import *
from ..serializable import Serializable

from .. import draw

class Component(Serializable):
    def __init__(self):
        pass

    def update(self, dt: float, events: list[Event]):
        pass

    def get_draw(self, dest: Coordinate) -> draw.Draw:
        return draw.Draw((1, 1))
