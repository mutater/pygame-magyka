from library.common import *
from library.constant.fonts import *
from library.screen import Screen

import library.draw as draw
import library.interact as interact

class Test(Screen):
    def start(self):
        self.form = interact.Form()
        self.form.add_item(
            interact.ButtonGroup((umx * 2, umy), fontm, [
                ("N", "New Game", pygame.K_n, self.print),
                ("C", "Continue", pygame.K_c, self.print),
                ("O", "Options", pygame.K_o, self.print),
                ("H", "Help", pygame.K_h, self.print),
                ("Q", "Quit", pygame.K_q, self.print)
            ])
        )

        self.form.add_item(
            interact.ButtonGroup((umx * 2, umy * 13), fontm, [
                ("N", "New Game", pygame.K_n, self.print),
                ("C", "Continue", pygame.K_c, self.print),
                ("O", "Options", pygame.K_o, self.print),
                ("H", "Help", pygame.K_h, self.print),
                ("Q", "Quit", pygame.K_q, self.print)
            ])
        )

    def update(self, events: List[pygame.event.Event]):
        self.form.update(events)

    def draw(self, screen: pygame.Surface):
        self.form.draw(screen)
    
    def print(self, event: pygame.event.Event):
        print("asdf")