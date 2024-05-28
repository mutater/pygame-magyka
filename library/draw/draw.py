from ..common import *

class Draw:
    def __init__(self, size: Coordinate, dest: Coordinate = (0, 0)):
        self._color = pygame.Color("white")
        self._align = "topleft"

        self.name = ""
        self.rect = pygame.Rect(dest, size)
        self.visible = True
    
    def named(self, name: str) -> Self:
        self.name = name
        return self
    
    # Getters / Setters

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color: ColorValue):
        self._color = pygame.Color(color)

    @property
    def dest(self) -> tuple[int, int]:
        return getattr(self.rect, self.align)
    
    @dest.setter
    def dest(self, dest: Coordinate):
        dest = int_coords(dest)

        if dest != self.dest:
            setattr(self.rect, self.align, int_coords(dest))

    @property
    def width(self) -> int:
        return self.rect.width
    
    @width.setter
    def width(self, value: float):
        self.rect.width = int(value)
    
    @property
    def height(self) -> int:
        return self.rect.height
    
    @height.setter
    def height(self, value: float):
        self.rect.height = int(value)
    
    @property
    def size(self) -> tuple[int, int]:
        return self.rect.size
    
    @size.setter
    def size(self, value: Coordinate):
        self.rect.size = int_coords(value)
    
    @property
    def align(self) -> str:
        return self._align
    
    @align.setter
    def align(self, value: str):
        if value in ["topleft", "bottomleft", "topright", "bottomright"]:
            self._align = value
        else:
            raise ValueError(f"'{value}' is not a valid alignment type.")

    # Methods
    
    def move(self, offset: Coordinate) -> Self:
        self.dest = add_coords(self.dest, offset)
        return self
    
    def move_to(self, dest: Coordinate) -> Self:
        self.dest = dest
        return self

    def draw(self, surface: Surface):
        pass

DrawOrList = Draw | list[Draw]
