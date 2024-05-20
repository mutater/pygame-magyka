import json

from .common import *
from .serializable import Serializable

class ValueContainer(Serializable):
    @overload
    def __init__(self, max: float, /, value: float | None = None): ...
    @overload
    def __init__(self, min: float, max: float, /, value: float | None = None): ...

    def __init__(self, *args, **kwargs):
        self._value: float = 0
        self._min: float = 0
        self._max: float = 0
        
        if len(args) == 1:
            self.min = 0
            self.max = args[0]
        else:
            self.min = args[0]
            self.max = args[1]
        
        self.value = kwargs.get("value", self.max)

    def __add__(self, value: float) -> float:
        return self.value + value
    
    def __iadd__(self, value: float) -> Self:
        self.value += value
        return self
    
    def __sub__(self, value: float) -> float:
        return self.value - value

    def __isub__(self, value: float) -> Self:
        self.value -= value
        return self
    
    def __mul__(self, value: float) -> float:
        return self.value * value
    
    def __imul__(self, value: float) -> Self:
        self.value *= value
        return self
    
    def __floor__(self) -> int:
        return self.value.__floor__()
    
    def __round__(self) -> int:
        return self.value.__round__()
    
    def __ceil__(self) -> int:
        return self.value.__int__()
    
    def __str__(self) -> str:
        return f"{self.value:.1f}/{self.max:.1f}"
    
    def __eq__(self, value) -> bool:
        return self.value.__eq__(value)
    
    def __lt__(self, value) -> bool:
        return self.value.__lt__(value)
    
    def __gt__(self, value) -> bool:
        return self.value.__gt__(value)

    @property
    def min(self):
        return self._min
    
    @min.setter
    def min(self, value: float):
        self._min = value
        self.value = self.value
    
    @property
    def max(self):
        return self._max
    
    @max.setter
    def max(self, value: float):
        self._max = value
        self.value = self.value
    
    @property
    def int_max(self) -> int:
        return int(math.ceil(self.max))

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: float):
        self._value = clamp(value, self.min, self.max)
    
    @property
    def int_value(self) -> int:
        return int(math.ceil(self.value))
    
    @property
    def percent(self) -> float:
        return ((self.value + self.min) / (self.max - self.min))
    
    @percent.setter
    def percent(self, value: float):
        value = clamp(value, 0, 1)
        self.value = (self.max - self.min) * (value) + self.min
    
    @property
    def empty(self) -> bool:
        return self.value == self.min
    
    @property
    def full(self) -> bool:
        return self.value == self.max

    def serialize(self) -> str | None:
        return json.dumps({"min": self.min, "max": self.max, "value": self.value})
    
    def deserialize(self, json_data: str) -> Self:
        data = json.loads(json_data)

        self.min = data["min"]
        self.max = data["max"]
        self.value = data["value"]
        
        return self
