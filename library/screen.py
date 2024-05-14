from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .gameManager import GameManager
    from .screenManager import ScreenManager

from .common import *
from .constant.fonts import *
from . import draw, ui, entity, component

class Screen:
    name = "screen"

    def __init__(self, gm: GameManager, sm: ScreenManager, name: str):
        self.next: Screen | None = None
        self.gm = gm
        self.sm = sm
        self.name = name

        self.form = ui.Form()
        self.form.add_key(pygame.K_ESCAPE, self.back)
        self.can_back = True
    
    def start(self):
        pass

    def update(self, dt: float, events: list[Event]):
        self.form.update(dt, events)

    def draw(self, window: Surface):
        self.form.draw(window)

    def back(self, event: Event):
        if self.can_back and self.form.selected_item == None:
            self.sm.pop()
