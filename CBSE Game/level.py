import os
import pygame

from pygame.sprite import Group

from coins import Coin
from health import Health
from player import Player
from enemies import Tracer
from settings import *
from tiles import Tile

pygame.font.init()

class Level():
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.coins_counter = 0
        self.health = Health()
        self.game_active = True
        
    def setup_level(self, layout):
        self.coins = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.trace = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col.lower() == 'x':
                    tile = Tile((x, y), TILE_SIZE)
                    self.tiles.add(tile)
                elif col.lower() == 'p':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                elif col.lower() == 'c':
                    coin_sprite = Coin((x,y) , COIN_SIZE)
                    self.coins.add(coin_sprite)
                elif col.lower() == 't':
                    trace_sprite = Tracer((x,y) , 32)
                    self.trace.add(trace_sprite)

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
    
    def display_coins_collected(self):
        self.font = pygame.font.Font('Assets/font/Pixeltype.ttf',50)
        self.text = self.font.render(f'  {self.coins_counter}', False , 'pink')
        self.text_rect = self.text.get_rect(center = (980 , 110))

        self.coin_image = pygame.image.load('Assets\Images\Coins\coiner.png').convert_alpha()
        self.coin_surface = pygame.transform.scale(self.coin_image,(50,50))
        self.coin_rect = self.coin_surface.get_rect(topleft = (905,84))

        self.display_surface.blit(self.text,self.text_rect)
        self.display_surface.blit(self.coin_surface , self.coin_rect)

    def trace_collision(self):
        player = self.player.sprite
        if pygame.sprite.spritecollide(player, self.trace, True):
            self.health.player_health-=6

    def respawn(self):
        if self.player.sprite.rect.y >750:
            self.health.lives -= 1
            self.player.sprite.rect.y = 0
            pygame.time.delay(500)
            self.player.sprite.direction.y = -5
            
    #----------------------------
    
    def tracer_movement_x(self):
        for tracer in self.trace.sprites():
            for sprite in self.tiles.sprites():
                if tracer.rect.colliderect(sprite.rect):
                    if tracer.direction.y < 0:
                        tracer.direction.x = 5
                        tracer.direction.y = 0
                        tracer.rect.top = sprite.rect.bottom
                    elif tracer.direction.y > 0:
                        tracer.direction.x = 5
                        tracer.direction.y = 0
                        tracer.rect.bottom = sprite.rect.top
                        tracer.jump_active = JUMP_ACTIVE
    
    def tracer_movement_y(self):
        for tracer in self.trace.sprites():
            for sprite in self.tiles.sprites():
                if tracer.rect.colliderect(sprite.rect):
                    if tracer.direction.x < 0:
                        tracer.direction.y = 5
                        tracer.direction.x = 0
                        tracer.rect.left = sprite.rect.right
                    elif tracer.direction.x > 0:
                        tracer.direction.y = 5
                        tracer.direction.x = 0
                        tracer.rect.right = sprite.rect.left
                        tracer.jump_active = JUMP_ACTIVE
    
    def tracer_movement(self):
        self.tracer_movement_x()
        self.tracer_movement_y()
    #----------------------------

    def run(self):
        self.game_active = self.health.game_state_changer()
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.coins.update(self.world_shift)
        self.collect_coins()
        self.scroll_x()
        self.display_coins_collected()
        self.health.health_run(self.display_surface)
        self.respawn()
        self.player.update()
        self.player.draw(self.display_surface)
        self.trace.draw(self.display_surface)
        self.trace.update(self.player.sprite.rect.x, self.player.sprite.rect.y,self.world_shift)
        
        self.tracer_movement()

        self.trace_collision()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.coins.draw(self.display_surface)
        #self.health.draw(self.display_surface)
        

