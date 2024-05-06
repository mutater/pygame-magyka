from library.screen import Screen
from library.gameManager import GameManager
from library.gameState import GameState
from library.screenManager import ScreenManager

class TitleScreen(Screen):
    name = "title"

    def __init__(self, gm: GameManager, gs: GameState, sm: ScreenManager, name: str):
        super().__init__(gm, gs, sm, name)
    
    def start(self):
        print("hi")

    def update(self):
        print("update")

    def draw(self):
        print("draw")