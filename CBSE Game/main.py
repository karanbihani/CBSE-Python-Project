#from ast import Global
from lib2to3.pgen2.token import NAME
import pygame
import sys
from random import *
from pygame.constants import QUIT
import mysql.connector as sql
from tkinter import *

STATS = ()

#User defined modules
from settings import *
from level import Level
from level_data import levels
from level_menue_data import menue_level
from menue import Menue

pygame.init()

# tkinter login

def gate():
    USERNAME = username.get()
    PASSWORD = password.get()

    con = sql.connect(host = 'localhost', user = 'root', password = 'Bihani123', database = 'quacktable')
    cur = con.cursor()

    pqry = f"select pass,plct,uname from login where uname = '{USERNAME}';"
    cur.execute(pqry)
    pry = cur.fetchall()

    if pry:
        if pry[0][0] == PASSWORD and pry[0][1]>0:
            global STATS
            q = f"select uname,level,coinct,win from plays where uname = '{USERNAME}' order by tolp;"
            cur.execute(q)
            s = cur.fetchall()
            if s[-1][3] == 0:
                STATS = s[-1][0:3]
            else:
                STATS = (USERNAME,0,0)
            root.destroy()

        elif pry[0][0] == PASSWORD and pry[0][1]==0:
            STATS = (USERNAME,0,0)
            root.destroy()

        elif PASSWORD != pry[0][0]:
            message.delete('1.0',END)
            message.insert(END,'Incorrect Password')
        else:
            message.delete('1.0',END)
            message.insert(END,'Error')
    else:
        message.delete('1.0',END)
        message.insert(END,'Invalid Username. Try again or Register')

def registeration():
    
    USERNAME = username.get()
    PASSWORD = password.get()

    con = sql.connect(host = 'localhost', user = 'root', password = 'Bihani123', database = 'quacktable')
    cur = con.cursor()

    pqry = f"select pass from login where uname = '{USERNAME}';"
    cur.execute(pqry)
    pry = cur.fetchall()

    if pry :
        if PASSWORD == pry[0][0]:
            gate()
        else:
            message.delete('1.0',END)
            message.insert(END,'Username already exists')
    else:
        q = f'insert into login (uname, pass) values("{USERNAME}","{PASSWORD}");'
        cur.execute(q)
        con.commit()
        message.delete('1.0',END)
        message.insert(END,'Successfully Registered ! Click Login')
    
def clearing():
    username.delete(0,END)
    password.delete(0,END)

root = Tk()
root.title('Student Data')

username = Entry(root,borderwidth=5)
username.insert(0,'Username')
password = Entry(root,borderwidth=5)
password.insert(0,'Password')
message = Text(root,borderwidth=5,width = 55,height =  3)
message.insert(END,'''Enter UserName and Passwd.
 Register if first time user 
 Login for preexisting account''')

login = Button(root,width=55,text='Login',command=gate)
clear = Button(root,width=55,text='Clear',command=clearing)
register = Button(root, width = 55, text = 'Register', command = registeration)

username.grid(row=0,column=0)
password.grid(row=0,column=1)
login.grid(row=3,column=0,columnspan=2)
clear.grid(row=4,column=0,columnspan=2)
register.grid(row=2,column=0,columnspan=2)
message.grid(row=1,column = 0,columnspan=2)

root.mainloop()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Agent Quack 007')
clock = pygame.time.Clock()

game_bg = pygame.image.load('Assets\Images\Background\game_bg.png').convert_alpha()
game_bg = pygame.transform.scale(game_bg,(1200,700))

menu_bg = pygame.image.load('Assets\Images\Background\menu_bg.png').convert_alpha()
menu_bg = pygame.transform.scale(game_bg,(1200,700))

class Game():
    #need to add cheker if ther is old data if nto start new with standard data
    def __init__(self,levels,menue_level,username,current_level,coin_ct,game_bg, menu_bg): # 26/2 --  need to take coin_ct , username , 
        self.current_level = current_level 
        self.coin_ct = coin_ct
        self.username = username
        self.menu_bg = menu_bg
        self.game_bg = game_bg
        self.menue_level = menue_level
        self.levels = levels
        self.level = Level(self.levels, SCREEN, self.username, self.current_level ,self.coin_ct,game_bg) # ok understood
        self.menue = Menue(self.menue_level,SCREEN,3,menu_bg)
        self.game_active = True
        
    def run(self):#mode is 0,1  where 0 is menue and 1 is game
        if self.game_active:
            SCREEN.blit(self.game_bg, (0,0))
            game.level.run() 
            self.current_level = self.level.current_level
            self.game_active = self.level.game_active
            if not self.game_active:
                self.menue = Menue(self.menue_level, SCREEN, self.current_level,self.menu_bg)
            if self.current_level == 3:
                print('You Won')
                con = sql.connect(host = 'localhost', user = 'root', password = 'Bihani123', database = 'quacktable')
                if con.is_connected():
                    cur = con.cursor()
                    q = (f'insert into plays (uname,coinct,level,win) values("{self.username}", {self.level.coins_counter_old}, {self.current_level}, 1);')
                    cur.execute(q)
                    con.commit()
                    q2 = (f'update login set plct = plct + 1')
                    cur.execute(q2)
                    con.commit()
                    pygame.quit()
                    sys.exit()
                else:
                    print('Mysql connection not made, please check')  
        
        else:
            self.coin_ct = self.level.coins_counter_old
            SCREEN.blit(self.menu_bg, (0,0))
            game.menue.run()
            self.game_active = self.menue.game_active
            if self.game_active:        
                self.level = Level(self.levels, SCREEN, self.username, self.current_level, self.coin_ct, self.game_bg)

game = Game(levels, menue_level, STATS[0],STATS[1],STATS[2] ,game_bg,menu_bg)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()   
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
    
    if game.game_active == True:
        SCREEN.blit(game_bg, (0,0))
    else:
        SCREEN.blit(menu_bg, (0,0))

    game.run()    

    pygame.display.update()
    clock.tick(FPS)
