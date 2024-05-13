from .gameObject import *

class Entity(GameObject):
    def __init__(self):
        super().__init__()
    
    @classmethod
    def new(cls) -> Self:
        gameObject = super().new()
        gameObject.add_component(Health())
        return gameObject
