from library.common import *
from library.draw.text import Text

from . import Interact, EventCallbackValue

class Button(Interact):
    def __init__(self, dest: Coordinate, text: Text, callbacks: EventCallbackValue):
        super().__init__()
        
        self.add_draw(text)
        self.rect = pygame.Rect(dest[0], dest[1], text.get_width(), text.get_height())

        self.add_keys([pygame.K_RETURN, pygame.K_SPACE], callbacks)
        self.add_button(1, callbacks)

    def draw(self, surface: pygame.Surface):
        self.set_draws_color(self.color)
        
        super().draw(surface)