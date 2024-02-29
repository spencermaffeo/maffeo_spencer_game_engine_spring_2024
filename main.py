# This file was created by Spencer Maffeo


# import libraries
import pygame as pg
from settings import *
from sprites import *
import sys
from random import randint
from os import path

# creating a class named Game
class Game:
    # define a method with parameter 'self'
    def __init__(self):
        pg.init()
        # set width and height for display
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # set caption for display
        pg.display.set_caption("My first video game!")
        # set time clock for display
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.running = True
        # stores game info with this, ex. high scores
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
    
    # importing map data from the file map.txt
    
        

        '''
        with is a context manager, helps close or release resources
        after they are used, it prevents errors.
    
        '''
        # open map.txt and add lines into list (line)
        # with open (path.join(game_folder, 'map.txt'), 'rt') as f:
        #     for line in f:
        #         print(line)
        #         self.map_data.append(line)

    # add player sprite to Group
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        # self.player = Player(self,10,10)
        # self.all_sprites.add(self.player)
        
        #for x in range(10,20):
            #Wall(self,x,5)
        
        
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == 'x':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'e':
                    self.Enemy = Enemy(self,col,row)
                if tile == 'C':
                    Coin(self, col, row)
                

    # runs the game, game won't run without it
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # input
            self.events()
            # processing
            self.update()
            # output
            self.draw()
    
    # quits the game when you click the red x
    def quit(self):
        pg.quit()
        sys.exit()

    # method; tied to the class
    def input(self):
        pass

    # updates the position of all sprites on the grid
    def update(self):
        self.all_sprites.update()
        

    # draws the grid for our game
    def draw_grid(self):
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        
        for y in range (0,HEIGHT,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH,y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)


    # paints the background black & draws grid lines
    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
        pg.display.flip()


    def events(self):
        # listening for events
        for event in pg.event.get():
            # when you hit the red x the window closes and ends
            if event.type == pg.QUIT:
                self.quit()
                print ("the game has ended...")
            # player movement via arrow keys
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=+1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=+1)
            
    
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# call the class to run it
g = Game()
# g.show_start_screen()

while True:
    g.new()
    g.run()
    # g.show_go_screen()