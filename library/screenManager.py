import pygame

from typing import Type

from library.screen import Screen
from library.gameManager import GameManager
from library.gameState import GameState

class ScreenManager:
    def __init__(self, gm: GameManager, gs: GameState):
        self.top: Screen | None = None
        self.gm = gm
        self.gs = gs
    
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

        while True:
            current: Screen = self.top

            current.start()
            while current == self.top:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                current.update()
                current.draw(screen)
                
                self.gm.time.tick()
