from ..common import *
from ..fonts import *

from . import Component, Experience

class Level(Component):
    def __init__(self):
        self.exp = Experience()
        self._value = 1
    
    def __add__(self, value: int) -> int:
        return self.value + value
    
    def __iadd__(self, value: int) -> Self:
        self.value += value
        return self
    
    def __sub__(self, value: int) -> int:
        return self.value - value

    def __isub__(self, value: int) -> Self:
        self.value -= value
        return self
    
    def __mul__(self, value: int) -> int:
        return self.value * value
    
    def __imul__(self, value: int) -> Self:
        self.value *= value
        return self
    
    def __str__(self) -> str:
        return f"{self.value}"
    
    def __eq__(self, value) -> bool:
        return self.value.__eq__(value)
    
    def __lt__(self, value) -> bool:
        return self.value.__lt__(value)
    
    def __gt__(self, value) -> bool:
        return self.value.__gt__(value)
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: int):
        self._value = value