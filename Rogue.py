import pygame
import random
import math
from pygame.sprite import collide_mask, collide_rect, collide_rect_ratio

#blah blah blah

# must be an even multiple of 32
display_width = 512
display_height = 512

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

tile_size = 32 # pixel size per tile
character_size = 32

player_speed = 3 # number of pixels player moves per action

gameDisplay = pygame.display.set_mode((display_width, display_height)) #set up frame for game
pygame.display.set_caption('Rogue-Like') #change title on the game window
clock = pygame.time.Clock() #pygame clock based off frames apparently

#playerImg = pygame.image.load('baldGuy.png') #load player image

class Obstacle(pygame.sprite.Sprite):#creates a class of obstacles for loading and spawning
    obstacle_list = ['./Art/barrel.png','./Art/table_no_cloth.png']# list of sprites to be loaded in as obstacles

    def __init__(self):
        super()
        self.image = pygame.image.load(self.obstacle_list[0])#can be used to blit later
        self.x = 100#spawning coordinates will proabably be randomized at somepoint
        self.y = 100
        self.width  = self.image.get_width()
        self.height =  self.image.get_height()#if ~8 pixels are subtracted can be used to make depth but then have to figure out redraw so you dont slid under other sprites
        self.rect = self.image.get_rect()# creates a rectangle and may not be strictly necessary if using collide_mask
        self.rect.topleft = (self.x,self.y)
        self.rect.inflate_ip(-5,-5)
    def draw(self):
        gameDisplay.blit(self.image, (self.x, self.y,))#this is currently bliting barrel probably a better way to do this

#obstacle_sprites = pygame.sprite.Group()#i think delete or figure out how groups work later


class Player(pygame.sprite.Sprite):
    walk_up = ["./Art/Oswaldo_Up.png", "./Art/Oswaldo_Up_Left.png", "./Art/Oswaldo_Up_Right.png"]
    walk_right = ["./Art/Oswaldo_Right.png", "./Art/Oswaldo_Right_Left.png", "./Art/Oswaldo_Right_Right.png"]
    walk_left = ["./Art/Oswaldo_Left.png", "./Art/Oswaldo_Left_Left.png", "./Art/Oswaldo_Left_Right.png"]
    walk_down = ["./Art/Oswaldo_Down.png", "./Art/Oswaldo_Down_Left.png", "./Art/Oswaldo_Down_Right.png"]

    def __init__(self):
        super()
        self.image = pygame.image.load(self.walk_up[0])
        self.rect = self.image.get_rect()

        self.x = 0
        self.y = 0
        self.speed_x = 3
        self.speed_y = 3
        self.direction = "UP"
        self.walk_count = 0
        self.health = 6
        self.vulnerable = True
        self.clock = 0
        

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_a]:
            if self.speed_x == 0 and self.direction != "LEFT": #makes it so you can move right away from obstacle applies to all of the things 
                self.speed_x = 3
            if self.direction != "LEFT" or self.walk_count + 1 >= 27:
                self.walk_count = 0
            self.direction = "LEFT"
            self.x -= self.speed_x
            self.image = pygame.image.load(self.walk_left[self.walk_count//9])
            self.walk_count += 1
        elif pressed_keys[pygame.K_d]:
            if self.speed_x == 0 and self.direction != "RIGHT":
                self.speed_x = 3
            if self.direction != "RIGHT" or self.walk_count + 1 >= 27:
                self.walk_count = 0
            self.direction = "RIGHT"
            self.x += self.speed_x
            self.image = pygame.image.load(self.walk_right[self.walk_count//9])
            self.walk_count += 1
        elif pressed_keys[pygame.K_s]:
            if self.speed_y == 0 and self.direction != "DOWN":
                self.speed_y = 3
            if self.direction != "DOWN" or self.walk_count + 1 >= 27:
                self.walk_count = 0
            self.direction = "DOWN"
            self.y += self.speed_y
            self.image = pygame.image.load(self.walk_down[self.walk_count//9])
            self.walk_count += 1
        elif pressed_keys[pygame.K_w]:
            if self.speed_y == 0 and self.direction != "UP":
                self.speed_y = 3
            if self.direction != "UP" or self.walk_count + 1 >= 27:
                self.walk_count = 0
            self.direction = "UP"
            self.y -= self.speed_y
            self.image = pygame.image.load(self.walk_up[self.walk_count//9])
            self.walk_count += 1

        gameDisplay.blit(self.image, (self.x, self.y))


        self.rect.topleft = (self.x, self.y)
        #pygame.draw.rect(gameDisplay, black, self.rect)
            
        
    def update(self):
        pass

    def attack(self):
        pass

class Enemy(object):
    walk = [pygame.image.load('./Art/warrior.png')]

    def __init__(self, x, y, end):
        self.x= x
        self.y = y
        self.image = pygame.image.load('./Art/warrior.png')
        self.path = [x, end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 1
        self.rect = self.image.get_rect()

    def draw(self, player):
        self.move(player)
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        
        if self.vel > 0:
            gameDisplay.blit(self.walk[0], (self.x,self.y))
            self.rect.topleft = (self.x, self.y)
           # gameDisplay.blit(self.walk[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1

    def move(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.x - self.x, player.y - self.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.x += dx * self.vel
        self.y += dy * self.vel
        self.damage(player, dx, dy)

    def damage(self, player, dx, dy):
        if collide_rect (self, player) and player.vulnerable:
            player.health -= 1
            player.x += dx * 15
            player.y += dy * 15
            player.vulnerable = False
            print(player.health)
            if player.health <= 0:
                pygame.quit()
                quit()
            

 
def room():
    #if display_width == 320 and display_height == 320:
        #gameDisplay.blit(pygame.image.load('./Art/floortiles_320x320.png'), (0, 0))
    #elif display_width == 640 and display_height == 640:
    gameDisplay.blit(pygame.image.load('./Art/floortiles_640x640.png'), (0, 0))
    
    # create top row of walls
    gameDisplay.blit(pygame.image.load('./Art/wall_topleft.png'), (0, 0))
    gameDisplay.blit(pygame.image.load('./Art/wall_top_ns.png'), (0, tile_size))
    gameDisplay.blit(pygame.image.load('./Art/wall_topright.png'), (display_width-tile_size, 0))
    gameDisplay.blit(pygame.image.load('./Art/wall_top_ns.png'), (display_width-tile_size, tile_size))

    for x in range(1, int(display_width/32 - 1)):
        gameDisplay.blit(pygame.image.load('./Art/wall_straight.png'), (tile_size*x, 0))

    # create floor rows and side walls
    for y in range(2, int(display_height/32 - 2)):
        gameDisplay.blit(pygame.image.load('./Art/wall_top_ns.png'), (0, tile_size*y))
        gameDisplay.blit(pygame.image.load('./Art/wall_top_ns.png'), (display_width-tile_size, tile_size*y))

    # create bottom walls
    gameDisplay.blit(pygame.image.load('./Art/wall_bottomleft.png'), (0, display_height-tile_size*2))
    gameDisplay.blit(pygame.image.load('./Art/wall_bottomright.png'), (display_width-tile_size, display_height-tile_size*2))
    for x in range(1, int((display_width/32)/2 - 2)):
        gameDisplay.blit(pygame.image.load('./Art/wall_straight.png'), (tile_size*x, display_height-tile_size*2))
    for x in range(int((display_width/32)/2 + 2), int(display_width/32 - 1)):
        gameDisplay.blit(pygame.image.load('./Art/wall_straight.png'), (tile_size*x, display_height-tile_size*2))
        
    gameDisplay.blit(pygame.image.load('./Art/wall_right_end.png'), (((display_height/32)/2 - 2)*tile_size, display_height-tile_size*2))
    gameDisplay.blit(pygame.image.load('./Art/wall_left_end.png'), (((display_height/32)/2 + 1)*tile_size, display_height-tile_size*2))


def game_loop():
    
    x = (display_width * 0.45)
    y = (display_height * 0.5)
    x_change = 0
    y_change = 0

    exit_game = False

    player = Player()
    obstacle  = Obstacle()#makes Obstacle easier to work with

    k = random.randint(tile_size,display_width-tile_size-character_size)

    bigbad = Enemy(k,random.randint(tile_size*2,display_height-(tile_size*2)-character_size), k + 200)

    while not exit_game:
        for event in pygame.event.get():  # event handling loop (inputs and shit)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white) # must order this and next line because otherwise fill would fill over the car
        ### Draw scenery then enemies here ###
        room()

        obstacle.draw()
        bigbad.draw(player)
        player.move()
        #bigbad.damage(player)
        #pygame.draw.rect(gameDisplay,green,player.rect)
        #pygame.draw.rect(gameDisplay,red,obstacle.rect)

        if collide_rect (player,obstacle) and player.direction == "LEFT":#collision_mask checks for sprite mask collision which goes beyond rectangles i think
            player.x = obstacle.rect.right #sets player speed to zero if collides from the left and repeat for other ifs
        if collide_rect(player,obstacle) and player.direction == "RIGHT":
            player.x = obstacle.rect.left - (player.image.get_width())
        if collide_rect(player,obstacle) and player.direction == "UP":
            player.y = obstacle.rect.bottom
        if collide_rect(player,obstacle) and player.direction == "DOWN":
            player.y = obstacle.rect.top -  (player.image.get_height())

        
        if not player.vulnerable:
            player.clock += 1
            if player.clock >= 180:
                player.clock = 0
                player.vulnerable = True

        ### Draw scenery then enemies here ###
        #player(x, y)

        pygame.display.update() #also can use pygame.display.flip(), update allows a parameter to specifically update
        clock.tick(60) #sets frames per second


game_loop()
pygame.quit() #stop pygame from running
quit() #end program




############################
#TODO: Solidify collision with objects and walls------DONE
#TODO: Enemies walk towards player------DONE
#TODO: Enemy Sprites and animation
#TODO: Enemy damage player when collision boxes touch-----DONE
#TODO: Create system for placing multiple objects around the room