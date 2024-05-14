from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .screen import Screen
    from .gameManager import GameManager

from .common import *
from .constant.fonts import *
from .console import Console

class ScreenManager:
    def __init__(self, gm: GameManager):
        self.top: Screen | None = None
        self.gm = gm

        self.break_flag = False

        pygame.init()
        pygame.key.set_repeat(500, 100)
        
        self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.console = Console(self)
        
        pygame.scrap.init()
    
    def toggle_fullscreen(self):
        if self.window.get_flags() & pygame.FULLSCREEN:
            self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        else:
            pygame.display.quit()
            pygame.display.init()
            self.window = pygame.display.set_mode((0, 0), pygame.NOFRAME | pygame.FULLSCREEN)
    
    def toggle_console(self):
        self.console.active = not self.console.active

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
    
    def clear(self):
        self.top = None

    def peek(self) -> Screen | None:
        return self.top
    
    def loop(self):
        if self.top == None:
            raise Exception("No screen has been pushed yet.")

        while not self.break_flag:
            current: Screen = self.top

            current.start()
            while not self.break_flag and current == self.top:
                events: list[Event] = pygame.event.get() # type: ignore

                scale = (1, 1)
                if self.window.get_height() > 1440:
                    scale = (2, 2)

                for event in events:
                    if event == None:
                        continue

                    if hasattr(event, "pos"):
                        event.pos = div_coords(event.pos, scale)

                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.MOUSEMOTION:
                        pygame.mouse.set_visible(True)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F11:
                            self.toggle_fullscreen()
                        elif event.key == pygame.K_RETURN and event.mod & pygame.KMOD_ALT:
                            self.toggle_fullscreen()
                        elif event.key == pygame.K_BACKQUOTE:
                            self.toggle_console()

                if self.console.active:
                    self.console.update(self.dt, events)
                    events = []

                current.update(self.dt, events)

                surface = pygame.Surface(div_coords(self.window.get_size(), scale))
                surface.fill("#0f1820")

                current.draw(surface)

                if self.console.active:
                    self.console.draw(surface)
                
                pygame.transform.scale(surface, self.window.get_size(), self.window)

                pygame.display.flip()

                self.dt = self.clock.tick(60) / 1000
