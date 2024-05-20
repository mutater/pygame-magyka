from .gameObject import *

class Entity(GameObject):
    def __init__(self):
        super().__init__()
        self.add_component(Health())
        self.add_component(Mana())
