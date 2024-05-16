#This file was created by: Spencer Maffeo
# Appreciation to Chris Bradfield


import pygame as pg
from settings import *
from random import choice
from random import randint
from os import path
import math


# needed for animated sprite
SPRITESHEET = "theBell.png"
# needed for animated sprite
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
# needed for animated sprite
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # needed for animated sprite
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        # needed for animated sprite
        self.facing = 'right'
        self.load_images()
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.coinbag = 0
        self.unlock = 0
        self.bbag = 1
        self.b2bag = 1
        self.b3bag = 1
        self.speed = 300
        self.status = ""
        self.hitpoints = 1
        self.running = True
        # written by Chat GPT
        self.last_update = pg.time.get_ticks() 
        self.current_frame = 0
        self.sword = None  # Initialize the sword attribute
        self.attack_cooldown = 500  # Cooldown time for sword swing in milliseconds
        self.last_attack_time = 0  # Time of the last sword swing


    # def attack(self):
    #     if self.sword is None:
    #         self.sword = Sword(self)
    #     # Optionally, add a cooldown or animation for the attack
    #     now = pg.time.get_ticks()
    #     if now - self.last_attack_time > self.attack_cooldown:
    #         self.last_attack_time = now
    #         self.sword.swing()  # Swing the sword
    #         # Check for collision with enemies and deal damage
    #         hits = pg.sprite.spritecollide(self.sword, self.game.enemy, False)
    #         for enemy in hits:
    #             enemy.take_damage(self.sword.damage)
    
    #written by chat gpt
    def attack(self):
        if self.sword is None or not self.sword.swinging:
            self.sword = Sword(self)
            self.sword.swing() 
        # if self.sword is None:
        #     self.sword = Sword(self)
        now = pg.time.get_ticks()
        if now - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = now
            self.sword.swing()  # Swing the sword
            # Check for collision with enemies and deal damage
            for enemy in self.game.enemy:
                if pg.sprite.collide_rect(self.sword, enemy):
                    enemy.take_damage(self.sword.damage)

            for blocks in self.game.blocks:
                if pg.sprite.collide_rect(self.sword, blocks):
                    blocks.take_damage(self.sword.damage)

            for blocks2 in self.game.blocks2:
                if pg.sprite.collide_rect(self.sword, blocks2):
                    blocks2.take_damage(self.sword.damage)

            for blocks3 in self.game.blocks3:
                if pg.sprite.collide_rect(self.sword, blocks3):
                    blocks3.take_damage(self.sword.damage)
    
    def get_keys(self):
        self.vx, self.vy = 0, 0 
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
            self.facing = 'up'
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
            self.facing = 'down'
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        if keys[pg.K_SPACE]:
            self.attack()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
            self.facing = 'left'
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
            self.facing = 'right'


    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    def collide_with_door(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.door, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.door, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y


    
    
    
    # def collide_with_group(self, group, kill):
    #     hits = pg.sprite.spritecollide(self, group, kill)
    #     if hits:
    #         if str(hits[0].__class__.__name__) == "PowerUp":
    #             print(hits[0].__class__.__name__)
    #             self.speed += 500
            
 # needed for animated sprite
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.

    # needed for animated sprite        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom


            

    def update(self):
        self.animate()
        self.get_keys()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_door('x')
        self.collide_with_door('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        # I made it so that you collide with enemy the same way you collide with a coin. 
        self.collide_with_group(self.game.enemy, True)
        self.collide_with_group(self.game.coins2, True)
        self.collide_with_group(self.game.switch, True)
        if self.sword:
            # Only check for collisions if the player has a sword
            hits = pg.sprite.spritecollide(self.sword, self.game.enemy, True)
            for enemy in hits:
                enemy.take_damage(self.sword.damage)
            hits = pg.sprite.spritecollide(self.sword, self.game.enemy, True)
            for blocks in hits:
                blocks.take_damage(self.sword.damage)

            hits = pg.sprite.spritecollide(self.sword, self.game.enemy, True)
            for blocks2 in hits:
                blocks2.take_damage(self.sword.damage)
            
            hits = pg.sprite.spritecollide(self.sword, self.game.enemy, True)
            for blocks3 in hits:
                blocks3.take_damage(self.sword.damage)
            


# 
# 
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            #when you collide with enemy your hitpoints go to 0 and the game restarts
            if str(hits[0].__class__.__name__) == 'Enemy':
                print("you died")
                self.hitpoints -=1
                # pg.quit()
                # sys.exit()
            if str(hits[0].__class__.__name__) == "Coin":
                print("you got a coin")
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "Coin2":
                print("you got a coin")
                self.coinbag += 1
            if str(hits[0].__class__.__name__) == "Powerup":
                print("you got a speed boost")
                self.speed += 150
            if str(hits[0].__class__.__name__) == "Switch":
                print("you unlocked the door")
                self.unlock += 5
            
        
            
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE





        
class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):

        self.groups = game.all_sprites, game.enemy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
        self.hitpoints = 1  # Set initial hitpoints
        

    def take_damage(self, damage):
        self.hitpoints -= damage
        if self.hitpoints <= 0:
            self.kill()  # Remove the enemy when hitpoints reach zero

    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        # self.collide_with_walls('x')
        self.rect.y = self.y
        # self.collide_with_walls('y')



class Powerup(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


# written by chat gpt
class Sword(pg.sprite.Sprite):
    def __init__(self, player):
        super().__init__(player.game.all_sprites)
        self.player = player
        self.image = pg.Surface((40, 10), pg.SRCALPHA)  # Create a transparent surface for the sword
        pg.draw.rect(self.image, pg.Color(YELLOW), (0, 0, 40, 10))
        self.rect = self.image.get_rect()
        self.damage = 1  # Set the damage inflicted by the sword
        self.swinging = False  # Flag to indicate if the sword is swinging
        self.swing_duration = 300  # Duration of the swing in milliseconds
        self.swing_timer = 0  # Timer to keep track of the swing duration
        self.swing_speed = 0.2  # Speed of swing rotation (adjust as needed)
        self.swing_radius = 50  # Radius of swing arc (adjust as needed)
        self.swing_angle = 0  # Initial swing angle
        self.update_position()

    def update_position(self):
        # Update the position of the sword based on player's position and facing direction
        if self.player.facing == 'right':
            self.rect.midleft = self.player.rect.midright
            self.swing_angle = -45  # Set initial swing angle for right-facing player
        elif self.player.facing == 'left':
            self.rect.midright = self.player.rect.midleft
            self.swing_angle = 180  # Set initial swing angle for left-facing player
        elif self.player.facing == 'up':
            self.rect.midtop = self.player.rect.midtop
            self.swing_angle = 255  # Set initial swing angle for up-facing player
        elif self.player.facing == 'down':
            self.rect.midbottom = self.player.rect.midbottom
            self.swing_angle = 45  # Set initial swing angle for down-facing player

    def swing(self):
        # Method to initiate the sword swing action
        if not self.swinging:  # Only swing if the sword is not already swinging
            self.swinging = True
            self.swing_timer = pg.time.get_ticks()  # Start the swing timer

    def update(self):
        # Update the position of the sword each frame
        self.update_position()

        # Check if the sword is swinging
        if self.swinging:
            # Calculate the swing angle based on time and speed
            time_elapsed = pg.time.get_ticks() - self.swing_timer
            self.swing_angle += self.swing_speed * time_elapsed

            # Calculate the new position of the sword based on swing arc
            x_offset = self.swing_radius * math.cos(math.radians(self.swing_angle))
            y_offset = self.swing_radius * math.sin(math.radians(self.swing_angle))
            self.rect.centerx = self.player.rect.centerx + x_offset
            self.rect.centery = self.player.rect.centery + y_offset

            # Check if the swing duration has elapsed
            if time_elapsed > self.swing_duration:
                self.swinging = False  # End the swing if duration is over
                self.kill()  # Remove the sword from the game


class Switch(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.switch
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE



class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.door
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        



class Block(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player = Player
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.hitpoints = 100
        # self.bbag = 1

        
    def take_damage(self, damage):
        self.hitpoints -= damage
    
        if self.hitpoints == 99:
            self.image.fill(RED)
            self.game.player.bbag += 2  # Accessing bbag through an instance of Player
        if self.hitpoints == 98:
            self.image.fill(PURPLE)
            self.game.player.bbag -= 1  # Accessing bbag through an instance of Player
        # if self.hitpoints == 97:
        #     self.image.fill(PINK)
        #     self.bbag -= 1
        # if self.hitpoints == 96:
        #     self.image.fill(RED)
        #     self.bbag +=2
        # if self.hitpoints == 95:
        #     self.image.fill(PURPLE)
        #     self.bbag -= 1
        # if self.hitpoints == 94:
        #     self.image.fill(PINK)
        #     self.bbag -= 1
        # if self.hitpoints == 93:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints == 92:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints == 91:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints == 90:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints == 89:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints == 88:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints <= 87:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints <= 86:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints <= 85:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints <= 84:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints <= 83:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints <= 82:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints <= 81:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints <= 80:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints <= 79:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints <= 78:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints <= 77:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints <= 76:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints <= 75:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints <= 74:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints <= 73:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints <= 72:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints <= 71:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints <= 70:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints <= 69:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints <= 68:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints <= 67:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints <= 66:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints <= 65:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints <= 64:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints <= 63:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints <= 62:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints <= 61:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints <= 60:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints <= 59:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints <= 58:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints <= 57:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints <= 56:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints <= 55:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        # if self.hitpoints <= 54:
        #     self.image.fill(RED)
        #     self.bbag =3
        # if self.hitpoints <= 53:
        #     self.image.fill(PURPLE)
        #     self.bbag = 2
        # if self.hitpoints <= 52:
        #     self.image.fill(PINK)
        #     self.bbag = 1
        



class Block2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.blocks2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.hitpoints = 100
        # self.b2bag = 1
        
        
    def take_damage(self, damage):
        self.hitpoints -= damage
        if self.hitpoints == 99:
            self.image.fill(RED)
            self.b2bag += 2
        if self.hitpoints == 98:
            self.image.fill(PURPLE)
            self.b2bag -= 1
        if self.hitpoints == 97:
            self.image.fill(PINK)
            self.b2bag -= 1
        if self.hitpoints == 96:
            self.image.fill(RED)
            self.b2bag += 2
        if self.hitpoints == 95:
            self.image.fill(PURPLE)
            self.b2bag -= 1
        if self.hitpoints == 94:
            self.image.fill(PINK)
            self.b2bag -= 1
#
#
#
#         if self.hitpoints <= 93:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 92:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 91:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 90:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 89:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 88:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 87:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 86:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 85:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 84:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 83:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 82:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 81:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 80:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 79:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 78:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 77:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 76:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 75:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 74:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 73:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 72:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 71:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 70:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 69:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 68:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 67:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 66:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 65:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 64:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 63:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 62:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 61:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 60:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 59:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 58:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 57:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 56:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 55:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 54:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 53:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 52:
#             self.image.fill(PINK)
#             self.b3bag = 1
        
        
        


class Block3(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.blocks3
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.hitpoints = 100
        # self.b3bag = 1

        
    def take_damage(self, damage):
        self.hitpoints -= damage
        if self.hitpoints == 99:
            self.image.fill(RED)
            self.b3bag += 2
        if self.hitpoints == 98:
            self.image.fill(PURPLE)
            self.b3bag -= 1
        if self.hitpoints == 97:
            self.image.fill(PINK)
            self.b3bag -= 1
        if self.hitpoints == 96:
            self.image.fill(RED)
            self.b3bag += 2
        if self.hitpoints == 95:
            self.image.fill(PURPLE)
            self.b3bag -= 1
        if self.hitpoints == 94:
            self.image.fill(PINK)
            self.b3bag -= 1
        if self.hitpoints == 93:
            self.image.fill(RED)
            self.b3bag =3
        if self.hitpoints == 92:
            self.image.fill(PURPLE)
            self.b3bag = 2
#         if self.hitpoints <= 91:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 90:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 89:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 88:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 87:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 86:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 85:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 84:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 83:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 82:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 81:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 80:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 79:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 78:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 77:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 76:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 75:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 74:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 73:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 72:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 71:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 70:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 69:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 68:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 67:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 66:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 65:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 64:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 63:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 62:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 61:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 60:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 59:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 58:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 57:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 56:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 55:
#             self.image.fill(PINK)
#             self.b3bag = 1
#         if self.hitpoints <= 54:
#             self.image.fill(RED)
#             self.b3bag =3
#         if self.hitpoints <= 53:
#             self.image.fill(PURPLE)
#             self.b3bag = 2
#         if self.hitpoints <= 52:
#             self.image.fill(PINK)
#             self.b3bag = 1
        

    
       


    
