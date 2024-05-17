from ..common import *
from . import Component

class Info(Component):
    def __init__(self, **kwargs):
        self.name: str = kwargs.get("name", "")
        self.desc: str = kwargs.get("desc", "")
        self.rarity: str = kwargs.get("rarity", "")