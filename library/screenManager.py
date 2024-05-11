from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .screen import Screen

from .common import *
from .gameManager import GameManager

class ScreenManager:
    def __init__(self, gm: GameManager):
        self.top: Screen | None = None
        self.gm = gm

        self.break_flag = False
        self.console_flag = False

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    
    def toggle_fullscreen(self):
        if self.window.get_flags() & pygame.FULLSCREEN:
            self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        else:
            pygame.display.quit()
            pygame.display.init()
            self.window = pygame.display.set_mode((0, 0), pygame.NOFRAME | pygame.FULLSCREEN)

    def push(self, Screen: Type[Screen]):
        screen = Screen(self.gm, self, Screen.name)

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

                current.update(self.dt, events)

                self.window.fill("#080f18")

                current.draw(self.window)
                
                pygame.display.flip()

                self.dt = self.clock.tick(60) / 1000
