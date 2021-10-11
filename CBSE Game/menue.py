import pygame
from settings import *
from menue_stage import Stage

class Menue():
    def __init__(self,menue_data,display_surface,max):
        self.display_surface = display_surface
        self.menue_data = menue_data
        self.max = max
        self.tile_active = True
        self.game_active = False
        self.setup_menue()

    def setup_menue(self):
        self.stage = pygame.sprite.Group()
        for key in range(5):
            if self.menue_data[key]['unlocked'] > self.max:
                self.tile_active = False
            self.pos = self.menue_data[key]['pos']
            self.stage_instance = Stage(self.pos,TILE_SIZE,self.tile_active,self.display_surface)
            self.stage.add(self.stage_instance) 
    
    def run(self):
        self.stage.draw(self.display_surface)