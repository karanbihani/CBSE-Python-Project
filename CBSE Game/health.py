import pygame
import os
from settings import *

class Health():

    def __init__(self):
        
        self.health_icon_image = pygame.image.load(os.path.join('Assets','Images','Health','health_heart.png')).convert_alpha()
        self.health_icon_surface = pygame.transform.scale(self.health_icon_image,(60 , 60))
        self.health_icon_rect = self.health_icon_surface.get_rect(topleft = (880,35))

    def health_define(self, player_health , display_surface):
        health_bar_length = (SCREEN_WIDTH//120) * player_health
        x = 960
        y = 50
        health_image = pygame.Surface((health_bar_length,30))
        health_image.fill('red')
        health_rect = health_image.get_rect(topleft = (x,y))
        display_surface.blit(self.health_icon_surface, self.health_icon_rect)
        display_surface.blit(health_image ,health_rect)