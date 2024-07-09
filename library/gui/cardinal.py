from ..common import *

class Cardinal():
    @overload
    def __init__(self, up: int = 0, down: int = 0, left: int = 0, right: int = 0, /): ...

    @overload
    def __init__(self, up_down_left_right: tuple[int, int, int, int]): ...

    @overload
    def __init__(self, cardinal: Self, /): ...

    def __init__(self, *args):
        if isinstance(args[0], Cardinal):
            self.set(args[0].up, args[0].down, args[0].left, args[0].right)
        elif isinstance(args[0], tuple):
            self.__init__(*args[0])
        elif len(args) == 4:
            for arg in args:
                if not isinstance(arg, int):
                    raise ValueError(f"Expected four integer values, received an arg of type {type(arg)}.")
            
            self.set(int(args[0]), int(args[1]), int(args[2]), int(args[3]))
        else:
            raise TypeError("Expected a Cardinal or four integer values.")
    
    def set(self, up: int | None, down: int | None, left: int | None, right: int | None):
        if up != None:
            self.up = max(0, up)
        if down != None:
            self.down = max(0, down)
        if left != None:
            self.left = max(0, left)
        if right != None:
            self.right = max(0, right)

CardinalValue = tuple[int, int, int, int] | Cardinal
