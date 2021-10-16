from os import walk
import pygame
import random

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



def player(x, y):
    gameDisplay.blit(pygame.image.load('./Art/warrior.png'), (x,y)) #draw carImg onto background at (x,y) coordinates

class enemy(object):
    walk = [pygame.image.load('./Art/warrior.png')]

    def __init__(self, x, y,end):
        self.x= x
        self.y = y
        self.path = [x, end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = random.randrange(2,6)
    def draw(self,gameDisplay):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        
        if self.vel > 0:
            gameDisplay.blit(self.walk[0], (self.x,self.y))
           # gameDisplay.blit(self.walk[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        else:
            gameDisplay.blit(self.walk[0], (self.x,self.y))
            self.walkCount += 1

    def move(self):
        if self.vel > 0:  # If we are moving right
            if self.x < self.path[1] + self.vel: # If we have not reached the furthest right point on our path.
                self.x += self.vel
            else: # Change direction and move back the other way
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else: # If we are moving left
            if self.x > self.path[0] - self.vel: # If we have not reached the furthest left point on our path
                self.x += self.vel
            else:  # Change direction
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0






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

i = random.randint(tile_size,display_width-tile_size-character_size)
bigbad = enemy(i,random.randint(tile_size*2,display_height-(tile_size*2)-character_size), i + 200)
                
def game_loop():
    

    x = (display_width * 0.45)
    y = (display_height * 0.5)
    x_change = 0
    y_change = 0

    exit_game = False

    while not exit_game:
        for event in pygame.event.get():  # event handling loop (inputs and shit)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
      
            if event.type == pygame.KEYDOWN: # basic movement currently with just one image, implement movement images
                if event.key == pygame.K_LEFT:
                    x_change = -player_speed
                if event.key == pygame.K_RIGHT:
                    x_change = player_speed
                if event.key == pygame.K_UP:
                    y_change = -player_speed
                if event.key == pygame.K_DOWN:
                    y_change = player_speed

            if event.type == pygame.KEYUP: # stop moving in a direction
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        # change player coordinates then draw
        x += x_change
        y += y_change

        # check collision with walls
        if y + character_size >= display_height - tile_size*2 :
            y_change = 0
            y = display_height - tile_size*2 - character_size
        elif y <= 64 - 16:
            y_change = 0
            y = 64 - 16
        if x <= 32:
            x_change = 0
            x = 32
        elif x >= display_width - tile_size - character_size:
            x_change = 0
            x = display_width - tile_size - character_size


        gameDisplay.fill(white) # must order this and next line because otherwise fill would fill over the car
        ### Draw scenery then enemies here ###
        room()
        
        ### Draw scenery then enemies here ###
        player(x, y)
        bigbad.draw(gameDisplay)

        pygame.display.update() #also can use pygame.display.flip(), update allows a parameter to specifically update
        clock.tick(120) #sets frames per second


game_loop()
pygame.quit() #stop pygame from running
quit() #end program



##############################################
############# Background Needs ###############
# 1. Simply place tiles in proper spots to make a room
# 2. Create collision with walls
# 3. Place Items to decorate room
# 4. Implement "grid" placement of tiles
# 5. Create door to another room
# 6. 
#
#
#
#
#