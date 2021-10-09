import pygame
import math

class Tracer(pygame.sprite.Sprite):
    def __init__(self):   #px - player's x pos || py - player's y pos
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft = (400,300))
        self.direction = pygame.math.Vector2(0,0)

    def attack(self,speed,normalizer):
        self.direction.x = (self.px - self.rect.x)/normalizer # ~= 1
        self.direction.y = (self.py - self.rect.y)/normalizer # ~= 1

        self.rect.x += (self.direction.x)*speed
        self.rect.y += (self.direction.y)*speed

        print(self.direction)

    def update(self,player_x,player_y):
        self.px = player_x
        self.py = player_y
        self.targetdest = math.sqrt((self.px - self.rect.x) ** 2 + (self.py - self.rect.y) ** 2)
        if self.targetdest <=100:
            self.attack(3,self.targetdest)
        elif self.targetdest <=300:
            self.attack(1.5,self.targetdest)



