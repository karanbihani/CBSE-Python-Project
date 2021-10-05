import pygame
from settings import *

class Stage(pygame.sprite.Sprite):
    def __init__(self,pos,size,active,display_surface):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('red')
        self.active = active
        self.active_color = 'red'
        self.not_active_color = 'grey'
        self.image_rect = self.image.get_rect(topleft = pos)
        self.display_surface = display_surface
        self.display_surface.blit(self.image,self.image_rect)

    def run(self):
        pass