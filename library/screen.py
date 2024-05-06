from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from library.gameManager import GameManager
    from library.gameState import GameState
    from library.screenManager import ScreenManager
    from library.input.interactable import Interactable

import pygame
from typing import List

class Screen:
    name = "screen"

    def __init__(self, gm: GameManager, gs: GameState, sm: ScreenManager, name: str):
        self.interactables: List[Interactable] = []
        self.next: Screen | None = None
        self.gm = gm
        self.gs = gs
        self.sm = sm
        self.name = name
    
    def start(self):
        pass

    def update(self, events: List[pygame.event.Event]):
        pass

    def update_interactables(self, events: List[pygame.event.Event]):
        for event in events:
            for inter in self.interactables:
                inter.on_event(event)

    
    def draw(self, screen: pygame.Surface):
        pass

    def draw_interactables(self, screen: pygame.Surface):
        for inter in self.interactables:
            inter.draw(screen)
