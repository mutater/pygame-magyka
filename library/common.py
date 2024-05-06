from typing import Union, Tuple, Sequence
import pygame

Coordinate = Union[Tuple[float, float], Sequence[float], pygame.Vector2]

RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[pygame.Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]

def replace_color(source: pygame.Surface, old: ColorValue, new: ColorValue):
    if not isinstance(old, pygame.Color):
        try:
            old = pygame.Color(old)
        except ValueError:
            old = pygame.Color("white")
    
    if not isinstance(new, pygame.Color):
        try:
            new = pygame.Color(new)
        except ValueError:
            new = pygame.Color("white")

    for x in range(source.get_width()):
        for y in range(source.get_height()):
            if source.get_at((x, y)) == old:
                source.set_at((x, y), new)
