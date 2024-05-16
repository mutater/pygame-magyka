from library.common import Event, Surface
from ..screen import *

class OptionsScreen(Screen):
    name = "options"

    def start(self):
        self.form.add_draw(draw.Label(fontl, "- Options -", (umx, umy)))
