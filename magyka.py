import pygame

from library.gameManager import GameManager
from library.gameState import GameState
from library.screenManager import ScreenManager

from screen.title import TitleScreen

from constant.fonts import *

pygame.init()
screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0], pygame.FULLSCREEN | pygame.RESIZABLE)

gm = GameManager()
gs = GameState()
sm = ScreenManager(gm, gs)

sm.push(TitleScreen)

sm.loop()

# asdfasdfasdfasdf

pygame.quit()