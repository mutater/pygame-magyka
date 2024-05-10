from library.common import *
from library.draw import Draw, DrawValueOrList

from . import DrawInteract, EventCallbackOrList

class Button(DrawInteract):
    def __init__(self, draws: DrawValueOrList, callbacks: EventCallbackOrList, mods: IntOrList = []):
        super().__init__()
        
        self.add_draw(draws)
        self.rect = self.get_draws_rect()

        self.add_key([pygame.K_RETURN, pygame.K_SPACE], callbacks, mods)
        self.add_button(1, callbacks, mods)

    def draw(self, surface: pygame.Surface):
        self.set_draws_color(self.color)
        
        super().draw(surface)