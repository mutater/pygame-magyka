from library.common import Event, Surface
from ..screen import *

class OptionsScreen(Screen):
    name = "options"

    def start(self):
        self.form = ui.Form()
        self.form.add_draw(draw.Text(fontl, "- Options -", (umx, umy)))
    
    def update(self, dt: float, events: list[Event]):
        self.form.update(dt, events)
    
    def draw(self, window: Surface):
        self.form.draw(window)
