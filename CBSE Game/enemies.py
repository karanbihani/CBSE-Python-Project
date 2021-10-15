import pygame
import math

class Tracer(pygame.sprite.Sprite):
    def __init__(self,pos,size):   #px - player's x pos || py - player's y pos
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)

    def attack(self,speed,normalizer):
        self.direction.x = (self.px - self.rect.x)/normalizer # ~= 1
        self.direction.y = (self.py - self.rect.y)/normalizer # ~= 1
        self.rect.x += (self.direction.x)*speed
        self.rect.y += (self.direction.y)*speed

    def shift(self,x_shift):
        self.rect.x += x_shift

    def update(self,player_x,player_y,x_shift):
        self.px = player_x
        self.py = player_y
        self.targetdest = math.sqrt((self.px - self.rect.x) ** 2 + (self.py - self.rect.y) ** 2)
        if self.targetdest <=100:
            self.attack(2.5,self.targetdest)
        elif self.targetdest <=300:
            self.attack(2,self.targetdest)
        self.rect.x += x_shift
        



