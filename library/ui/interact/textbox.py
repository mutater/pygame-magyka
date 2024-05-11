from library.common import *
from library.constant import fonts
from library.timer import Timer

from . import DrawInteract
from ..draw import Font, Text

class Textbox(DrawInteract):
    def __init__(self, dest: Coordinate, font: Font, max_chars: int, value: str = "", charset: str = "all"):
        super().__init__()

        self.font = font
        self.max_chars = max_chars
        self.value = value

        self.back_text = Text(font, f"> [{'':<{self.max_chars}}]")
        self.cursor_text = Text(font, "_", (font.width * 3, 0))
        self.value_text = Text(font, self.value, (font.width * 3, 0))

        self.cursor_timer = Timer(0.5)
        
        self.charset = fonts.charset.get(charset, None)

        if self.charset == None:
            raise ValueError("Invalid charset.")
        
        self.add_draw(self.back_text, dest)
        self.add_draw(self.cursor_text, dest)
        self.add_draw(self.value_text, dest)

    def _on_selected(self):
        super()._on_selected()
        pygame.key.set_repeat(300, 50)
    
    def _on_unselected(self):
        super()._on_unselected()
        pygame.key.set_repeat(500, 100)

    def on_key_event(self, event: Event):
        if event.type != pygame.KEYDOWN:
            return
        
        if event.key == pygame.K_BACKSPACE and len(self.value) > 0:
            if event.mod & pygame.KMOD_CTRL:
                self.value = self.value.rstrip()
                self.value = " ".join(self.value.split(" ")[:-1])
                if self.value != "":
                    self.value += " "
            else:
                self.value = self.value[:-1]
        if event.unicode in self.charset:
            self.value += event.unicode
        
        self.value = self.value[0:self.max_chars]

        self.cursor_text.move((self.font.width * (len(self.value) - len(self.value_text.value)), 0))
        self.cursor_text.visible = True
        self.cursor_timer.value = -0.25
        self.value_text.value = self.value
    
    def update(self, dt: float, events: list[Event]):
        if self.selected:
            if self.cursor_timer.tick(dt).complete:
                self.cursor_text.visible = not self.cursor_text.visible
        else:
            self.cursor_text.visible = False
            self.cursor_timer.reset()


    def draw(self, surface: Surface):
        self.back_text.color = self.color
        
        for draw in self.draws:
            draw.draw(surface)
