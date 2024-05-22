from enum import Enum

from ..common import *
from ..fonts import *

from . import Component

class Currency(Component):
    class _Unit:
        def __init__(self, name: str, nickname: str, color: ColorValue, value: int):
            self.name = name
            self.nickname = nickname
            self.color = pygame.Color(color)
            self.value = value

    celest = _Unit("celest", "peak", "dodgerblue", 1000000)
    aural = _Unit("aural", "crown", "gold", 10000)
    argent = _Unit("argent", "shiner", "silver", 250)
    lumen = _Unit("lumen", "lump", "slategray", 25)
    copper = _Unit("copper", "bit", "chocolate1", 1)

    Units = [
        celest,
        aural,
        argent,
        lumen,
        copper,
    ]

    UnitValue = Literal[
        "sapphire",
        "aural",
        "argent",
        "lumen",
        "copper",
    ]
    
    def __init__(self, value: int = 0):
        super().__init__()
        self.value = value
    
    def __str__(self):
        return self.to_text()

    def to_text(self, use_nicknames = False) -> str:
        if self.value == 0:
            return Currency.Units[-1].nickname if use_nicknames else Currency.Units[-1].name

        value = abs(self.value)
        units = []

        for unit in Currency.Units:
            if value >= unit.value:
                num = value // unit.value
                value -= num * unit.value
                units.append(f"{num} {unit.nickname if use_nicknames else unit.name}{'s' if value != 1 else ''}")
        
        if len(units) == 1:
            return units[0]
        elif len(units) == 2:
            return units[0] + " and " + units[1]
        else:
            return ", ".join(units[:-1]) + "and " + units[-1]
