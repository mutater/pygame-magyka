from .common import *

MaxValue = float | tuple[float, float]

class Timer:
    def __init__(self, max_range: MaxValue, enabled: bool = True, reset_on_complete: bool = True, reset_subtracts_max: bool = True):
        self._max: tuple[float, float] = (0, 0)
        self.max = 0.0
        self.value = 0.0

        self._max_range: tuple[float, float] = (0, 0)
        self.max_range = max_range
        self.enabled = enabled
        self.reset_on_complete = reset_on_complete
        self.reset_subtracts_max = reset_subtracts_max

    @property
    def max_range(self):
        return self._max

    @max_range.setter
    def max_range(self, value: MaxValue):
        if not isinstance(value, tuple):
            self._max = (value, value)
        else:
            self._max = value
    
    @property
    def complete(self):
        if self.enabled and self.value >= self.max:
            if self.reset_on_complete:
                self.reset(self.reset_subtracts_max)
            
            return True

        return False

    @property
    def percent(self) -> float:
        return self.value / self.max

    def tick(self, dt: float) -> Self:
        if self.enabled:
            self.value += dt
        
        return self
    
    def reset(self, subtract_max: bool = False):
        if subtract_max:
            self.value -= self.max
        else:
            self.value = 0
        
        self.reset_max()

    def reset_time(self):
        self.value = 0

    def reset_max(self):
        self.max = rand(self.max_range)
