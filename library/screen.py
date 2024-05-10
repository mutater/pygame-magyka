from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from library.gameManager import GameManager
    from library.gameState import GameState
    from library.screenManager import ScreenManager

from library.common import *

class Screen:
    name = "screen"

    def __init__(self, gm: GameManager, gs: GameState, sm: ScreenManager, name: str):
        self.next: Screen | None = None
        self.gm = gm
        self.gs = gs
        self.sm = sm
        self.name = name
    
    def start(self):
        pass

    def update(self, events: List[pygame.event.Event]):
        pass

    def draw(self, window: pygame.Surface):
        pass
