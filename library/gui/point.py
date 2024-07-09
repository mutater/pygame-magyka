from ..common import *

class Point:
    @overload
    def __init__(self, point: Self, /): ...

    @overload
    def __init__(self, x_y: tuple[int, int], /): ...

    @overload
    def __init__(self, x: int = 0, y: int = 0, /): ...

    def __init__(self, *args):
        if isinstance(args[0], Point):
            self.x = args[0].x
            self.y = args[0].y
        elif isinstance(args[0], tuple):
            self.__init__(*args[0])
        elif len(args) == 2:
            for arg in args:
                if not isinstance(arg, int):
                    raise ValueError(f"Expected two integer values, received x={type(args[0])} and y={type(args[1])}.")
            
            self.x = int(args[0])
            self.y = int(args[1])
        else:
            raise TypeError("Expected a Point or two integer values.")

    def clamp_low(self, low: tuple[int, int] | Self = (0, 0)):
        if isinstance(low, Point):
            self.x = max(self.x, low.x)
            self.y = max(self.y, low.y)
        else:
            self.x = max(self.x, low[0])
            self.y = max(self.y, low[1])
    
    def clamp_high(self, high: tuple[int, int] | Self = (0, 0)):
        if isinstance(high, Point):
            self.x = min(self.x, high.x)
            self.y = min(self.y, high.y)
        else:
            self.x = min(self.x, high[0])
            self.y = min(self.y, high[1])

    def clamp(self, low: tuple[int, int] | Self = (0, 0), high: tuple[int, int] | Self = (0, 0)):
        self.clamp_low(low)
        self.clamp_high(high)
    
    def as_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

PointValue = tuple[int, int] | Point
