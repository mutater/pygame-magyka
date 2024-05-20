from ..common import *

class Draw:
    @overload
    def __init__(self, surface: Coordinate | Surface, dest: Coordinate = (0, 0), /): ...
    
    @overload
    def __init__(self, value: Self, /): ...

    def __init__(self, *args):
        self.name = ""
        
        if isinstance(args[0], Draw):
            self = args[0].copy()
            return

        surface: Coordinate | Surface = args[0]
        dest: Coordinate = args[1]

        self._color = pygame.Color("white")
        self._align = "topleft"

        if isinstance(surface, Surface):
            self.rect = pygame.Rect(dest, surface.get_size())
            self.update_surface(surface.copy())
        else:
            self.rect = pygame.Rect(dest, surface)
            self.update_surface(Surface(surface, pygame.SRCALPHA))
        
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
        color = pygame.Color(color)
        if self._color != color:
            self._update_color(color)

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
        return self.surface.get_width()
    
    @property
    def height(self) -> int:
        return self.surface.get_height()
    
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

    def update(self, draw: Self):
        self.dest = draw.dest
        self.surface = draw.surface.copy()

    def update_surface(self, surface: Surface | Self):
        dest = self.dest
        
        if isinstance(surface, Surface):
            self.surface = surface.copy()
        else:
            self.surface = surface.surface.copy()
        
        self._update_color(self._color)

        self.rect = pygame.Rect((0, 0), self.surface.get_size())
        self.dest = dest
    
    def _update_color(self, color: ColorValue):
        self._color = pygame.Color(color)
        self._draw_surface = self.surface.copy()
        replace_color(self._draw_surface, (255, 255, 255), color)

    def copy(self) -> Self:
        return self.__class__(self.surface.copy(), self.rect.topleft)

    def blit(self, surface: Surface, dest: Coordinate):
        self.surface.blit(surface, dest)
        self._draw_surface = self.surface.copy()
    
    def move(self, offset: Coordinate) -> Self:
        self.dest = add_coords(self.dest, offset)
        return self
    
    def move_to(self, dest: Coordinate) -> Self:
        self.dest = dest
        return self

    def draw(self, surface: Surface):
        if self.visible:
            surface.blit(self._draw_surface, self.rect.topleft)

DrawOrList = Draw | list[Draw]
