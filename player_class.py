import pygame
from settings import *



class Player:
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        self.direction = vec(0,0)
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], 15, 80)
        self.center = [self.pos[0]+7.5, self.pos[1]+40]
        self.score = 0
        self.color = PLAYER_COLOR
    def update(self):
        if self.pos[1] < HEIGHT-80 and self.pos[1] > 0:
            self.pos += self.direction
            self.center += self.direction
            self.hitbox.left = self.pos[0]
            self.hitbox.top = self.pos[1]

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color, 
        [self.pos[0], self.pos[1], 15, 80])

    def move(self, direction):
        self.direction = direction
        self.pos[1] += direction[1]
        self.center[1] += direction[1]
    
    def change_color(self, color):
        self.color = color
