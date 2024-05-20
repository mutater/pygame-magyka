from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .gameManager import GameManager
    from .screenManager import ScreenManager

from .common import *
from .fonts import *
from . import draw, ui, entity, component

class Screen:
    """
    A screen. Contains start(), update(), and draw() methods.
    """

    name = "screen"

    def __init__(self, gm: GameManager, sm: ScreenManager, name: str):
        self.started = False
        self.next: Screen | None = None
        self.gm = gm
        self.sm = sm
        self.name = name

        self.form = ui.Form()
        self.form.add_key(pygame.K_ESCAPE, self.back)
        self.can_back = True
    
    def start(self):
        """
        Called once when the screen is loaded by the screen manager for the first time.

        If overriding Screen.start(), call super().start() in the method.
        """
        
        self.started = True

    def update(self, dt: float, events: list[Event]):
        """
        Called every frame to process events.

        If overriding Screen.update(), call super().update(...) or manually update the form.
        """

        self.form.update(dt, events)

    def draw(self, window: Surface):
        """
        Called every frame to draw to the window.

        If overriding Screen.draw(), call super().draw(...) or manually draw the form.
        """

        self.form.draw(window)

    def back(self, event: Event):
        """
        Callback for when escape is pressed and self.can_back is True.

        If overriding Screen.back(), call super().back(...) AFTER all other code.
        """
        if self.can_back and self.form.selected_item == None:
            self.sm.pop()
