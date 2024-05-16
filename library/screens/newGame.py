from ..screen import *
from . import *

class NewGameScreen(Screen):
    name = "newGame"

    def start(self):
        super().start()

        self.form.add_draw(draw.Label(fontm, "Enter your name.", (umx, umy)))
        self.form.add_item(
            ui.Textbox((umx, umy * 3), fontm, 16, charset=blacklist(charset_all, charset_windows_invalid))
            .named("name_textbox")
            .add_key(pygame.K_RETURN, self.name_textbox_submit))
        self.form.add_draw(draw.Label(fontm, "", (umx, umy * 5)).named("name_label"))

        self.form.add_draw(draw.Label(fontm, "Enter your class.", (umx, umy * 7)))
        self.form.add_item(
            ui.Textbox((umx, umy * 9), fontm, 16, charset=charset_all)
            .named("class_textbox")
            .add_key(pygame.K_RETURN, self.class_textbox_submit))
        self.form.add_draw(draw.Label(fontm, "", (umx, umy * 11)).named("class_label"))
    
    def verify(self, name: str, textbox: ui.Textbox, label: draw.Label) -> bool:
        if name == "":
            label.text = cmd_color("indianred1") + "Cannot be empty."
            textbox.set_value(name)
            return False
        elif len(name) < 3:
            label.text = cmd_color("indianred1") + "Must be at least 3 characters long."
            textbox.set_value(name)
            return False
        
        return True

    def name_textbox_submit(self, event: Event):
        textbox = self.form.get_interact(ui.Textbox, "name_textbox")
        label = self.form.get_draw(draw.Label, "name_label")

        name = textbox.value.strip()

        self.verify(name, textbox, label)
    
    def class_textbox_submit(self, event: Event):
        textbox = self.form.get_interact(ui.Textbox, "class_textbox")
        label = self.form.get_draw(draw.Label, "class_label")

        name = textbox.value.strip()

        self.verify(name, textbox, label)
