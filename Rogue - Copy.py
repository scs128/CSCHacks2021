import pygame

# must be an even multiple of 32
display_width = 320
display_height = 320

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

tile_size = 32 # pixel size per tile

player_speed = 3 # number of pixels player moves per action

gameDisplay = pygame.display.set_mode((display_width, display_height)) #set up frame for game
pygame.display.set_caption('Rogue-Like') #change title on the game window
clock = pygame.time.Clock() #pygame clock based off frames apparently

#playerImg = pygame.image.load('baldGuy.png') #load player image

obstacles_list = ['./Art/barrel.png']

def obstable_maker(list_index):
    gameDisplay.blit(pygame.image.load(obstacles_list[list_index]),(32,48))
    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./Art/warrior.png')
        self.rect = self.image.get_rect()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,list_index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(obstacles_list[list_index])
        self.rect = self.image.get_rect()

player_sprite = Player()
obstable_group = pygame.sprite.Group()
obstacle  = Obstacle()
obstable_group.add(obstacle)

def hit_check():
    hit = pygame.sprite.spritecollide(player_sprite, obstacle, False)
    if hit:
        player_sprite 

def player(x, y):
        gameDisplay.blit(pygame.image.load('./Art/warrior.png'), (x,y)) #draw carImg onto background at (x,y) coordinates
    
def walls():
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
        for x in range(1, int(display_width/32 - 1)):
            gameDisplay.blit(pygame.image.load('./Art/floortile.png'), (tile_size*x, tile_size*y))

    # create bottom walls
    gameDisplay.blit(pygame.image.load('./Art/wall_bottomleft.png'), (0, display_height-tile_size*2))
    gameDisplay.blit(pygame.image.load('./Art/wall_bottomright.png'), (display_width-tile_size, display_height-tile_size*2))
    for x in range(1, int((display_width/32)/2 - 2)):
        gameDisplay.blit(pygame.image.load('./Art/wall_straight.png'), (tile_size*x, display_height-tile_size*2))
    for x in range(int((display_width/32)/2 + 2), int(display_width/32 - 1)):
        gameDisplay.blit(pygame.image.load('./Art/wall_straight.png'), (tile_size*x, display_height-tile_size*2))
        
    gameDisplay.blit(pygame.image.load('./Art/wall_right_end.png'), (((display_height/32)/2 - 2)*tile_size, display_height-tile_size*2))
    gameDisplay.blit(pygame.image.load('./Art/wall_left_end.png'), (((display_height/32)/2 + 1)*tile_size, display_height-tile_size*2))

    # fill in floor in bottom doorway
    gameDisplay.blit(pygame.image.load('./Art/floortile.png'), (((display_height/32)/2 - 1)*tile_size, display_height-tile_size*2))
    gameDisplay.blit(pygame.image.load('./Art/floortile.png'), (((display_height/32)/2)*tile_size, display_height-tile_size*2))
    gameDisplay.blit(pygame.image.load('./Art/floortile.png'), (((display_height/32)/2 - 1)*tile_size, display_height-tile_size))
    gameDisplay.blit(pygame.image.load('./Art/floortile.png'), (((display_height/32)/2)*tile_size, display_height-tile_size))

def player_hitbox(x,y):
    rect1 = pygame.Rect(0,0, )


def game_loop():
    
    
    x = (display_width * 0.45)
    y = (display_height * 0.8)
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
        gameDisplay.fill(white) # must order this and next line because otherwise fill would fill over the car
        ### Draw scenery then enemies here ###
        walls()


        ### Draw scenery then enemies here ###
        player(x, y)
        obstable_maker(0)

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