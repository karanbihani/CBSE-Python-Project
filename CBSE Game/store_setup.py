import pygame

class Store_Builder(pygame.sprite.Sprite):
    def __init__(self,size,display_surface):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.colored()
        self.rect = self.image.get_rect(topleft = (0,0))
        self.display_surface = display_surface

    def run(self):
        pass