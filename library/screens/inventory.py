from library.common import Surface
from ..screen import *
from . import *

class InventoryScreen(Screen):
    name = "map"

    def start(self):
        super().start()
    
    def update(self, dt: float, events: list[Event | None]):
        super().update(dt, events)
    
    def draw(self, window: Surface):
        super().draw(window)
