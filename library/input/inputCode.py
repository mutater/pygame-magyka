from library.common import *

class InputCode:
    def __init__(self, code: Tuple[int, ]):
        self.code = code
        self.pressed = False
        self.callback_ids = callback_ids