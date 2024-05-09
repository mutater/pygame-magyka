import pygame

from library.gameManager import GameManager
from library.gameState import GameState
from library.screenManager import ScreenManager

import library.screens as screens

pygame.init()
pygame.key.set_repeat(300, 100)

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

gm = GameManager()
gs = GameState()
sm = ScreenManager(gm, gs)

sm.push(screens.Test)
sm.loop(screen)

pygame.quit()
