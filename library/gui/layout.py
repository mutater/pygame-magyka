from __future__ import annotations

from . import Cardinal, CardinalValue, Point, PointValue

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Widget

class _Layout:
    def __init__(self, margins: CardinalValue = (8, 8, 8, 8), padding: PointValue = (8, 8)):
        self.margins: Cardinal = Cardinal(margins)
        self.padding: Point = Point(padding)
        self.direction = 0

class HLayout(_Layout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.direction = 1

class VLayout(_Layout):
    def __init__(self):
        self.direction = 0
