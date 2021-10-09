import pygame
import os
from settings import *

class Health():

    def __init__(self):
        self.lives = LIVES
        self.player_health = PLAYER_HEALTH
        self.health_icon_image = pygame.image.load(os.path.join('Assets','Images','Health','health_heart.png')).convert_alpha()
        self.health_icon_surface = pygame.transform.scale(self.health_icon_image,(60 , 60))
        self.health_icon_rect = self.health_icon_surface.get_rect(topleft = (900,35))
    
    def lives_output(self,display_surface):
        self.spacer_x = 60 
        self.x_start = 700
        y = 30
        for spacer in range(self.lives):
            x = self.x_start + spacer*self.spacer_x
            self.health_rect = self.health_icon_surface.get_rect(topleft = (x,y))
            display_surface.blit(self.health_icon_surface, self.health_rect) 

    def life_loss(self):
        self.player_health = PLAYER_HEALTH
        self.lives -= 1
        print(self.lives)
    
    def game_state_changer(self):
        if self.lives == 0:
            return False
        else:
            return True

    def health_define(self, display_surface ):
        if self.player_health>0:
            self.health_bar_length = (SCREEN_WIDTH//120) * self.player_health
        else:
            self.life_loss()
        x = 960
        y = 50
        self.health_image = pygame.Surface((self.health_bar_length,30))
        self.health_image.fill('red')
        health_rect = self.health_image.get_rect(topleft = (x,y))
        display_surface.blit(self.health_icon_surface, self.health_icon_rect)
        display_surface.blit(self.health_image ,health_rect)
    
    def health_run(self,display_surface):
        self.health_define(display_surface)
        self.lives_output(display_surface)