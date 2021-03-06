import math
import pygame
from settings import *
import random


class Ball:
    def __init__(self, game):
        self.game = game
        self.pos = BALL_START_POS
        self.hitbox = pygame.Rect(self.pos[0]-10, self.pos[1]-10, 20, 20)
        self.dir_horizontal = 1
        self.dir_vertical = 0
        self.vert_speed = BALL_START_SPEED_VERT
        self.horizontal_speed = BALL_START_SPEED
        self.speedSave = self.horizontal_speed
        self.hidden = False
        self.color = BALL_COLOR

    def update(self):
        self.pos[0] += self.horizontal_speed*self.dir_horizontal
        self.hitbox.left = self.pos[0]
        self.hitbox.top = self.pos[1]
        self.pos[1] += self.vert_speed*self.dir_vertical
    
    def draw(self):
        if self.hidden == False:
            pygame.draw.circle(self.game.screen, self.color, 
            [self.pos[0], self.pos[1]], BALL_SIZE)
    

    def scoreCheck(self):
        if self.pos[0] > WIDTH:
            self.hidden = True
            return [True, 'ai']
        elif self.pos[0] < 0:
            self.hidden = True
            return [True, 'player']
        return [False, '']

    def respawn(self):
        self.dir_horizontal *= random.randrange(-1, 1, 2)
        self.dir_vertical = 0
        self.vert_speed += -self.vert_speed
        self.horizontal_speed = self.speedSave
        self.hidden = False
        if self.pos[0] > WIDTH:
            self.pos[0] -= WIDTH/2
            self.pos[1] -= self.pos[1]-HEIGHT/2
        elif self.pos[0] < 0:
            self.pos[0] += WIDTH/2
            self.pos[1] -= self.pos[1]-HEIGHT/2
        


    def reflect(self, type, object):
        if type == 'player':
            # Determine distance from center of player/ai (center - ballpos)
            dist = object.center[1] - self.pos[1]
            # if positive (top half): add to current vertical velocity (upwards)
            if dist > 0:
                self.dir_vertical = -1
                self.vert_speed += 1
            # if negative (bottom half): subtract from current vertical velocity (send downwards)
            elif dist < 0:
                self.dir_vertical = 1
                self.vert_speed += 1
            else:
                self.dir_vertical = random.randrange(-1, 1, 2) #random direction
                self.vert_speed += self.dir_vertical
            # reverse and increase horizontal velocity
            self.dir_horizontal *= -1
            self.horizontal_speed += 1
        elif type == 'wall':
            # Reverse vertical direction
            self.dir_vertical *= -1
            # Move it away from the wall to prevent it getting stuck
            if self.dir_vertical > 0:
                self.pos[1] += 20
            elif self.dir_vertical < 0:
                self.pos[1] -= 20

    def change_start_speed(self, speed):
        self.horizontal_speed = speed
        self.speedSave = speed
    def change_color(self, color):
        self.color = color






    #     if collision_type=='horizontal': #top or bottom wall
    #         self.dir_vertical *= -1
    #         if self.pos[1] < 10:
    #             self.pos[1] += 10
    #         else:
    #             self.pos[1] -= 10

    #     if collision_type=='vertical': #player or ai
    #         if self.dir_vertical==0:
    #             self.dir_vertical=1
    #         centerDist = self.pos[1]-object.center[1]
    #         self.vert_speed += centerDist/10
    #         self.dir_horizontal = self.dir_horizontal*-1


    # def collisionCheck(self):
    #     if self.hitbox.colliderect(self.player.hitbox):
    #         self.pos[0] -= 4
    #         self.dir = self.dir*-1
    #         centerDist = self.pos[1]-self.player.center[1]
    #         self.vertForce += centerDist/3.5
    #     if self.hitbox.colliderect(self.ai.hitbox):
    #         self.pos[0] += 4
    #         self.dir = self.dir*-1
    #         centerDist = self.pos[1]-self.ai.center[1]
    #         self.vertForce += centerDist
    #     for i in range(2):
    #         if self.hitbox.colliderect(self.walls.hitboxVert[i]):
    #             self.pos[1] += self.dir*4
    #             self.dir = self.dir*-1
    #             centerDist = self.pos[1]-self.ai.center[1]
    #             self.vertForce += self.dir*centerDist


# Ball deflection:
# The farther above the center of the paddle it hits, the biggger of an angle 
# upwards it goes
# Opposite for below center
