from typing import Protocol, Callable, Type, Self, TypeVar, overload
import math
import pygame
import random

Coordinate = tuple[float, float]

_CanBeRect = pygame.Rect | tuple[float, float, float, float] | tuple[Coordinate, Coordinate]

class _HasRectAttribute(Protocol):
    rect: _CanBeRect | Callable[[], _CanBeRect]

RectValue = _CanBeRect | _HasRectAttribute

ColorValue = pygame.Color | tuple[int, int, int] | str

IntOrList = int | list[int]

Event = pygame.event.Event
Surface = pygame.Surface

def replace_color(source: Surface, old: ColorValue, new: ColorValue):
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

def add_coords(coord_a: Coordinate, coord_b: Coordinate) -> Coordinate:
    return (coord_a[0] + coord_b[0], coord_a[1] + coord_b[1])

def mul_coords(coord_a: Coordinate, coord_b: Coordinate) -> Coordinate:
    return (coord_a[0] * coord_b[0], coord_a[1] * coord_b[1])

def div_coords(coord_a: Coordinate, coord_b: Coordinate) -> Coordinate:
    return (coord_a[0] / coord_b[0], coord_a[1] / coord_b[1])

def rand(low: float | tuple[float, float], high: float | None = None, places: int = -1) -> float:
    if isinstance(low, tuple):
        low, high = low[0], low[1]
    
    if high != None:
        if low == high:
            return low
        elif low > high:
            low, high = high, low
    else:
        low, high = 0, low

    number = low + (high - low) * random.random()
    if places:
        number = round(number, places)
    
    return number

T = TypeVar('T')
def to_list(value: T | list[T]) -> list[T]:
    if not isinstance(value, list):
        return [value]
    else:
        return value

def to_int(value: tuple[float, float]) -> tuple[int, int]:
    return (math.floor(value[0]), math.floor(value[1]))

def str_remove_at(string: str, i: int) -> str:
    return string[:i] + string[i + 1:]

def clamp(value: float, low: float, high: float) -> float:
    return max(min(value, high), low)

def cmd_color(color: ColorValue) -> str:
    color = pygame.Color(color)
    return f"/c[{to_hex(color)}]"

def cmd_icon(icon: str) -> str:
    return f"/i[{icon}]"
