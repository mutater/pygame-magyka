from library.common import *
from . import Interact, Group

class Form(Group):
    def __init__(self):
        super().__init__()

        self.clear_keys()
        self.add_key(pygame.K_TAB, self.select_next)
    
    def add_item(self, interact: Interact):
        if self.selected_item == None:
            super().add_item(interact)
            self.select_first()
        else:
            super().add_item(interact)

    def select_next(self, event: pygame.event.Event):
        super().select_next(event)
        
        if (isinstance(self.selected_item, Group)):
            self.selected_item.select_first()
