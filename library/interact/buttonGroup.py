from library.common import *
from library.font import Font
from library.interact.interact import EventCallbackValue
from library.interact.button import Button
from library.interact.group import Group
from library.interact.key import Key

ButtonActionValue = Tuple[str, str, int, EventCallbackValue]

class ButtonGroup(Group):
    def __init__(self, dest: Coordinate, font: Font, interacts: List[ButtonActionValue]):
        super().__init__(dest)

        self.font = font

        for i in range(len(interacts)):
            letter = interacts[i][0]
            word = interacts[i][1]
            key_code = interacts[i][2]
            callbacks = interacts[i][3]

            interact_button = Button(
                (self.rect.left, self.rect.top + i * font.height * 2),
                font.text(f"[{letter}] {word}"),
                callbacks
            )

            interact_key = Key(
                key_code,
                callbacks
            )

            self.add_item(interact_button)
            self.add_interact(interact_key)
