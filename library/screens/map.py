from library.common import Event, Surface
from ..screen import *

class MapScreen(Screen):
    name = "map"

    def start(self):
        self.form = ui.Form()
    
    def update(self, dt: float, events: list[Event]):
        self.form.update(dt, events)
    
    def draw(self, window: Surface):
        self.form.draw(window)
