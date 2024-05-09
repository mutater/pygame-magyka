from library.common import *

class Draw:
    def __init__(self, dest: Coordinate, size: Coordinate):
        self.rect = pygame.Rect(dest[0], dest[1], size[0], size[1])
        
        self._color = pygame.Color("black")
        
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.draw_surface = pygame.Surface(size, pygame.SRCALPHA)

        self.color = pygame.Color("white")
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        if self._color != value:
            self._color = value
            self.draw_surface = self.surface.copy()
            replace_color(self.draw_surface, (255, 255, 255), value)

    def get_width(self) -> int:
        return self.surface.get_width()
    
    def get_height(self) -> int:
        return self.surface.get_height()

    def blit(self, surface: pygame.Surface, dest: Coordinate):
        self.surface.blit(surface, dest)
        self.draw_surface = self.surface.copy()
    
    def move(self, offset: Coordinate):
        self.rect.move_ip(offset)
    
    def move_to(self, dest: Coordinate):
        self.rect.update(dest, self.rect.size)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.draw_surface, self.rect.topleft)
