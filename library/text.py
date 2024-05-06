import pygame

from library.common import *

class Text:
    def __init__(self, size: Coordinate):
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.draw_surface = pygame.Surface(size, pygame.SRCALPHA)
        self.color = pygame.Color("white")
        self.o_color = pygame.Color("black")
    
    def blit(self, surface: pygame.Surface, dest: Coordinate):
        self.surface.blit(surface, dest)

    def draw(self, surface: pygame.Surface, dest: Coordinate):
        if self.color != self.o_color:
            self.draw_surface = self.surface.copy()
            replace_color(self.draw_surface, (255, 255, 255), self.color)
            self.o_color = self.color
        
        surface.blit(self.draw_surface, dest)
    
    def get_width(self) -> int:
        return self.surface.get_width()
    
    def get_height(self) -> int:
        return self.surface.get_height()
