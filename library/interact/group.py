from library.common import *
from library.interact.interact import Interact

class Group(Interact):
    def __init__(self, dest: Coordinate):
        super().__init__()
        
        self.rect = pygame.Rect(dest[0], dest[1], 0, 0)
        
        self.interacts: List[Interact] = []
        self.items: List[Interact] = []

        self.start_item: Interact | None = None
        self.end_item: Interact | None = None
        self.selected_item: Interact | None = None

        self.add_key(pygame.K_DOWN, self.next_item)
        self.add_key(pygame.K_UP, self.prev_item)
    
    def add_interacts(self, interacts: List[Interact]):
        for interact in interacts:
            self.add_interact(interact)
    
    def add_interact(self, interact: Interact):
        self.interacts.append(interact)

    def add_items(self, interacts: List[Interact]):
        for interact in interacts:
            self.add_item(interact)

    def add_item(self, interact: Interact):
        self.add_interact(interact)
        self.items.append(interact)
        
        if self.start_item == None or self.end_item == None:
            self.start_item = interact
            self.end_item = interact
        
        interact.next = self.start_item
        interact.prev = self.end_item
        
        self.end_item.next = interact
        self.start_item.prev = interact
        self.end_item = interact
    
    def next_item(self, event: pygame.event.Event):
        self.set_selected_item(self.start_item if self.selected_item == None else self.selected_item.next)
    
    def prev_item(self, event: pygame.event.Event):
        self.set_selected_item(self.end_item if self.selected_item == None else self.selected_item.prev)
    
    def set_selected_item(self, new_selected: Interact | None):
        if not self.enabled or not self.selected:
            return

        if self.selected_item != None:
            self.selected_item.selected = False
        
        if new_selected != None:
            new_selected.selected = True
        
        self.selected_item = new_selected

    def on_event(self, event: pygame.event.Event):
        if not self.enabled or not self.selected:
            return
        
        super().on_event(event)

        if event.type == pygame.MOUSEMOTION:
            for item in self.items:
                if item != self.selected_item:
                    item.selected = False

        for interact in self.interacts:
            interact.on_event(event)

        if event.type == pygame.MOUSEMOTION:
            for item in self.items:
                if item != self.selected_item and item.selected:
                    self.set_selected_item(item)
                    break
    
    def draw(self, surface: pygame.Surface):
        for interact in self.interacts:
            interact.draw(surface)
