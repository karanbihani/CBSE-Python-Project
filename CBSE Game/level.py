import os

import pygame
from pygame.sprite import Group

from coins import Coin
from health import Health
from player import Player
from settings import *
from tiles import Tile

pygame.font.init()


class Level():
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.coins_counter = 0
        self.player_health = PLAYER_HEALTH
        
    def setup_level(self, layout):
        self.coins = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col.lower() == 'x':
                    tile = Tile((x, y), TILE_SIZE)
                    self.tiles.add(tile)
                if col.lower() == 'p':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                if col.lower() == 'c':
                    coin_sprite = Coin((x,y) , COIN_SIZE)
                    self.coins.add(coin_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < 300 and direction_x < 0:
            self.world_shift = PLAYER_SPEED
            player.speed = 0
        
        elif player_x > 800 and direction_x > 0:
            self.world_shift = -PLAYER_SPEED
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = PLAYER_SPEED
    
    def horizontal_movement_collision(self):
        player = self.player.sprite
        
        player.rect.x += player.direction.x*player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 :
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.direction.y = 0
                    player.rect.top = sprite.rect.bottom
                elif player.direction.y > 0:
                    player.direction.y = 0
                    player.rect.bottom = sprite.rect.top
                    player.jump_active = JUMP_ACTIVE
    
    def collect_coins(self):
        player = self.player.sprite
        if pygame.sprite.spritecollide(player, self.coins ,True):
            self.coins_counter += 1
            self.player_health -= 1
            print(self.player_health)
    
    def display_coins_collected(self):
        self.font = pygame.font.Font('Assets/font/Pixeltype.ttf',50)
        self.text = self.font.render(f'  {self.coins_counter}', False , 'pink')
        self.text_rect = self.text.get_rect(center = (980 , 110))

        self.coin_image = pygame.image.load('Assets\Images\Coins\coin_2.png').convert_alpha()
        self.coin_surface = pygame.transform.scale(self.coin_image,(50,50))
        self.coin_rect = self.coin_surface.get_rect(topleft = (905,84))

        self.display_surface.blit(self.text,self.text_rect)
        self.display_surface.blit(self.coin_surface , self.coin_rect)

    def health_run(self):
        self.health = Health()
        self.health.health_define(self.player_health, self.display_surface)

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.coins.update(self.world_shift)
        self.collect_coins()
        self.scroll_x()
        self.display_coins_collected()
        self.health_run()
        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.coins.draw(self.display_surface)
        #self.health.draw(self.display_surface)
        

