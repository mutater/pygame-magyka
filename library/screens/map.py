from library.common import Surface
from ..screen import *
from . import *

class MapScreen(Screen):
    name = "map"

    def start(self):
        super().start()
        self.form.add_draw(draw.Label(fontl, "Map", (umx, umy)))
        self.form.add_draw(self.gm.player.info.get_draw((umx, umy * 3)))
        self.form.add_draw(self.gm.player.health.get_draw((umx, umy * 4)))
        self.form.add_draw(self.gm.player.mana.get_draw((umx, umy * 5)))

        def add(event: Event): self.gm.player.health += 1
        def sub(event: Event): self.gm.player.health -= 1
        self.form.add_key(pygame.K_KP_PLUS, add)
        self.form.add_key(pygame.K_KP_MINUS, sub)
    
    def draw(self, window: Surface):
        super().draw(window)
    
    def update(self, dt: float, events: list[Event | None]):
        super().update(dt, events)
