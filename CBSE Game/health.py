import pygame

class Health():
    def __init__(self,size,pos):
        self.image = pygame.Surface((size,size))
        self.image.fill('red')
        self.image_rect = self.image.get_rect(topleft = pos)
