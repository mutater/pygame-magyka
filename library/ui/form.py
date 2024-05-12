from library.common import Event
from ..common import *
from . import Interact, Group

class Form(Group):
    def __init__(self):
        super().__init__()

        self.clear_keys()

        def select_next(event: Event):
            self.select_next()
        
        def select_next_not_group(event: Event):
            if not isinstance(self.selected_item, Group):
                self.select_next()
            
        def select_prev(event: Event):
            self.select_prev()
        
        def select_prev_not_group(event: Event):
            if not isinstance(self.selected_item, Group):
                self.select_prev()

        def unselect_all(event: Event):
            if self.selected_item == None or self.selected_item.selected == False:
                self.unselect_all_but()

        self.add_key(pygame.K_TAB, select_next)
        self.add_key(pygame.K_TAB, select_prev, pygame.KMOD_SHIFT)
        self.add_key(pygame.K_DOWN, select_next_not_group)
        self.add_key(pygame.K_UP, select_prev_not_group)
        self.add_key(pygame.K_ESCAPE, unselect_all)
    
    def add_item(self, interacts: Interact | list[Interact]) -> Self:
        for interact in to_list(interacts):
            if self.selected_item == None:
                super().add_item(interact)
                self.select_first()
            else:
                super().add_item(interact)
        
        return self
