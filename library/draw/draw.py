from library.common import *

class Draw:
    def __init__(self, dest: Coordinate, size: Coordinate):
        self.rect = pygame.Rect(dest[0], dest[1], size[0], size[1])
        
        self._color = pygame.Color("white")
        
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.draw_surface = pygame.Surface(size, pygame.SRCALPHA)
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        if self.color != value:
            self.color = value
            replace_color(self.draw_surface, (255, 255, 255), self.color)

    def draw(self, surface: pygame.Surface, offset: Coordinate = (0, 0)):
        surface.blit(self.draw_surface, add_coords(self.rect.topleft, offset))