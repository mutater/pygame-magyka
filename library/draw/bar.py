from ..common import *
from ..valueContainer import ValueContainer

from . import Label, Font

class Bar(Label):
    def __init__(self, font: Font, value: float | ValueContainer, length: int, dest: Coordinate = (0, 0), color_empty: ColorValue = "darkgray", color_filled: ColorValue = "lightgray"):
        super().__init__(font, "asdf", dest)

        self.length = length
        
        if isinstance(value, ValueContainer):
            self.value_container = value
            self.value_percent = value.percent
        else:
            self.value_container = None
            self.value_percent = clamp(value, 0, 100)
        
        self.color_empty = pygame.Color(color_empty)
        self.color_filled = pygame.Color(color_filled)
        
        self.text = self.__str__()

    def __str__(self) -> str:
        string = cmd_color(self.color_filled)

        for i in range(self.length):
            if i / self.length * 100 >= self.value_percent:
                string += cmd_color(self.color_empty)
            
            if i == 0:
                string += cmd_icon("bar_left")
            elif i == self.length - 1:
                string += cmd_icon("bar_right")
            else:
                string += cmd_icon("bar_middle")
        
        return string

    def draw(self, surface: Surface):
        o_value_percent = self.value_percent
        
        if self.value_container != None:
            self.value_percent = self.value_container.percent
        
        if self.value_percent != o_value_percent:
            self.text = self.__str__()
        
        super().draw(surface)
