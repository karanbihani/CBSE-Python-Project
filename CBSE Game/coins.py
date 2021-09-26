
import pygame
from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos , size):
        super().__init__()
        self.image = pygame.image.load('Assets\Images\Coins\coin_2.png').convert_alpha()
        self.surface = pygame.transform.scale(self.image,(size,size))
        self.rect = self.surface.get_rect(topleft = pos)

    def update(self , x_shift):
        self.rect.x += x_shift

