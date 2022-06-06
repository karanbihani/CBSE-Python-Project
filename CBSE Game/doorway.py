import pygame

class Door(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.image.load('Assets\Images\Terrain\portal.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        '''
        self.image = pygame.Surface((size,size))
        self.image.fill('white')
        self.rect =self.image.get_rect(topleft = pos)
        '''
    def update(self , x_shift):
        self.rect.x += x_shift