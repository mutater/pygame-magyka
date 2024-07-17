from __future__ import annotations

from . import Cardinal, CardinalValue, Point, PointValue

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Widget

class Layout:
    horizontal = 0
    vertical = 1

    def __init__(self, widget: Widget, direction: int, margins: CardinalValue = (8, 8, 8, 8), padding: int = 8,\
                 expand: bool = False):
        self.widget: Widget = widget
        self.direction: int = direction
        self.margins: Cardinal = Cardinal(margins)
        self.padding: int = padding
        self.expand: bool = expand
    
    def draw(self):
        if self.widget == None or len(self.widget.children) == 0:
            return

        pos = "x" if self.direction == Layout.horizontal else "y"

        sizes = []
        total_size: int = 0
        max_size: int = getattr(self.widget.size, pos)

        if self.direction == Layout.horizontal:
            max_size -= self.margins.left + self.margins.right
        else:
            max_size -= self.margins.up + self.margins.down

        for child in self.widget.children:
            if not hasattr(child, "draw"):
                continue

            size = getattr(child.size, pos)
            sizes.append(size)
            total += size
        
        calc_padding = self.padding
        if self.expand:
            calc_padding = int((max_size - total_size) / (len(sizes) - 1))
        
        for child in self.widget.children:
            if not hasattr(child, "draw"):
                continue

            child.draw
