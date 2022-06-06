import pygame
from settings import *
from menue_stage import Stage

class Menue():
    def __init__(self,menue_data,display_surface,max,menu_bg):
        self.display_surface = display_surface
        self.menue_data = menue_data
        self.max = max + 1
        self.tile_active = True
        self.game_active = False
        self.menu_bg = menu_bg
        self.setup_menue()

    def setup_menue(self):
        self.stage = pygame.sprite.Group()
        for key in range(3):
            if self.menue_data[key]['unlocked'] > self.max:
                self.tile_active = False
                #print(self.max, self.menue_data[key]['unlocked'],self.tile_active)
            self.pos = self.menue_data[key]['pos']
            self.stage_instance = Stage(self.pos,TILE_SIZE,self.tile_active,self.display_surface)
            self.stage.add(self.stage_instance)
        
        self.start_button = pygame.Surface((200,100))
        self.start_rect = self.start_button.get_rect(center = (SCREEN_WIDTH//2, 500))

        self.start_button = pygame.image.load('Assets\Images\Buttons\start_button.png')
        self.start_button_surface = pygame.transform.scale(self.start_button,(1,1))
        self.start_button_rect = self.start_button_surface.get_rect(center = (SCREEN_WIDTH//2 - 115, 500))
            
    def game_state_changer(self):
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.start_rect.collidepoint(mouse_pos):
                self.game_active = True
            
            #To control level using the 5 buttons (Currently not required)
            '''
            for sprite in self.stage.sprites():
                if sprite.rect.collidepoint(mouse_pos) and sprite.active:
                    print('Continue')
                elif sprite.rect.collidepoint(mouse_pos):
                    print('Clear more level')
            '''
    
    def run(self):
        
        self.game_state_changer()
        #self.display_surface.blit(self.menu_bg, (0,0))
        self.stage.draw(self.display_surface)
        self.display_surface.blit(self.start_button,self.start_button_rect)
        
        