from library.common import *

from .entity import Player

class GameManager:
    def __init__(self):
        self.player = Player.new()
