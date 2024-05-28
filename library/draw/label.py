from ..common import *

from . import DrawSurface, Font

class Label(DrawSurface):
    def __init__(self, font: Font, text: str, dest: Coordinate = (0, 0), color: ColorValue = "white"):
        super().__init__(font.text(text), dest)
        self.color = color
        self._text = text
        self.text = text
        self._font = font
        self.font = font
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value: str):
        if value != self._text:
            self._text = value
            self.update_surface(self.font.text(value))
    
    @property
    def font(self):
        return self._font
    
    @font.setter
    def font(self, value: Font):
        if value != self._font:
            self._font = value
            self.update_surface(self.font.text(self.text))
