import math
import re

from ..common import *

from . import Sheet
from . import Draw

class Font:
    def __init__(self, char_sheet: Sheet, chars: str, icon_sheet: Sheet, icons: list[str]):
        self.char_sheet: Sheet = char_sheet
        self.icon_sheet: Sheet = icon_sheet
        self.chars: dict[str, int] = {chars[i]: i for i in range(len(chars))}
        self.icons: dict[str, int] = {icons[i]: i for i in range(len(icons))}

        if char_sheet.size != icon_sheet.size:
            raise ValueError("Sheet sprite sizes do not match.")

        self.size = char_sheet.size
        self.width = self.size[0]
        self.height = self.size[1]
    
    def text(self, string: str) -> Surface:
        if len(string) == 0:
            return Surface((0, 0), pygame.SRCALPHA)

        # Splitting strings by newlines
        
        if "\n" in string:
            surfaces = [self.text(line) for line in string.split("\n")]
            width = max([surface.get_width() for surface in surfaces])
            height = len(surfaces) * self.height
            surface = Surface((width, height), pygame.SRCALPHA)

            for i in range(len(surfaces)):
                surface.blit(surfaces[i], (0, i * self.height))
            
            return surface
        
        # Parse string for icons etc

        pattern = re.compile(r"/([ic])\[([^\]]+)\]")
        
        surfaces: list[Surface] = []
        colors: dict[int, ColorValue] = {}
        
        i = 0
        c = 0
        while i < len(string):
            match = pattern.match(string[i:])

            if match != None:
                if match.group(1) == "i":
                    surfaces.append(self.icon_sheet.sprite(self.icons[match.group(2)]))
                elif match.group(1) == "c":
                    colors[c] = match.group(2)
                    c -= 1
                
                i += match.end() - match.start()
            else:
                if string[i] not in self.chars:
                    print(string)
                    raise AttributeError(f"'{string[i]} not found in font.'")

                surfaces.append(self.char_sheet.sprite(self.chars[string[i]]))
                i += 1
            
            c += 1

        # Get the dimensions of the new surface

        width = len(surfaces) * self.width
        height = math.ceil(len(surfaces) * self.width / width) * self.height
        cols = width / self.width

        # Create the new surface and blit the characters

        surface = Surface((width, height), pygame.SRCALPHA)
        color = "white"

        for i in range(len(surfaces)):
            if colors.get(i) != None:
                color = colors[i]

            char_surface = surfaces[i].copy()

            if color != "white":
                replace_color(char_surface, "white", color)

            x = (i % cols) * self.width
            y = math.floor(i / cols) * self.height
            surface.blit(char_surface, (x, y))
        
        return surface
