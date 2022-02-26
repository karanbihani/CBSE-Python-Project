import os
from time import time
import pygame
import mysql.connector as sql
import datetime

from pygame.sprite import Group

from coins import Coin
from health import Health
from player import Player
from enemies import Tracer
from settings import *
from tiles import Tile
from bullet import Bullet
from mirror import Mirror
from bomb import Bomb
from doorway import Door

pygame.font.init()

class Level():
    def __init__(self, level_data, surface,username, current_level, coins_counter):
        self.current_level = current_level
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.coins_counter = coins_counter
        self.health = Health(29) #player_health_sql NEEDS WORK F
        self.game_active = True
        self.shoot_active = True
        self.username = username
    
    # NEEDS WORK F testing
    
    '''
    def get_record_data(self):
        con = sql.connect(host = 'localhost', user = 'root', password = 'Bihani123', database = 'quacktable')
        if con.is_connected():
            print("Connection Established")
        cur = con.cursor()  
        q = (f'select level, coinct from plays where (uname = {self.username}) and (w = 0) order by tolp ascending;') #uname is taken from tkinter NEEDS WORK ok
        cur.execute(q)
        x = cur.fetchall()
        n = x[-1]
        return(n)
    '''
    
    def insert_record_data(self):
        con = sql.connect(host = 'localhost', user = 'root', password = 'Bihani123', database = 'quacktable')
        if con.is_connected():
            print("Connection Established")
        cur = con.cursor()
        q = (f'insert into plays (uname,coinct,level) values("{self.username}", {self.coins_counter},{self.current_level});')
        cur.execute(q)
        con.commit()
    
    def setup_level(self, layout):
        self.coins = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.trace = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.mirror = pygame.sprite.Group()
        self.bomb = pygame.sprite.Group()
        self.door = pygame.sprite.Group()
        for row_index, row in enumerate(layout[self.current_level]):
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
                elif col.lower() == 'm':
                    mirror_sprite = Mirror((x,y) , MIRROR_SIZE)
                    self.mirror.add(mirror_sprite)
                elif col.lower() == 'b':
                    bomb_sprite = Bomb((x,y) , BOMB_SIZE)
                    self.bomb.add(bomb_sprite)
                elif col.lower() == 'e':
                    door_sprite = Door((x,y) , DOOR_SIZE)
                    self.door.add(door_sprite)

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
    # Shooting
    # class bullets rect and image, LEVEL- shoot click->add a bukllet to the sprite grp and if sprite collide remove bullet and remove enemy and if it goes beyond bound x removed    

    def bullet_shoot(self):
        player = self.player.sprite
        self.player_pos = (player.rect.x , player.rect.y)
        self.bullet_counter = 0

        for bullet in self.bullets.sprites():
            if bullet.rect.x>(SCREEN_WIDTH + 100) or bullet.rect.x<-100 or bullet.rect.y>(SCREEN_HEIGHT+100) or bullet.rect.y<-100:
                bullet.kill()
                self.bullet_counter += 1
        
        if pygame.mouse.get_pressed()[0] and self.shoot_active ==  True and self.bullet_counter<=2:
            self.bullet_sprite = Bullet(self.player_pos,BULLET_SIZE,pygame.mouse.get_pos())
            self.bullets.add(self.bullet_sprite)
            self.shoot_active = False

        if pygame.mouse.get_pressed()[0] == False:
            self.shoot_active = True
    
    def bullet_crash(self):
        for sprite in self.tiles.sprites():
            pygame.sprite.spritecollide(sprite, self.bullets ,True)
        for sprite in self.door.sprites():
            pygame.sprite.spritecollide(sprite, self.bullets, True)

    def tracer_killer(self):
        for sprite in self.bullets.sprites():
            for tracer_sprite in self.trace.sprites():
                if sprite.rect.colliderect(tracer_sprite.rect):
                    sprite.kill()
                    tracer_sprite.kill()

    def mirror_collision(self):
        for sprite in self.mirror.sprites():
            if pygame.sprite.spritecollide(sprite, self.bullets, True):
                self.health.player_health -= MIRROR_DAMAGE
        
    def bomb_collision(self):
        player = self.player.sprite
        if pygame.sprite.spritecollide(player, self.bomb, True):
            self.health.player_health -= BOMB_DAMAGE
    
    def next_level(self):
        player = self.player.sprite
        if pygame.sprite.spritecollide(player, self.door, False):
            self.game_active = False
            self.current_level += 1
            self.insert_record_data()
    
    '''
    def pauser(self):
        self.pause = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            print(True)
            self.pause = True
            while self.pause:
                pygame.time.Clock().tick(1)
                print(True)
                self.display_surface.fill('white')
                keys = pygame.key.get_pressed()
                if keys[pygame.K_c]:
                    self.pause = False
                    pygame.time.Clock().tick(FPS)
    '''

    # Compilation of all run programs to better organise and follow code

    def TILES(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
    
    def DOOR(self):
        self.next_level()
        self.door.update(self.world_shift)
        self.door.draw(self.display_surface)

    def COINS(self):
        self.coins.update(self.world_shift)
        self.collect_coins()
        self.display_coins_collected()
        self.coins.draw(self.display_surface)

    def HEALTHS(self):
        self.health.health_run(self.display_surface)
        self.respawn()

    def PLAYERS(self):
        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()

    def BULLETS(self):
        self.bullet_shoot()
        self.bullets.update(self.world_shift)
        self.bullets.draw(self.display_surface)
        self.tracer_killer()
        self.bullet_crash()
    
    def TRACERS(self):
        self.tracer_movement()
        self.trace_collision()
        self.trace.update(self.player.sprite.rect.x, self.player.sprite.rect.y,self.world_shift)
        self.trace.draw(self.display_surface)

    def SETUPER(self):
        self.game_active = self.health.game_state_changer()
        self.scroll_x()

    def MIRRORS(self):
        self.mirror_collision()
        self.mirror.update(self.world_shift)
        self.mirror.draw(self.display_surface)

    def BOMBS(self):
        self.bomb_collision()
        self.bomb.update(self.world_shift)
        self.bomb.draw(self.display_surface)

    def run(self):
        self.SETUPER()
        self.TILES()
        self.COINS()
        self.HEALTHS()
        self.PLAYERS()
        self.BULLETS()
        self.TRACERS()
        self.MIRRORS()
        self.BOMBS()
        self.DOOR()       
        #self.pauser()
        #self.health.draw(self.display_surface)
        

