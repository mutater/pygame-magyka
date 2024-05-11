from library.common import *
from library.constant.fonts import *
from library.screen import Screen

import library.ui.draw as draw
import library.ui.interact as interact

class Test(Screen):
    def start(self):
        self.form = interact.Form()
        self.form.add_draw([
            draw.Text(fonts, "Sphinx of black quartz, judge my vow.", (umx, umy)),
            draw.Text(fontm, "Sphinx of black quartz, judge my vow.", (umx, umy * 2)),
            draw.Text(fontl, "Sphinx of black quartz, judge my vow.", (umx, umy * 3))
        ])
        self.textbox = interact.Textbox((umx, umy * 5), fontm, 32)
        self.form.add_item(self.textbox)

    def update(self, dt: float, events: list[Event]):
        self.form.update(dt, events)

    def draw(self, window: Surface):
        self.form.draw(window)
    
    def print(self, event: Event):
        print("asdf")
    
    def print2(self, event: Event):
        print("asdf2")