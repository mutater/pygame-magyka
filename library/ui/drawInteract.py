from ..common import *

from ..draw import Draw, DrawOrList
from . import Interact

class DrawInteract(Interact):
    def __init__(self, dest: Coordinate = (0, 0)):
        super().__init__()

        self.color = pygame.Color("white")
        self.color_disabled = pygame.Color("darkgray")
        self.color_normal = pygame.Color("white")
        self.color_selected = pygame.Color("#BBDDFF")
        self.color_highlighted = self.color_selected
        self.color_pressed = pygame.Color("#8899AA")

        self.draws: list[Draw] = []
        self.draws_lookup: dict[str, Draw] = {}
        self.dest = dest

    # Getters / Setters

    @property
    def dest(self):
        return self.rect.topleft
    
    @dest.setter
    def dest(self, value: Coordinate):
        if value != self.rect.topleft:
            for draw in self.draws:
                draw.move(sub_coords(value, self.rect.topleft))
            self.rect.topleft = int_coords(value)

    # Events

    def _on_enabled(self, event: Event):
        super()._on_enabled(event)
        self.color = self.color_normal if self.selected else self.color_normal
    
    def _on_disabled(self, event: Event):
        super()._on_disabled(event)
        self.color = self.color_disabled

    def _on_pressed(self, event: Event):
        super()._on_pressed(event)
        if self.enabled:
            self.color = self.color_pressed
    
    def _on_released(self, event: Event):
        super()._on_released(event)
        if self.enabled:
            if self.selected:
                self.color = self.color_selected
            elif self.highlighted:
                self.color = self.color_highlighted
            else:
                self.color = self.color_normal
    
    def _on_selected(self, event: Event):
        super()._on_selected(event)
        if self.enabled and not self.pressed:
            self.color = self.color_selected
    
    def _on_unselected(self, event: Event):
        super()._on_unselected(event)
        if self.enabled and not self.pressed and not self.highlighted:
            self.color = self.color_normal

    def _on_highlighted(self, event: Event):
        super()._on_highlighted(event)
        if self.enabled and not self.pressed:
            self.color = self.color_highlighted
        
    def _on_unhighlighted(self, event: Event):
        super()._on_unhighlighted(event)
        if self.enabled and not self.pressed and not self.selected:
            self.color = self.color_normal
    
    # Methods

    def add_draw(self, draws: DrawOrList, offset: Coordinate | None = None):
        for draw in to_list(draws):
            if isinstance(draw, tuple):
                draw = Draw(draw[0], draw[1])

            if draw.name in self.draws_lookup:
                raise AttributeError(f"Draw with name '{draw.name}' already exists.")

            if offset != None:
                self.draws.append(draw.move(offset))
            else:
                self.draws.append(draw)
            
            if draw.name != "":
                self.draws_lookup[draw.name] = draw
    
    def get_draw(self, draw_type: type[T], name: str) -> T:
        if name == "":
            raise AttributeError("No name provided.")
        
        draw = self.draws_lookup.get(name, None)

        if draw == None or not isinstance(draw, draw_type):
            raise AttributeError(f"Draw of name '{name}' not found.")
        else:
            return draw

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
    
    def move(self, offset: Coordinate) -> Self:
        self.rect.move_ip(offset)
        return self
    
    def move_to(self, dest: Coordinate) -> Self:
        self.dest = dest
        return self

    def draw(self, surface: Surface):
        self.set_draws_color(self.color)

        for draw in self.draws:
            draw.draw(surface)
