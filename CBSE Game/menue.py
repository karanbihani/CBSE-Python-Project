import pygame
from settings import *
from menue_stage import Stage

class Menue():
    def __init__(self,menue_data,display_surface,max):
        self.display_surface = display_surface
        self.menue_data = menue_data
        self.max = max
        self.stage = pygame.sprite.Group()
        self.active = True
        self.setup_menue()

    def setup_menue(self):
        for key in self.menue_data:
            if self.menue_data[key]['unlocked'] > self.max:
                print(False)
                self.active = False
            self.pos = self.menue_data[key]['pos']
            self.stage_instance = Stage(self.pos,TILE_SIZE,True,self.display_surface)
            self.stage.add() 
    
    def run(self):
        self.stage.draw(self.display_surface)