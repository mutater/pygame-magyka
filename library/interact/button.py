from library.common import *
from library.draw import Draw, DrawValue

from . import DrawInteract, EventCallbackValue

class Button(DrawInteract):
    def __init__(self, draws: DrawValue | List[DrawValue], callbacks: EventCallbackValue):
        super().__init__()
        
        self.add_draws(draws)
        self.rect = self.get_draws_rect()

        self.add_keys([pygame.K_RETURN, pygame.K_SPACE], callbacks)
        self.add_button(1, callbacks)

    def draw(self, surface: pygame.Surface):
        self.set_draws_color(self.color)
        
        super().draw(surface)