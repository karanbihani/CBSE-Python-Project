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
        self.game_active = False
        self.menue_level = menue_level
        self.level = levels
        self.level = Level(self.level[0], SCREEN)
        self.menue = Menue(self.menue_level,SCREEN,3)

game = Game(levels,menue_level)

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()   
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            
    SCREEN.fill('Black')
    game.menue.run()

    pygame.display.update()
    clock.tick(FPS)
