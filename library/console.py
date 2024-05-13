from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .screenManager import ScreenManager

from .common import *
from .constant.fonts import *

from . import ui
from . import draw

class Console(ui.Form):
    class Arg():
        def __init__(self, name: str, value_type: str):
            self.name = name
            self.value_tye = value_type
            self.optional = False

    class Command():
        def __init__(self, name: str, args: list[Console.Arg], optional_args: list[Console.Arg]):
            self.name = name
            self.args = args
            self.optional_args = optional_args

    def __init__(self, sm: ScreenManager):
        super().__init__()
        
        self.sm = sm

        self.active = False

        self.clear_keys()
        self.add_key(pygame.K_RETURN, self.command)

        self.textbox = ui.Textbox((0, 0), fontm, 100, charset="all", blacklist="`", start="", end="")
        self.add_item(self.textbox)

        self.background = draw.Rect("gray30", (1, 1))
        self.add_draw(self.background)
        self.textbox_background = draw.Rect("gray18", (1, 1))
        self.add_draw(self.textbox_background)
    
    def draw(self, surface: Surface):
        size = surface.get_size()
        height = size[1] // 2 // fontm.height * fontm.height
        self.background.size = (size[0], height)
        self.textbox_background.size = (size[0], fontm.height)
        self.textbox_background.dest = (0, height - fontm.height)
        self.textbox.dest = self.textbox_background.dest
        self.textbox._max_chars = int(size[0] / fontm.width)
        
        super().draw(surface)
    
    def command(self, event: Event):
        value = self.textbox.value.strip()

        if value == "":
            return
        elif " " not in value:
            command = value
            args = []
        else:
            command = value.split(" ", 1)[0]
            args = value.split(" ")[1:]
        
        match command:
            case "quit":
                self.sm.break_flag = True