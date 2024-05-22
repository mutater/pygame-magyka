from .gameObject import *

class Item(GameObject):
    def __init__(self):
        super().__init__()
        self.info = Info()

        self.stackable = False
