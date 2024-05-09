from library.common import *
from library.font import Font

from . import EventCallbackValue, Button, Key, Group

ButtonActionValue = Tuple[str, str, int, EventCallbackValue]

class ButtonGroup(Group):
    def __init__(self, dest: Coordinate, font: Font, interacts: List[ButtonActionValue]):
        super().__init__()

        self.rect = pygame.Rect(dest[0], dest[1], 0, 0)

        self.font = font

        for i in range(len(interacts)):
            letter = interacts[i][0]
            word = interacts[i][1]
            key_code = interacts[i][2]
            callbacks = interacts[i][3]
            position = (self.rect.left, self.rect.top + i * font.height * 2)

            interact_button = Button(
                position,
                font.text(f"[{letter}] {word}", position),
                callbacks
            )
            self.add_item(interact_button)

            interact_key = Key(
                key_code,
                callbacks
            )
            self.add_interact(interact_key)

            if i < len(interacts) - 1:
                bar = font.text("|", add_coords(position, (font.width, font.height)))
                self.add_draw(bar)

