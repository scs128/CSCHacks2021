import pygame
from pygame.sprite import collide_mask, collide_rect
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
obstacle_list= ['./Art/barrel.png','./Art/table_no_cloth.png']# list of sprites to be loaded in as obstacles
player_speed = 3 # number of pixels player moves per action

gameDisplay = pygame.display.set_mode((display_width, display_height)) #set up frame for game
pygame.display.set_caption('Rogue-Like') #change title on the game window
clock = pygame.time.Clock() #pygame clock based off frames apparently

#playerImg = pygame.image.load('baldGuy.png') #load player image

class Obstacle(pygame.sprite.Sprite):#creates a class of obstacles for loading and spawning
    def __init__(self):
        super()
        self.image = pygame.image.load(obstacle_list[0])#can be used to blit later
        self.x = 100#spawning coordinates will proabably be randomized at somepoint
        self.y = 100
        self.rect = pygame.Rect(self.x,self.y, 32,32)# creates a rectangle and may not be strictly necessary if using collide_mask

obstacle_sprites = pygame.sprite.Group()#i think delete or figure out how groups work later
obstacle  = Obstacle()#makes Obstacle easier to work with

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super()
        self.image = pygame.image.load("./Art/Oswaldo_Up.png")
        self.rect = self.image.get_rect()

        self.x = 300
        self.y = 300#spawning for Oswaldo
        self.speed_x = 3
        self.speed_y = 3#speed of as Oswaldo in the x and y directions seperation is needed for collision

        self.direction = "UP"

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            if self.speed_x == 0 and self.direction != "LEFT": #makes it so you can move right away from obstacle applies to all of the things 
                self.speed_x = 3
            self.direction = "LEFT"
            self.x -= self.speed_x
        elif pressed_keys[pygame.K_RIGHT]:
            if self.speed_x == 0 and self.direction != "RIGHT":
                self.speed_x = 3
            self.direction = "RIGHT"
            self.x += self.speed_x
        elif pressed_keys[pygame.K_DOWN]:
            if self.speed_y == 0 and self.direction != "DOWN":
                self.speed_y = 3
            self.direction = "DOWN"
            self.y += self.speed_y
        elif pressed_keys[pygame.K_UP]:
            if self.speed_y == 0 and self.direction != "UP":
                self.speed_y = 3
            self.direction = "UP"
            self.y -= self.speed_y

        gameDisplay.blit(self.image, (self.x, self.y))


        self.rect.topleft = (self.x, self.y)
        #pygame.draw.rect(gameDisplay, black, self.rect)
            
        
    def update(self):
        pass

    def attack(self):
        pass

#def player(x, y):
    #gameDisplay.blit(pygame.image.load('./Art/Oswaldo_Up.png'), (x,y)) #draw carImg onto background at (x,y) coordinates
 
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
    collide = pygame.sprite.collide_rect(player,obstacle)

    while not exit_game:
        for event in pygame.event.get():  # event handling loop (inputs and shit)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            #if event.type == pygame.KEYDOWN: # basic movement currently with just one image, implement movement images
                #if event.key == pygame.K_LEFT:
                    #x_change = -player_speed
                #if event.key == pygame.K_RIGHT:
                    #x_change = player_speed
                #if event.key == pygame.K_UP:
                    #y_change = -player_speed
                #if event.key == pygame.K_DOWN:
                    #y_change = player_speed

            #if event.type == pygame.KEYUP: # stop moving in a direction
                #if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    #x_change = 0
                #if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    #y_change = 0

        # change player coordinates then draw
        #x += x_change
        #y += y_change


        # check collision with walls
        #if y + character_size >= display_height - tile_size*2 :
            #y_change = 0
            #y = display_height - tile_size*2 - character_size
        #elif y <= 64 - 16:
            #y_change = 0
            #y = 64 - 16
        #if x <= 32:
            #x_change = 0
            #x = 32
        #elif x >= display_width - tile_size - character_size:
            #x_change = 0
            #x = display_width - tile_size - character_size

        
        gameDisplay.fill(white) # must order this and next line because otherwise fill would fill over the car
        ### Draw scenery then enemies here ###
        room()

        player.move()
        gameDisplay.blit(obstacle.image,(obstacle.x,obstacle.y,))#this is currently bliting barrel probably a better way to do this
        #probably needs to be in a loop to load multiple obstacles

        if collide_mask (player,obstacle) and player.direction == "LEFT":#collision_mask checks for sprite mask collision which goes beyond rectangles i think
            player.speed_x = 0#sets player speed to zero if collides from the left and repeat for other ifs
        if collide_mask(player,obstacle) and player.direction == "RIGHT":
            player.speed_x = 0
        if collide_mask(player,obstacle) and player.direction == "UP":
            player.speed_y = 0
        if collide_mask(player,obstacle) and player.direction == "DOWN":
            player.speed_y = 0
            #may need to change this to 4 speeds because rn collision is awkward if attempting to switch movement axis 
            # want to check if issue is resoved with collide_rect rather than mask  
                    #UNTESTED AS OF: 10/15 10:27
        
        

        
        ### Draw scenery then enemies here ###
        #player(x, y)

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