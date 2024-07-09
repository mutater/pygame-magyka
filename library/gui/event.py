from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Point

class Event:
    """
    An object for representing events. Each event has a numeric type and various attributes.

    | Name        | Attributes   |
    | :---------- | :----------- |
    | Quit        | ~            |
    | KeyDown     | key, mods    |
    | KeyUp       | key, mods    |
    | MouseMove   | pos, buttons |
    | MouseDown   | pos, button  |
    | MouseUp     | pos, button  |
    """

    class Type:
        """
        An enum of event types, which contains the following:

        Quit, KeyDown, KeyUp, MouseMove, MouseDown, MouseUp
        """
        
        Quit = 0
        KeyDown = 1
        KeyUp = 2
        MouseMove = 3
        MouseDown = 4
        MouseUp = 5
    
    def __init__(self, type: int, **kwargs):
        self.key: str
        self.mods: list[str]
        self.pos: Point
        self.buttons: list[int]
        self.button: int

        for k, v in kwargs:
            setattr(self, k, v)
        
        self.type = type
        self.is_handled = False
