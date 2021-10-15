import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((32,64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)
        
        #movement
        self.direction = pygame.math.Vector2(0,0)
        self.jump_active = JUMP_ACTIVE
        self.speed = PLAYER_SPEED
        self.gravity = GRAVITY
        self.jump_speed = JUMP_SPEED

    # Movement

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            
        elif keys[pygame.K_a]:
            self.direction.x = -1

        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.jump_active > 0:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_active = self.jump_active - 1  
    
    def update(self):
        self.get_input()