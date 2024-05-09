# This file was created by Spencer Maffeo

'''
Beta Goal:

Create a weapon system and a way to kill enemies. 

create unique features for each level you progress such as:


add a boss fight and a way to beat the game. 






'''
# import libraries
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path

# added this math function to round down the clock
from math import floor

LEVEL1 = "map1.txt"
LEVEL2 = "map2.txt"
LEVEL3 = "map3.txt"


# this 'cooldown' class is designed to help us control time
class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            return x
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)



# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        self.all_sprites = pg.sprite.Group()
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # setting game clock 
        self.clock = pg.time.Clock()
        self.map_data = []
        self.load_data()
        self.running = True

        # added images folder and image in the load_data method for use with the player
    def load_data(self):
        self.game_folder = path.dirname(__file__)

        with open(path.join(self.game_folder, 'map1.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    def create_switches(self):
        # Create switches and place them in different rooms
        Switch(self, 2, 2)
        Switch(self, 8, 8)

    def change_level(self, lvl):
        # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
        # reset criteria for changing level
        self.player.moneybag = 0
        self.player.coinbag = 0
        self.player.unlock = 0
        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        # repopulate the level with stuff
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == 'x':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'e':
                    Enemy(self, col, row)
                if tile == 'T':
                    Powerup(self, col, row)
                if tile == 'c':
                    Coin2(self, col, row)
                if tile == 'S':
                    Switch(self,col, row)
                if tile == 'D':
                    Door(self, col, row)

                




    # Create run method which runs the whole GAME
    def new(self):
        self.test_timer = Cooldown()
        # print("create new game...")
        self.walls = pg.sprite.Group()            
        self.coins = pg.sprite.Group()
        self.coins2 = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()   
        self.player = pg.sprite.Group()   
        self.self = pg.sprite.Group()  
        self.door = pg.sprite.Group()
        self.switch = pg.sprite.Group()
        # self.healthbar = pg.sprite.Group()
        self.player.moneybag = 0
        self.player.coinbag = 0
        self.player.unlock = 0


       
    
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'x':
                    print("a wall at", row, col)
                    Wall(self, col, row)
               
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'e':
                    Enemy(self, col, row)
                if tile == 'T':
                    Powerup(self, col, row)
                if tile == 'c':
                    Coin2(self, col, row)
                if tile == 'S':
                    Switch(self,col, row)
                if tile == 'D':
                    Door(self, col, row)


    def update(self):
        self.test_timer.ticking()
        self.all_sprites.update()
        if self.player.hitpoints < 1:
                self.playing = False
        if self.player.moneybag > 4:
                self.change_level(LEVEL2)
        if self.player.moneybag > 2 and self.player.coinbag > 1:
            self.change_level(LEVEL3)
        if self.player.unlock > 4:
            for door in self.door:
                door.kill()


    def run(self):
        # 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
         pg.quit()
         sys.exit()

  
             
            
    
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)
    
    def draw(self):
            self.screen.fill(BGCOLOR)
            #self.draw_grid()
            self.all_sprites.draw(self.screen)
            #timer draw
            # self.draw_text(self.screen, str(self.test_timer.countdown(45)), 24, WHITE, WIDTH/2 - 32, 2)
            #moneybag draw
            # self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
            pg.display.flip()

    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
                
    def show_start_screen(self):
        if self.running == False:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Start Game - press any key to start", 24, WHITE, WIDTH/3.5 - 32, 2)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False





# Instantiate the game... 
g = Game()
# use game method run to run
# g.show_start_screen()
g.show_start_screen()
while True:
    g.new()
    g.run()