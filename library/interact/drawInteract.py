from library.common import *
from library.draw import Draw, DrawValue, DrawsValue
from . import Interact

class DrawInteract(Interact):
    def __init__(self):
        super().__init__()
        self.color = pygame.Color("white")
        self.color_disabled = pygame.Color("darkgray")
        self.color_normal = pygame.Color("white")
        self.color_selected = pygame.Color("#BBDDFF")
        self.color_highlighted = self.color_selected
        self.color_pressed = pygame.Color("#8899AA")

        self.draws: List[Draw] = []

    # Getters / Setters

    def on_enabled(self):
        super().on_enabled()
        self.color = self.color_normal if self.selected else self.color_normal
    
    def on_disabled(self):
        super().on_disabled()
        self.color = self.color_disabled

    def on_pressed(self):
        super().on_pressed()
        if self.enabled:
            self.color = self.color_pressed
    
    def on_released(self):
        super().on_released()
        if self.enabled:
            if self.selected:
                self.color = self.color_selected
            elif self.highlighted:
                self.color = self.color_highlighted
            else:
                self.color = self.color_normal
    
    def on_selected(self):
        super().on_selected()
        if self.enabled and not self.pressed:
            self.color = self.color_selected
    
    def on_unselected(self):
        super().on_unselected()
        if self.enabled and not self.pressed and not self.highlighted:
            self.color = self.color_normal

    def on_highlighted(self):
        super().on_highlighted()
        if self.enabled and not self.pressed:
            self.color = self.color_highlighted
        
    def on_unhighlighted(self):
        super().on_unhighlighted()
        if self.enabled and not self.pressed and not self.selected:
            self.color = self.color_normal
    
    # Methods

    def add_draw(self, draw: DrawValue):
        if isinstance(draw, tuple):
            draw = Draw(draw[0], draw[1])

        self.draws.append(draw)
    
    def add_draws(self, draws: DrawsValue):
        if not isinstance(draws, list):
            draws = [draws]

        for draw in draws:
            self.add_draw(draw)
    
    def clear_draws(self):
        self.draws.clear()

    def set_draws_color(self, color: ColorValue):
        for draw in self.draws:
            draw.color = pygame.Color(color)
    
    def get_draws_rect(self):
        if len(self.draws) == 0:
            return pygame.Rect(0, 0, 0, 0)
        elif len(self.draws) == 1:
            return self.draws[0].rect.copy()
        
        left = self.draws[0].rect.left
        top = self.draws[0].rect.top

        for draw in self.draws:
            left = min(left, draw.rect.left)
            top = min(top, draw.rect.top)
        
        width = self.draws[0].rect.width
        height = self.draws[0].rect.height

        for draw in self.draws:
            width = max(width, draw.rect.right - left)
            height = max(height, draw.rect.bottom - height)
        
        return pygame.Rect(left, top, width, height)
    
    def draw(self, surface: pygame.Surface):
        for draw in self.draws:
            draw.draw(surface)
