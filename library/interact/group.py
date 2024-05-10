from library.common import *
from . import Interact, DrawInteract

class Group(DrawInteract):
    def __init__(self):
        super().__init__()

        self.rect = pygame.Rect(0, 0, 0, 0)
        
        self.interacts: List[Interact] = []
        self.items: List[Interact] = []

        self.first_item: Interact | None = None
        self.last_item: Interact | None = None
        self.selected_item: Interact | None = None

        self.add_key(pygame.K_DOWN, self.select_next)
        self.add_key(pygame.K_UP, self.select_prev)

        self.selected = True
    
    def _on_selected(self):
        super()._on_selected()
        self.select_first()

    def _on_unselected(self):
        super()._on_unselected()
        self.unselect_all_but(None)
    
    def add_interact(self, interacts: Interact | List[Interact]) -> Self:
        if not isinstance(interacts, list):
            interacts = [interacts]
        
        for interact in interacts:
            self.interacts.append(interact)

        return self

    def add_item(self, interacts: Interact | List[Interact]) -> Self:
        if not isinstance(interacts, list):
            interacts = [interacts]

        for interact in interacts:
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

    def select_next(self, event: pygame.event.Event):
        pygame.mouse.set_visible(False)
        self.select_item(self.first_item if self.selected_item == None else self.selected_item.next)
    
    def select_prev(self, event: pygame.event.Event):
        pygame.mouse.set_visible(False)
        self.select_item(self.last_item if self.selected_item == None else self.selected_item.prev)
    
    def select_first(self):
        if self.first_item != None:
            self.select_item(self.first_item)

    def unselect_all_but(self, item: Interact | None):
        for i in self.items:
            if i != item:
                i.selected = False

    def on_event(self, event: pygame.event.Event):
        if not self.enabled:
            return
        
        if self.selected:
            self.on_key_event(event)

        if event.type == pygame.MOUSEMOTION:
            self.unselect_all_but(self.selected_item)

        for interact in self.interacts:
            interact.on_event(event)

        if event.type == pygame.MOUSEMOTION:
            for item in self.items:
                if item != self.selected_item and item.selected:
                    self.select_item(item)
                    break
    
    def draw(self, surface: pygame.Surface):
        super().draw(surface)

        for interact in self.interacts:
            if isinstance(interact, DrawInteract):
                interact.draw(surface)
