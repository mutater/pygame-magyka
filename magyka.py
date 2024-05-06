import pygame

from library.gameManager import GameManager
from library.gameState import GameState
from library.screenManager import ScreenManager

from screen.title import TitleScreen

pygame.init()
screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[1], pygame.RESIZABLE)

gm = GameManager()
gs = GameState()
sm = ScreenManager(gm, gs)

sm.push(TitleScreen)
sm.loop(screen)

pygame.quit()