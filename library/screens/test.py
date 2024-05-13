from ..screen import *

class TestScreen(Screen):
    def start(self):
        self.entity = entity.GameObject()
        self.entity.add_component(component.Health())
        self.entity.health.percent = 50
        print(self.entity.health)
        self.bar = draw.Bar(fontm, self.entity.health, 32, (umx, umy * 7), color_filled="red")

        self.form = ui.Form()
        self.form.add_draw([
            draw.Text(fonts, "Sphinx of black quartz, judge my vow.", (umx, umy)),
            draw.Text(fontm, "Sphinx of black quartz, judge my vow.", (umx, umy * 2)),
            draw.Text(fontl, "Sphinx of black quartz, judge my vow.", (umx, umy * 3)),
            self.bar
        ])
        self.textbox = ui.Textbox((umx, umy * 5), fontm, 32, "abcd efgh [[[[[[]]]]")
        self.form.add_item(self.textbox)

    def update(self, dt: float, events: EventList):
        self.form.update(dt, events)

    def draw(self, window: Surface):
        self.form.draw(window)
    
    def print(self, event: Event):
        print("asdf")
    
    def print2(self, event: Event):
        print("asdf2")