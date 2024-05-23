from .gameObject import *

class Item(GameObject):
    def __init__(self):
        super().__init__()

        self.value = Currency()

        self.components += [self.value]

        self.stackable = False
