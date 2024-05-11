from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from library.screen import Screen

from library.common import *

from library.gameManager import GameManager
from library.gameState import GameState

class ScreenManager:
    def __init__(self):
        self.top: Screen | None = None
        self.gm = GameManager()
        self.gs = GameState()

        self.break_flag = False
        self.console_flag = False

        self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    
    def toggle_fullscreen(self):
        if self.window.get_flags() & pygame.FULLSCREEN:
            self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        else:
            pygame.display.quit()
            pygame.display.init()
            self.window = pygame.display.set_mode((0, 0), pygame.NOFRAME | pygame.FULLSCREEN)

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
    
    def loop(self):
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
                        if event.key == pygame.K_F11:
                            self.toggle_fullscreen()
                        elif event.key == pygame.K_RETURN and event.mod & pygame.KMOD_ALT:
                            self.toggle_fullscreen()

                current.update(self.gm.time.dt, events)

                self.window.fill("#080f18")

                current.draw(self.window)
                
                pygame.display.flip()

                self.gm.time.tick()
