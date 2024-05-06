from typing import Union, Tuple, List, Dict, Sequence, Protocol, Callable
import pygame

Coordinate = Union[Tuple[float, float], Sequence[float], pygame.Vector2]

_CanBeRect = Union[
    pygame.Rect,
    Tuple[Union[float, int], Union[float, int], Union[float, int], Union[float, int]],
    Tuple[Coordinate, Coordinate],
    Sequence[Union[float, int]],
    Sequence[Coordinate],
]

class _HasRectAttribute(Protocol):
    rect: Union[_CanBeRect, Callable[[], _CanBeRect]]

RectValue = Union[_CanBeRect, _HasRectAttribute]

RGBAOutput = Tuple[int, int, int, int]
RGBColorValue = Union[pygame.Color, Tuple[int, int, int]]
ColorValue = Union[pygame.Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]

InputCodeValue = Union[int, Tuple[int, int]]

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

def rgb_to_hex(rgb: ColorValue):
    if not isinstance(rgb, pygame.Color):
        rgb = pygame.Color(rgb)
    
    return f"#{rgb.r:02X}{rgb.g:02X}{rgb.b:02X}"
