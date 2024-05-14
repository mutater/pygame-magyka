from ..common import *
from ..serializable import Serializable

class Component(Serializable):
    def __init__(self):
        self.name = "Component"

    def update(self, dt: float, events: list[Event]):
        pass

    def draw(self, surface: Surface):
        pass
