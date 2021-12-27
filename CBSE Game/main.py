import pygame
import sys
from random import *
from pygame.constants import QUIT

#User defined modules
from settings import *
from level import Level
from level_data import levels
from level_menue_data import menue_level
from menue import Menue

pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Agent Quack 007')
clock = pygame.time.Clock()

class Game():
    def __init__(self,levels,menue_level):
        self.current_level = 0
        self.menue_level = menue_level
        self.levels = levels        
        self.level = Level(self.levels, SCREEN, self.current_level)
        self.menue = Menue(self.menue_level,SCREEN,3)
        self.game_active = True

    def run(self):#mode is 0,1 or 2 where 0 is menue and 1 is game
        if self.game_active:
            game.level.run() 
            self.current_level = self.level.current_level
            self.game_active = self.level.game_active
            if not self.game_active:
                self.menue = Menue(self.menue_level, SCREEN, self.current_level+2)
        else:
            game.menue.run()
            self.game_active = self.menue.game_active
            if self.game_active:        
                self.level = Level(self.levels, SCREEN, self.current_level)

game = Game(levels, menue_level)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()   
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            
    SCREEN.fill('Black')
    
    game.run()

    pygame.display.update()
    clock.tick(FPS)
