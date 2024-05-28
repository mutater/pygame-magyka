from ..screen import *
from . import *

class InventoryScreen(Screen):
    name = "inventory"

    def start(self):
        self.form_type = ui.Form()
        self.form_type.add_draw(draw.Column("gray20", umx * 20, umx))

        self.form_items = ui.Form()
        self.form_inspect = ui.Form()
    
    def update(self, dt: float, events: list[Event]):
        self.form_type.update(dt, events)
        self.form_items.update(dt, events)
        self.form_inspect.update(dt, events)
    
    def draw(self, window: Surface):
        self.form_type.draw(window)
        self.form_items.draw(window)
        self.form_inspect.draw(window)
