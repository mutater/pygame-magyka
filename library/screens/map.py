from ..screen import *
from . import *

class MapScreen(Screen):
    name = "map"

    def start(self):
        super().start()

        self.form.add_draw([
            draw.Label(fontl, "Map", (umx, umy)),
            draw.Label(fontm, f"{self.gm.player.info.name} <Level {self.gm.player.level}>", (umx, umy * 3)),
            self.gm.player.life.get_draw((umx, umy * 4)),
            self.gm.player.mana.get_draw((umx, umy * 5)),
            self.gm.player.level.exp.get_draw((umx, umy * 6))
        ])

        self.form.add_item(ui.ButtonGroup((umx * 2, umy * 8), fontm, [
            ("B", "/c[darkgray]Battle", pygame.K_b, self.battle),
            ("T", "/c[darkgray]Town", pygame.K_t, self.town),
            ("O", "Options", pygame.K_o, self.options),
            ("Q", "Quit", pygame.K_q, self.quit),
        ]))

        self.form.add_item(ui.ButtonGroup((umx * 2, umy * 17), fontm, [
            ("I", "/c[darkgray]Inventory", pygame.K_i, self.inventory),
            ("C", "/c[darkgray]Crafting", pygame.K_c, self.crafting),
            ("G", "/c[darkgray]Goals", pygame.K_g, self.goals),
            ("S", "/c[darkgray]Stats", pygame.K_s, self.stats),
        ]))
    
    def draw(self, window: Surface):
        super().draw(window)
    
    def update(self, dt: float, events: list[Event | None]):
        super().update(dt, events)
    
    # Callbacks

    def battle(self, event: Event):
        pass

    def town(self, event: Event):
        pass

    def options(self, event: Event):
        self.sm.push(OptionsScreen)

    def quit(self, event: Event):
        self.sm.break_flag = True
    
    def inventory(self, event: Event):
        pass

    def crafting(self, event: Event):
        pass

    def goals(self, event: Event):
        pass

    def stats(self, event: Event):
        pass
