import pygame

from library.common import *
from library.input.interactable import Interactable, InputCodeValue, EventCallable
from library.text import Text

class Button(Interactable):
    def __init__(self, dest: Coordinate, text: Text):
        super().__init__()
        self.dest = dest
        self.text = text
        self.rect = pygame.Rect(dest[0], dest[1], self.text.get_width(), self.text.get_height())
    
    def with_inputs(self, key: InputCodeValue, callback: EventCallable):
        self.set_keys([key])
        self.set_buttons([1])
        self.set_callbacks([("main", callback)])
        return self

    def draw(self, surface: pygame.Surface, offset: Coordinate = (0, 0)):
        self.text.color = self.color
        self.text.draw(surface, add_coords(self.dest, offset))