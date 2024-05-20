from ..screen import *
from . import *

class NewGameScreen(Screen):
    name = "newGame"

    def start(self):
        super().start()

        self.form.add_draw(draw.Label(fontm, "Enter your name.", (umx, umy)))
        self.form.add_item(
            ui.Textbox((umx, umy * 3), fontm, 12, charset=blacklist_charset(charset_all, charset_windows_invalid))
            .named("name_textbox")
            .add_key(pygame.K_RETURN, self.name_textbox_submit))
        self.form.add_draw(draw.Label(fontm, "", (umx, umy * 5)).named("name_label"))
        self.form.add_item(
            ui.Button((umx, umy * 5), draw.Label(fontm, "Submit"), self.name_textbox_submit)
            .named("name_submit"))
    
    def verify(self, value: str, textbox: ui.Textbox, label: draw.Label) -> bool:
        if value == "":
            label.text = cmd_color("indianred1") + "Cannot be empty."
            textbox.set_value(value)
            return False
        elif len(value) < 3:
            label.text = cmd_color("indianred1") + "Must be at least 3 characters long."
            textbox.set_value(value)
            return False
        
        return True

    def name_textbox_submit(self, event: Event):
        textbox = self.form.get_interact(ui.Textbox, "name_textbox")
        button = self.form.get_interact(ui.Button, "name_submit")
        label = self.form.get_draw(draw.Label, "name_label")

        name = textbox.value.strip()

        if self.verify(name, textbox, label):
            self.gm.player = entity.Player(name)

            self.sm.clear()
            self.sm.push(MapScreen)
        else:
            button.move_to((umx, umy * 7))
            return
