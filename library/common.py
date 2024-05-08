from typing import Union, Tuple, List, Dict, Sequence, Protocol, Callable, Optional, Literal
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

RGBColorValue = Union[pygame.Color, Tuple[int, int, int]]
ColorValue = Union[RGBColorValue, str, Sequence[int]]

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

def to_hex(color: ColorValue):
    if not isinstance(color, pygame.Color):
        color = pygame.Color(color)
    
    return f"#{color.r:02X}{color.g:02X}{color.b:02X}"

def to_list(var) -> List:
    return var if type(var) is list else [var]

def add_coords(coord_a: Coordinate, coord_b: Coordinate) -> Coordinate:
    return (coord_a[0] + coord_b[0], coord_a[1] + coord_b[1])
