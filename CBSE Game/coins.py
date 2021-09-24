import os
import pygame
from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets','Images','Coins','coin.png')).convert_alpha()
        self.surface = pygame.transform.scale(self.image,(50,50))
        self.rect = self.surface.get_rect(topleft = pos)
    def update(self , x_shift):
        self.rect.x += x_shift

