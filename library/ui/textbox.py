from ..common import *
from ..constant import fonts
from ..timer import Timer

from . import DrawInteract
from ..draw import Font, Text

class Textbox(DrawInteract):
    def __init__(self, dest: Coordinate, font: Font, max_chars: int, value: str = "", charset: str = "all", blacklist: str = "", start = "> [", end = "]"):
        super().__init__(dest)

        self.font = font
        self._max_chars = max_chars
        self._value = ""
        self.value = value
        self._index: int = 0
        self.index = 0

        self.start = start
        self.end = end

        self.back_text = Text(font, f"{start}{' ' * self._max_chars}{end}")
        self.value_text = Text(font, self.value, (font.width * len(start), 0))
        self.cursor_text = Text(font, "_", (font.width * len(start), 0))
        self.cursor_timer = Timer(0.5)
        
        self.charset = fonts.get_charset(charset, blacklist)

        if self.charset == None:
            raise ValueError("Invalid charset.")
        
        self.add_draw(self.back_text, dest)
        self.add_draw(self.value_text, dest)
        self.add_draw(self.cursor_text, dest)

        self.rect = self.get_draws_rect()

    # Getters / Setters

    @property
    def max_chars(self):
        return self._max_chars
    
    @max_chars.setter
    def max_chars(self, value: int):
        if self._max_chars != value:
            self._max_chars = value
            if value < self.length:
                self.value = self.value[:value]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        if value != self._value:
            self._value = value[:self._max_chars]
            self.value_text.value = self._value
            self.index = self.index

    def set_value(self, value: str):
        self.value = value
        self.index = self.length

    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, value: int):
        o_index = self._index
        self._index = int(clamp(value, 0, self.length))
        
        if o_index != self._index:
            self.cursor_text.move_to(add_coords(self.rect.topleft, (self.font.width * (self.index + len(self.start)), 0)))

    @property
    def length(self):
        return len(self._value)

    def char_at(self, index: int | None = None):
        if index == None:
            index = self.index

        if index < 0 or index >= self.length:
            return ""
        return self._value[index]

    # Events

    def _on_key_event(self, event: Event):
        if event == None:
            return
        elif event.type != pygame.KEYDOWN:
            if event.type == pygame.KEYUP:
                reset_key_repeat()
            return

        def find_next_index(index: int, direction: int) -> int:
            ignore = None

            if index + direction >= self.length or index + direction < 0:
                pass
            elif self._value[index + direction] in fonts.get_charset("symbolic"):
                ignore = fonts.get_charset("symbolic")
            elif self.value[index + direction] == " ":
                ignore = " "

            while 0 <= index <= self.length:
                index += direction

                if ignore == None:
                    if self.char_at(index) in fonts.get_charset("symbolic") + " ":
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

        elif event.key in [pygame.K_x, pygame.K_c, pygame.K_v] and event.mod & pygame.KMOD_CTRL:
            match event.key:
                case pygame.K_x:
                    self.cut_value()
                case pygame.K_c:
                    self.copy_value()
                case pygame.K_v:
                    self.paste_value()

        elif event.unicode != "" and event.unicode in self.charset and self.length < self._max_chars:
            self.value = self.value[:self.index] + event.unicode + (self.value[self.index:] if self.length > self.index + 1 else "")
            self.index += 1
        
        else:
            return

        pygame.key.set_repeat(300, 40)
        self.cursor_text.visible = True
        self.cursor_timer.value = -0.25
    
    # Methods

    def cut_value(self):
        self.copy_value()
        self.value = ""
        self.index = 0

    def copy_value(self):
        pygame.scrap.put(pygame.SCRAP_TEXT, self.value.encode())

    def paste_value(self):
        value_bytes = pygame.scrap.get(pygame.SCRAP_TEXT)
        if value_bytes != None:
            value_string = value_bytes.decode()[:self.max_chars - self.length]
            self.value += value_string
            self.index += len(value_string)
    
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
