from library.common import *

from library.screenManager import ScreenManager
from library.gameManager import GameManager

import library.screens as screens

pygame.init()
pygame.key.set_repeat(500, 100)

gm = GameManager()

sm = ScreenManager(gm)
sm.push(screens.Test)
sm.loop()

pygame.quit()
