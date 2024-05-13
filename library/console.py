from library.common import *
from library.constant.fonts import *
import library.ui as ui
import library.draw as draw

class Console(ui.Form):
    def __init__(self):
        super().__init__()
        
        self.clear_keys()

        self.textbox = ui.Textbox((0, 0), fontm, 100)

        self.add_item(self.textbox)

        self.background = draw.Rect("darkgray", (100, 100))

        self.add_draw(self.background)