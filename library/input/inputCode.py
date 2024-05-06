from library.common import *

InputCodeValue = int | Tuple[int, str | List[str]]

class InputCode:
    def __init__(self, code: int, callbacks: List[str] | None = None):
        self.code = code
        self.pressed = False
        self.callbacks = callbacks

    def has_callback(self, callback: str) -> bool:
        if self.callbacks == None:
            return True
        else:
            return callback in self.callbacks
