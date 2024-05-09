import pygame as pg

class Time:
    def __init__(self, fps):
        self.fps = fps
        self.clock = pg.time.Clock()
        self.dt = 0
    
    def tick(self):
        self.dt = self.clock.tick(self.fps) / 1000