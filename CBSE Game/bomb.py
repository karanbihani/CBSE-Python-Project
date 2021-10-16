#This enemy when shot causes palyer to lose health

import pygame

class Bomb(pygame.sprite.Sprite):
    def __init__(self,pos,size):   
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('purple')
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift