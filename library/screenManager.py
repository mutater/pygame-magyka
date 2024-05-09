from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from library.gameManager import GameManager
    from library.gameState import GameState
    from library.screen import Screen

from library.common import *

class ScreenManager:
    def __init__(self, gm: GameManager, gs: GameState):
        self.top: Screen | None = None
        self.gm = gm
        self.gs = gs
        self.break_flag = False
    
    def push(self, Screen: Type[Screen]):
        screen = Screen(self.gm, self.gs, self, Screen.name)

        screen.next = self.top
        self.top = screen
    
    def pop(self) -> Screen | None:
        if self.top == None:
            return
        else:
            oTop = self.top
            self.top = self.top.next
            return oTop
    
    def pop_to(self, name: str) -> Screen | None:
        if self.top == None:
            return

        oTop = self.top
        while self.top.name != name:
            oTop = self.pop()
        
        return oTop
    
    def peek(self) -> Screen | None:
        return self.top
    
    def loop(self, screen: pygame.Surface):
        if self.top == None:
            raise Exception("No screen has been pushed yet.")

        while not self.break_flag:
            current: Screen = self.top

            current.start()
            while not self.break_flag and current == self.top:
                events = pygame.event.get()

                for event in events:
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.MOUSEMOTION:
                        pygame.mouse.set_visible(True)
                    elif event.type == pygame.KEYDOWN:
                        pygame.mouse.set_visible(False)

                current.update(events)

                screen.fill("#080f18")

                current.draw(screen)
                
                pygame.display.flip()

                self.gm.time.tick()
