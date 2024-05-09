from library.common import *
from . import Interact, Group

class Form(Group):
    def __init__(self):
        super().__init__()

        self.clear_keys()
        self.add_key(pygame.K_TAB, self.select_next)
    
    def add_item(self, interact: Interact):
        super().add_item(interact)
        self.unselect_all_but(self.first_item)
        

    def select_next(self, event: pygame.event.Event):
        super().select_next(event)
        
        if (isinstance(self.selected_item, Group)):
            self.selected_item.select_first()
