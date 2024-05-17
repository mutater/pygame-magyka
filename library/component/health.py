from ..common import *
from ..valueContainer import ValueContainer

from . import Component

class Health(Component, ValueContainer):
    def __init__(self, value: int = 30):
        Component.__init__(self)
        ValueContainer.__init__(self, value)
