from ..common import *

from . import Interact, EventCallbackOrList

class Key(Interact):
    def __init__(self, keys: IntOrList, callbacks: EventCallbackOrList):
        super().__init__()

        self.add_key(to_list(keys), callbacks)
    
    def on_event(self, event: Event):
        if not self.enabled:
            return

        self.on_key_event(event)
