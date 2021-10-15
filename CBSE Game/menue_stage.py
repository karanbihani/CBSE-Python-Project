import pygame
from settings import *

class Stage(pygame.sprite.Sprite):
    def __init__(self,pos,size,active,display_surface):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.active = active
        self.active_color = 'red'
        self.not_active_color = 'grey'
        self.colored()
        self.rect = self.image.get_rect(topleft = pos)
        self.display_surface = display_surface

    def colored(self):
        if self.active:
            self.image.fill(self.active_color)
        else:
            self.image.fill(self.not_active_color)
            
    def run(self):
        pass