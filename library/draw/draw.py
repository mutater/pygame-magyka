from ..common import *

class Draw:
    @overload
    def __init__(self, value: Self, /): ...
    
    @overload
    def __init__(self, surface: Coordinate | Surface, dest: Coordinate = (0, 0), /): ...

    def __init__(self, *args):
        if isinstance(args[0], Draw):
            self = args[0].copy()
            return

        surface: Coordinate | Surface = args[0]
        dest: Coordinate = args[1]

        self._color = pygame.Color("white")

        if isinstance(surface, Surface):
            self.rect = pygame.Rect(dest, surface.get_size())
            self.update_surface(surface.copy())
        else:
            self.rect = pygame.Rect(dest, surface)
            self.update_surface(Surface(surface, pygame.SRCALPHA))
        
        self.visible = True
    
    def update(self, draw: Self):
        self.rect.topleft = draw.rect.topleft
        self.surface = draw.surface.copy()

    def update_surface(self, surface: Surface | Self):
        if isinstance(surface, Surface):
            self.surface = surface.copy()
        else:
            self.surface = surface.surface.copy()
        
        self._draw_surface = self.surface

        self._update_color(self._color)
    
    def _update_color(self, color: ColorValue):
        self._color = pygame.Color(color)
        self._draw_surface = self.surface.copy()
        replace_color(self._draw_surface, (255, 255, 255), color)

    def copy(self) -> Self:
        return self.__class__(self.surface.copy(), self.rect.topleft)

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color: pygame.Color):
        if self._color != color:
            self._update_color(color)

    def get_width(self) -> int:
        return self.surface.get_width()
    
    def get_height(self) -> int:
        return self.surface.get_height()

    def blit(self, surface: Surface, dest: Coordinate):
        self.surface.blit(surface, dest)
        self._draw_surface = self.surface.copy()
    
    def move(self, offset: Coordinate) -> Self:
        self.rect.move_ip(offset)
        return self
    
    def move_to(self, dest: Coordinate) -> Self:
        self.rect.update(dest, self.rect.size)
        return self

    def draw(self, surface: Surface):
        if self.visible:
            surface.blit(self._draw_surface, self.rect.topleft)

DrawOrList = Draw | list[Draw]