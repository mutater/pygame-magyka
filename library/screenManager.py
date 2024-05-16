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
        self.current: Screen
        self.gm = gm

        self.break_flag = False

        pygame.init()
        reset_key_repeat()
        
        self.base_size = (1280, 720)
        self.window = pygame.display.set_mode(self.base_size, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.console = Console(self)
        self.scale_factor = 1
        self.scale = (1, 1)
        
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
    
    def pop(self):
        if self.top == None or self.top.next == None:
            return

        self.top = self.top.next
        self.top.next = None
    
    def pop_to(self, name: str):
        if self.top == None:
            return

        while self.top.name != name:
            self.pop()
    
    def clear(self):
        self.top = None

    def peek(self) -> str:
        path = ""
        
        i = self.top
        names: list[str] = []

        while i != None:
            names.insert(0, i.name.title())
            i = i.next
        
        for i in range(len(names)):
            if i != 0:
                path += " -> "
            
            path += names[i]
        
        return path
    
    def loop(self):
        if self.top == None:
            raise Exception("No screen has been pushed yet.")

        while not self.break_flag:
            self.current = self.top

            if not self.current.started:
                self.current.start()
            
            while not self.break_flag and self.current == self.top:
                events: list[Event] = pygame.event.get() # type: ignore

                for event in events:
                    if event == None:
                        continue

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
                    elif event.type == pygame.WINDOWRESIZED:
                        self.scale_factor = min(self.window.get_width() // self.base_size[0], self.window.get_height() // self.base_size[1])

                        if self.scale_factor < 1:
                            self.scale_factor = min(self.window.get_width() / self.base_size[0], self.window.get_height() / self.base_size[1])
                        
                        self.scale = (self.scale_factor, self.scale_factor)
                    
                    if hasattr(event, "pos"):
                        event.pos = div_coords(event.pos, self.scale)


                if self.console.active:
                    self.console.update(self.dt, events)
                    events = []

                self.current.update(self.dt, events)

                surface = pygame.Surface(div_coords(self.window.get_size(), self.scale))
                surface.fill("#0f1820")

                self.current.draw(surface)

                if self.console.active:
                    self.console.draw(surface)
                
                pygame.transform.scale(surface, self.window.get_size(), self.window)

                pygame.display.flip()

                self.dt = self.clock.tick(60) / 1000
