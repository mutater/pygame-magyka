from ..common import *
from ..fonts import *
from ..valueContainer import ValueContainer

from . import Label, Font, Group

class Bar(Group):
    def __init__(self, value: float | ValueContainer, length: int, dest: Coordinate = (0, 0), color_empty: ColorValue = "gray24", color_filled: ColorValue = "lightgray", mode = "%"):
        super().__init__(dest)

        self.length = length
        self.mode = mode
        
        if isinstance(value, ValueContainer):
            self.value_container = value
            self.value_percent = value.percent
        else:
            self.value_container = None
            self.value_percent = clamp(value, 0, 100)
        
        self.color_empty = pygame.Color(color_empty)
        self.color_filled = pygame.Color(color_filled)
        
        self.text_empty = Label(fontm, "")
        self.text_empty.color = color_empty
        self.text_filled = Label(fontm, "")
        self.text_filled.color = color_filled
        self.text_value = Label(fonts, "0/0", (umx * (self.length), 0))
        self.text_value.align = "bottomright"

        self.add_draw([self.text_empty, self.text_filled, self.text_value])

        self._update_texts()

    def _update_texts(self):
        string_empty = cmd_icon("bar_left") + cmd_icon("bar_middle") * (self.length - 2) + cmd_icon("bar_right")
        string_filled = ""
        if math.ceil(self.value_percent * self.length) == self.length:
            string_filled = string_empty
        elif self.value_percent > 0:
            string_filled += cmd_icon("bar_left") + cmd_icon("bar_middle") * (math.ceil(self.value_percent * self.length) - 1)

        if self.value_container == None:
            string_value = f"{int(math.ceil(self.value_percent * 100))}%"
        else:
            if self.mode == "%":
                string_value = f"{int(math.ceil(self.value_percent * 100))}%"
            else:
                string_value = f"/c[darkgray]{self.value_container.int_value}/c[white]/{self.value_container.int_max}"

        self.text_empty.text = string_empty
        self.text_filled.text = string_filled
        self.text_value.text = string_value
        print(self.text_value.dest)
        self.text_value.dest = add_coords(self.dest, (umx * (self.length) - 3, umy - 1))

    def draw(self, surface: Surface):
        o_value_percent = self.value_percent
        
        if self.value_container != None:
            self.value_percent = self.value_container.percent
        
        if self.value_percent != o_value_percent:
            self._update_texts()
        
        super().draw(surface)
