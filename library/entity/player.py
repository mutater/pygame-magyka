from . import *

from ..common import *
from ..component import *

class Player(Entity):
    def __init__(self, name: str):
        super().__init__()
        self.info = Info(name=name)
