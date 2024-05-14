from ..common import *
from . import Interact, DrawInteract

class Group(DrawInteract):
    def __init__(self):
        super().__init__()

        self.rect = pygame.Rect(0, 0, 0, 0)
        
        self.interacts: list[Interact] = []
        self.items: list[Interact] = []

        self.first_item: Interact | None = None
        self.last_item: Interact | None = None
        self.selected_item: Interact | None = None

        def select_next(event: Event):
            self.select_next()
            
        def select_prev(event: Event):
            self.select_prev()

        def unselect_all(event: Event):
            self.unselect_all_but()

        self.add_key(pygame.K_DOWN, select_next)
        self.add_key(pygame.K_UP, select_prev)
        self.add_key(pygame.K_ESCAPE, unselect_all)

        self.selected = True
    
    # Events

    def _on_selected(self, event: Event):
        super()._on_selected(event)
        self.select_first()

    def _on_unselected(self, event: Event):
        super()._on_unselected(event)
        self.unselect_all_but(None)
    
    def _on_event(self, event: Event):
        if not self.enabled or event == None:
            return
        
        if self.selected:
            self._on_key_event(event)

        if event.type == pygame.MOUSEMOTION:
            self.unselect_all_but(self.selected_item)

    # Methods

    def add_interact(self, interacts: Interact | list[Interact]) -> Self:
        for interact in to_list(interacts):
            self.interacts.append(interact)

        return self

    def add_item(self, interacts: Interact | list[Interact]) -> Self:
        for interact in to_list(interacts):
            self.add_interact(interact)
            self.items.append(interact)
            
            if self.first_item == None or self.last_item == None:
                self.first_item = interact
                self.last_item = interact
            
            interact.next = self.first_item
            interact.prev = self.last_item
            
            self.last_item.next = interact
            self.first_item.prev = interact
            self.last_item = interact

        return self
    
    def select_item(self, item: Interact | None):
        if self.selected_item != None:
            self.selected_item.selected = False
        
        if item != None:
            item.selected = True
        
        self.selected_item = item

    def select_next(self):
        pygame.mouse.set_visible(False)
        self.select_item(self.first_item if self.selected_item == None else self.selected_item.next)
    
    def select_prev(self):
        pygame.mouse.set_visible(False)
        self.select_item(self.last_item if self.selected_item == None else self.selected_item.prev)
    
    def select_first(self):
        if self.first_item != None:
            self.select_item(self.first_item)

    def unselect_all_but(self, item: Interact | None = None):
        for i in self.items:
            if i != item:
                i.selected = False
        
        if item != self.selected_item:
            self.selected_item = None

    def update(self, dt: float, events: list[Event]):
        super().update(dt, events)

        for interact in self.interacts:
            interact.update(dt, events)

    def draw(self, surface: Surface):
        for draw in self.draws:
            draw.draw(surface)

        for interact in self.interacts:
            if isinstance(interact, DrawInteract):
                interact.draw(surface)
