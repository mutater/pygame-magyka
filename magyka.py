from library.common import *

from library.screenManager import ScreenManager
from library.gameManager import GameManager

import library.screens as screens

gm = GameManager()

sm = ScreenManager(gm)
sm.push(screens.TitleScreen)
sm.loop()

pygame.quit()
