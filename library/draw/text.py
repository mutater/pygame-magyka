from library.common import *
from library.draw.draw import Draw

class Text(Draw):
    def __init__(self, dest: Coordinate, size: Coordinate):
        super().__init__(dest, size)
    
    def blit(self, surface: pygame.Surface, dest: Coordinate):
        self.surface.blit(surface, dest)

    def draw(self, surface: pygame.Surface, offset: Coordinate = (0, 0)):
        surface.blit(self.draw_surface, add_coords(self.dest, offset))
    
    def get_width(self) -> int:
        return self.surface.get_width()
    
    def get_height(self) -> int:
        return self.surface.get_height()
