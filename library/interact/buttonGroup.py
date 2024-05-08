from library.common import *
from library.font import Font
from library.interact.interact import EventCallbackValue
from library.interact.button import Button
from library.interact.group import Group
from library.interact.Key import Key

ButtonActionValue = Tuple[str, str, int, EventCallbackValue]

class ButtonGroup(Group):
    def __init__(self, dest: Coordinate, font: Font, inputs_data: List[ButtonActionValue]):
        super().__init__(dest)

        self.font = font

        y_position = self.rect.top

        for data in inputs_data:
            interact_button = Button((self.rect.left, y_position), font.text(f"[{data[0]}] {data[1]}"), data[3])
            interact_key = Key([data[2]], data[3])

            y_position += font.height
            
            self.add_item(interact_button)
            self.add_interact(interact_key)
