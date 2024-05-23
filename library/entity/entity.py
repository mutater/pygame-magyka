from .gameObject import *

class Entity(GameObject):
    def __init__(self):
        super().__init__()

        self.life = Life()
        self.mana = Mana()
        self.level = Level()

        self.components += [self.life, self.mana, self.level]
