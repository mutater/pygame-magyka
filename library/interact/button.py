from library.common import *
from library.interact.interact import Interact, EventCallbackValue
from library.text import Text

class Button(Interact):
    def __init__(self, dest: Coordinate, text: Text, callbacks: EventCallbackValue):
        super().__init__()
        
        self.text = text
        self.rect = pygame.Rect(dest[0], dest[1], self.text.get_width(), self.text.get_height())

        self.add_keys([pygame.K_RETURN, pygame.K_SPACE], callbacks)
        self.add_button(1, callbacks)

    def draw(self, surface: pygame.Surface):
        self.text.color = self.color
        self.text.draw(surface, self.rect.topleft)