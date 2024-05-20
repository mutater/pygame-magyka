from ..screen import *

class TestScreen(Screen):
    def start(self):
        self.entity = entity.GameObject()
        self.entity.add_component(component.Health())
        self.entity.health.percent = 50

        self.form = ui.Form()
        self.form.add_draw([
            draw.Label(fonts, "Sphinx of black quartz, judge my vow.", (umx, umy)),
            draw.Label(fontm, "Sphinx of black quartz, judge my vow.", (umx, umy * 2)),
            draw.Label(fontl, "Sphinx of black quartz, judge my vow.", (umx, umy * 3)),
        ])
        self.textbox = ui.Textbox((umx, umy * 5), fontm, 32, "abcd efgh [[[[[[]]]]")
        self.form.add_item(self.textbox)

        self.form.add_item(ui.ButtonGroup((umx, umy * 9), fontm, [
            ("a", "asdf", pygame.K_a, self.print),
            ("b", "bsdf", pygame.K_b, self.print),
            ("c", "csdf", pygame.K_c, self.print),
        ]))

    def update(self, dt: float, events: list[Event]):
        self.form.update(dt, events)

    def draw(self, window: Surface):
        self.form.draw(window)
    
    def print(self, event: Event):
        print("asdf")
    
    def print2(self, event: Event):
        print("asdf2")