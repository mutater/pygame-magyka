from ..common import *

from . import Draw, Font

class Text(Draw):
    def __init__(self, font: Font, value: str, dest: Coordinate = (0, 0)):
        super().__init__(font.text(value), dest)
        self._value = value
        self.value = value
        self._font = font
        self.font = font
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str):
        if value != self._value:
            self._value = value
            self.update_surface(self.font.text(value))
    
    @property
    def font(self):
        return self._font
    
    @font.setter
    def font(self, value: Font):
        if value != self._font:
            self._font = value
            self.update_surface(self.font.text(self.value))