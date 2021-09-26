import pygame
import sys
from random import *
from pygame.constants import QUIT

#User defined modules
from settings import *
from level import Level
from level_data import levels

pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Agent Quack 007')
clock = pygame.time.Clock()

level = Level(levels[0], SCREEN)

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()   
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            
    SCREEN.fill('Black')
    level.run()

    pygame.display.update()
    clock.tick(FPS)
