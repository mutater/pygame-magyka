from ..common import *

from . import EventCallbackOrList, Button, Key, Group

from ..draw import Font, Label

ButtonActionValue = tuple[str, str, int, EventCallbackOrList]

class ButtonGroup(Group):
    def __init__(self, dest: Coordinate, font: Font, interacts: list[ButtonActionValue]):
        super().__init__()

        self.rect = pygame.Rect(dest[0], dest[1], 0, 0)

        for i in range(len(interacts)):
            letter = interacts[i][0]
            word = interacts[i][1]
            key_code = interacts[i][2]
            callbacks = interacts[i][3]
            position = (self.rect.left, self.rect.top + i * font.height * 2)

            self.add_item(Button(
                position,
                Label(font, f"[{letter}] {word}"),
                callbacks
            ))

            self.add_interact(Key(
                key_code,
                callbacks
            ))

            if i < len(interacts) - 1:
                self.add_draw(Label(font, "|", add_coords(position, (font.width, font.height))))

