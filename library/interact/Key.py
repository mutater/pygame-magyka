from library.common import *
from library.interact.interact import Interact, EventCallbackValue

class Key(Interact):
    def __init__(self, keys: List[int], callbacks: EventCallbackValue):
        super().__init__()

        self.add_keys(keys, callbacks)
    
    def on_event(self, event: pygame.event.Event):
        if not self.enabled:
            return

        self.on_key_event(event)
