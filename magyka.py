import pygame

from library.screenManager import ScreenManager
import library.screens as screens

pygame.init()
pygame.key.set_repeat(500, 100)

sm = ScreenManager()
sm.push(screens.Test)
sm.loop()

pygame.quit()
