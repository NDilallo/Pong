import pygame
from settings import *


class AI:

    def __init__(self, game, pos): #removed ball
        self.game = game
        self.pos = pos
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], 15, 80)
        self.center = [self.pos[0]+7.5, self.pos[1]+40]
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], 15, 80)
        self.ballPos = []
        self.score = 0
        self.color = PLAYER_COLOR
        
    def update(self):
        currMin = self.ballPos[0].pos[0]
        index = 0
        count = 0
        for ball in self.ballPos:
            if ball.pos[0] < currMin:
                currMin = ball.pos[0]
                index = count
            count += 1

        if self.pos[1] <= HEIGHT-80 and self.pos[1] >= 0:
            if self.ballPos[index].pos[1] > self.center[1]:
                self.pos[1] += 4
                self.center[1] += 4
                self.hitbox.left = self.pos[0]
                self.hitbox.top = self.pos[1]
            elif self.ballPos[index].pos[1] < self.center[1]:
                self.pos[1] += -4
                self.center[1] += -4
                self.hitbox.left = self.pos[0]
                self.hitbox.top = self.pos[1]
        elif self.pos[1] > HEIGHT-80:
            self.pos[1] -= 1
        else:
            self.pos[1] += 1

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color, 
        [self.pos[0], self.pos[1], 15, 80])
    

    def giveBall(self, givenBall):
        self.ballPos.append(givenBall)

    def change_color(self, color):
        self.color = color
