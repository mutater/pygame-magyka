from .entity import *

class Player(Entity):
    def __init__(self):
        super().__init__()
    
    @classmethod
    def new(cls) -> Self:
        gameObject = super().new()
        return gameObject
