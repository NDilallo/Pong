import pygame
from settings import *


class Walls():

    def __init__(self, game) -> None:
        self.game = game
        self.hitboxVert = [pygame.Rect(0, 1, WIDTH, 1), pygame.Rect(0, HEIGHT, WIDTH, 1)] #list containing top and bottom walls
        self.hitboxGoal = [pygame.Rect(-1, 0, 1, HEIGHT), pygame.Rect(WIDTH, 0, 1, HEIGHT)]
    
    def draw(self):
        pass