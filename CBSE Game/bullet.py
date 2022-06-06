import pygame
import math
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,size,mpos):
        super().__init__()
        self.image = pygame.image.load('Assets\Images\Player\eshell.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        '''
        self.image = pygame.Surface((size,size))
        self.image.fill('blue')
        self.rect =self.image.get_rect(topleft = pos)
        '''
        self.direction = pygame.math.Vector2(0,0)
        self.player_pos = pos
        self.mpos = mpos

    def travel(self):
        
        self.targetdist = math.sqrt((self.mpos[0] - self.player_pos[0]) ** 2 + (self.mpos[1] - self.player_pos[1]) ** 2)

        self.direction.x = (self.mpos[0] - self.player_pos[0])/self.targetdist
        self.direction.y = (self.mpos[1] - self.player_pos[1])/self.targetdist

        self.rect.x += self.direction.x*BULLET_SPEED
        self.rect.y += self.direction.y*BULLET_SPEED

    def update(self,x_shift):
        self.rect.x += x_shift
        self.travel()

    #run the code now