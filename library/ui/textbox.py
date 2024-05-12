from ..common import *
from ..constant import fonts
from ..timer import Timer

from . import DrawInteract
from ..draw import Font, Text

class Textbox(DrawInteract):
    def __init__(self, dest: Coordinate, font: Font, max_chars: int, value: str = "", charset: str = "all"):
        super().__init__(dest)

        self.font = font
        self.max_chars = max_chars
        self.value = value
        self._index: int = 0
        self.index = 0

        self.back_text = Text(font, f"> [{'':<{self.max_chars}}]")
        self.value_text = Text(font, self.value, (font.width * 3, 0))
        self.cursor_text = Text(font, "_", (font.width * 3, 0))
        self.cursor_timer = Timer(0.5)
        
        self.charset = fonts.charset.get(charset, None)

        if self.charset == None:
            raise ValueError("Invalid charset.")
        
        self.add_draw(self.back_text, dest)
        self.add_draw(self.value_text, dest)
        self.add_draw(self.cursor_text, dest)

        self.rect = self.get_draws_rect()

    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, value: int):
        if value < 0:
            self._index = 0
        elif value > self.length:
            self._index = self.length
        else:
            self._index = value

    @property
    def length(self):
        return len(self.value)

    def char_at(self, index: int | None = None):
        if index == None:
            index = self.index

        if index < 0 or index >= self.length:
            return ""
        return self.value[index]

    def _on_selected(self):
        super()._on_selected()
        pygame.key.set_repeat(300, 50)
    
    def _on_unselected(self):
        super()._on_unselected()
        pygame.key.set_repeat(500, 100)

    def on_key_event(self, event: Event):
        if event.type != pygame.KEYDOWN:
            return
        
        def find_next_index(index: int, direction: int) -> int:
            ignore = None

            if index + direction >= self.length or index + direction < 0:
                pass
            elif self.value[index + direction] in fonts.charset["symbolic"]:
                ignore = fonts.charset["symbolic"]
            elif self.value[index + direction] == " ":
                ignore = " "

            while 0 <= index <= self.length:
                index += direction

                if ignore == None:
                    if self.char_at(index) in fonts.charset["symbolic"] + " ":
                        ignore = " "
                elif self.char_at(index) not in ignore:
                    break
            
            return index
        
        if event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
            if event.key == pygame.K_BACKSPACE:
                index = self.index - 1
                
                if index < 0:
                    return
                
                direction = -1
            else:
                index = self.index

                if index >= self.length:
                    return
                
                direction = 1
            
            self.value = str_remove_at(self.value, index)
            if direction == -1:
                index -= 1

            if event.mod & pygame.KMOD_CTRL:
                target_index = find_next_index(index, direction)
                
                while index != target_index:
                    self.value = str_remove_at(self.value, index)
                    
                    if direction == -1:
                        index -= 1
                    else:
                        target_index -= direction
            
            if direction == -1:
                self.index = index + 1
            else:
                self.index = index

        elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            direction = -1 if event.key == pygame.K_LEFT else 1

            if direction == -1 and self.index <= 0:
                return
            elif direction == 1 and self.index >= self.length:
                return
            
            self.index += direction

            if event.mod & pygame.KMOD_CTRL:
                self.index = find_next_index(self.index, direction)

        elif event.unicode != "" and event.unicode in self.charset and self.length < self.max_chars:
            self.value = self.value[:self.index] + event.unicode + (self.value[self.index:] if self.length > self.index + 1 else "")
            self.index += 1
        else:
            return
        
        self.value = self.value[0:self.max_chars]

        self.cursor_text.move_to(add_coords(self.rect.topleft, (self.font.width * (self.index + 3), 0)))
        self.cursor_text.visible = True
        self.cursor_timer.value = -0.25
        self.value_text.value = self.value
    
    def update(self, dt: float, events: list[Event]):
        super().update(dt, events)

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
