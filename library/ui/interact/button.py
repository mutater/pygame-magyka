from library.common import *
from ..draw import Draw, DrawOrList

from . import DrawInteract, EventCallbackOrList

class Button(DrawInteract):
    def __init__(self, dest: Coordinate, draws: DrawOrList, callbacks: EventCallbackOrList, mods: IntOrList = []):
        super().__init__(dest)
        
        self.add_draw(draws, dest)

        self.rect = self.get_draws_rect()

        self.add_key([pygame.K_RETURN, pygame.K_SPACE], callbacks, mods)
        self.add_button(1, callbacks, mods)
