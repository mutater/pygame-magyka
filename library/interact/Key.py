from library.common import *

from . import Interact, EventCallbackOrList

class Key(Interact):
    def __init__(self, keys: IntOrList, callbacks: EventCallbackOrList):
        super().__init__()

        if not isinstance(keys, list):
            keys = [keys]

        self.add_key(keys, callbacks)
    
    def on_event(self, event: pygame.event.Event):
        if not self.enabled:
            return

        self.on_key_event(event)
