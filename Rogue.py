import pygame
import random
from pygame import sprite
from pygame import image
from pygame.sprite import collide_mask, collide_rect, collide_rect_ratio
import math
#blah blah blah

# must be an even multiple of 32
display_width = 640
display_height = 640

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

    obstacle_list = ['./Art/barrel.png','./Art/table_no_cloth.png','./Art/table_cloth.png','./Art/potted_plant.png'
    ,'./Art/lab_bench_no_chem.png','./Art/lab_bench_chem.png','./Art/old_server.png']# list of sprites to be loaded in as obstacles

    def __init__(self,index):
        pygame.sprite.Sprite.__init__(self)
        super()
        self.image = pygame.image.load(self.obstacle_list[index])#can be used to blit later

        self.x = random.randint(32,400)
        self.y = random.randint(64, 400)
        self.width  = self.image.get_width()
        self.height =  self.image.get_height()#if ~8 pixels are subtracted can be used to make depth but then have to figure out redraw so you dont slid under other sprites
        self.rect = self.image.get_rect()# creates a rectangle and may not be strictly necessary if using collide_mask
        self.rect.topleft = (self.x,self.y)
        self.rect.inflate(-5,-5)
        
    def draw(self):
        gameDisplay.blit(self.image, (self.x, self.y,))#this is currently bliting barrel probably a better way to do this
#obstacle_sprites = pygame.sprite.Group()#i think delete or figure out how groups work later
#class Walls(pygame.sprite.Sprite):#creates a class of obstacles for loading and spawning
    #wall_list = ['./Art/wall_topleft.png','./Art/wall_top_ns.png']# list of sprites to be loaded in as obstacles
    
    #def __init__(self):
        #pygame.sprite.Sprite.__init__(self)
        #super()        
        #self.image = pygame.image.load(self.wall_list[1])      
        #self.width  = self.image.get_width()
        #self.height =  self.image.get_height()
        #self.x = 32
        #self.y = 0
        #self.rect = self.image.get_rect()
        #self.rect.topleft = (self.x,self.y)
    
def wall_boxes():
    top_wall =pygame.rect.Rect(0,0,display_width,48)
    left_wall = pygame.rect.Rect(0,0,32,display_height)
    right_wall = pygame.rect.Rect(display_width-32,0,32,display_height)
    botleft_wall = pygame.rect.Rect(0,display_height-64,display_width/2 -32,64)
    botright_wall = pygame.rect.Rect(botleft_wall.right,display_height-64,display_width/2,64)#altered to cover doorway
    #reset to (display_width/2 +32,display_height-64,display_width/2,64) to leave gap for door
    #pygame.draw.rect(gameDisplay,blue,top_wall)
    #pygame.draw.rect(gameDisplay,blue,left_wall)
    #pygame.draw.rect(gameDisplay,blue,right_wall)
    #pygame.draw.rect(gameDisplay,red,botleft_wall)
    #pygame.draw.rect(gameDisplay,green,botright_wall)
    walls = [top_wall,right_wall,left_wall,botleft_wall,botright_wall]
    return(walls)
    
def collision(player, obstacle):
    if collide_rect (player,obstacle) and player.direction == "LEFT":#collision_mask checks for sprite mask collision which goes beyond rectangles i think
            player.x = obstacle.rect.right #sets player speed to zero if collides from the left and repeat for other ifs
    if collide_rect (player,obstacle) and player.direction == "RIGHT":
            player.x = obstacle.rect.left - (player.image.get_width() )
    if collide_rect (player,obstacle) and player.direction == "UP":
            player.y = obstacle.rect.bottom
    if collide_rect (player,obstacle) and player.direction == "DOWN":
            player.y = obstacle.rect.top -  (player.image.get_height())
   

#obstacle_group = pygame.sprite.Group()        

class Player(pygame.sprite.Sprite):
    walk_up = ["./Art/Oswaldo_Up.png", "./Art/Oswaldo_Up_Left.png", "./Art/Oswaldo_Up_Right.png"]
    walk_right = ["./Art/Oswaldo_Right.png", "./Art/Oswaldo_Right_Left.png", "./Art/Oswaldo_Right_Right.png"]
    walk_left = ["./Art/Oswaldo_Left.png", "./Art/Oswaldo_Left_Left.png", "./Art/Oswaldo_Left_Right.png"]
    walk_down = ["./Art/Oswaldo_Down.png", "./Art/Oswaldo_Down_Left.png", "./Art/Oswaldo_Down_Right.png"]

    def __init__(self):
        super()
        self.image = pygame.image.load(self.walk_up[0])
        self.rect = self.image.get_rect()

        self.x = 300
        self.y = 300
        self.speed_x = 3
        self.speed_y = 3
        self.direction = "UP"
        self.walk_count = 0
        self.health = 6
        self.vulnerable = True
        self.can_attack = True
        self.vulnerability_clock = 0
        self.attack_clock = 0
        self.image_height = self.image.get_height()
        self.image_width = self.image.get_width()
        

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
    walk_up = ["./Art/BigBad_Up.png", "./Art/BigBad_Up_Left.png", "./Art/BigBad_Up_Right.png"]
    walk_right = ["./Art/BigBad_Right.png", "./Art/BigBad_Right_Left.png", "./Art/BigBad_Right_Right.png"]
    walk_left = ["./Art/BigBad_Left.png", "./Art/BigBad_Left_Left.png", "./Art/BigBad_Left_Right.png"]
    walk_down = ["./Art/BigBad_Down.png", "./Art/BigBad_Down_Left.png", "./Art/BigBad_Down_Right.png"]
    def __init__(self, x, y):
        self.x= x
        self.y = y
        self.image = pygame.image.load('./Art/BigBad_Down.png')
        # self.path = [x, end]  # This will define where our enemy starts and finishes their path.
        self.walk_count = 0
        self.vel = 1
        self.rect = self.image.get_rect()
        self.direction = "UP"

    def move(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.x - self.x, player.y - self.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.x += dx * self.vel
        self.y += dy * self.vel
        self.damage(player, dx, dy)

        self.walkCount = 0
        if dx >= 0 and dy < 0:
            if abs(dx) > abs(dy):
                if self.direction != "RIGHT" or self.walk_count + 1 >= 27:
                    self.walk_count = 0
                self.direction = "RIGHT"
                self.image = pygame.image.load(self.walk_right[self.walk_count//9])
                self.walk_count += 1
            else:
                if self.direction != "UP" or self.walk_count + 1 >= 27:
                    self.walk_count = 0
                self.direction = "UP"
                self.image = pygame.image.load(self.walk_up[self.walk_count//9])
                self.walk_count += 1
        elif dx >= 0 and dy > 0:
            if abs(dx) > abs(dy):
                if self.direction != "RIGHT" or self.walk_count + 1 >= 27:
                    self.walk_count = 0
                self.direction = "RIGHT"
                self.image = pygame.image.load(self.walk_right[self.walk_count//9])
                self.walk_count += 1
            else:
                if self.direction != "DOWN" or self.walk_count + 1 >= 27:
                    self.walk_count = 0
                self.direction = "DOWN"
                self.image = pygame.image.load(self.walk_down[self.walk_count//9])
                self.walk_count += 1
        elif dx <= 0 and dy < 0:
            if abs(dx) > abs(dy):
                if self.direction != "LEFT" or self.walk_count + 1 >= 27:
                    self.walk_count = 0
                self.direction = "LEFT"
                self.image = pygame.image.load(self.walk_left[self.walk_count//9])
                self.walk_count += 1
            else:
                if self.direction != "UP" or self.walk_count + 1 >= 27:
                    self.walk_count = 0
                self.direction = "UP"
                self.image = pygame.image.load(self.walk_up[self.walk_count//9])
                self.walk_count += 1
        elif dx <= 0 and dy > 0:
            if abs(dx) > abs(dy):
                if self.direction != "LEFT" or self.walk_count + 1 >= 27:
                    self.walk_count = 0
                self.direction = "LEFT"
                self.image = pygame.image.load(self.walk_left[self.walk_count//9])
                self.walk_count += 1
            else:
                if self.direction != "DOWN" or self.walk_count + 1 >= 27:
                    self.walk_count = 0
                self.direction = "DOWN"
                self.image = pygame.image.load(self.walk_down[self.walk_count//9])
                self.walk_count += 1
            
        gameDisplay.blit(self.image, (self.x, self.y))


        self.rect.topleft = (self.x, self.y)

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

class Projectile(object):
    def __init__(self, direction, player):
        super()
        self.x = player.x
        self.y = player.y
        self.direction = direction
        self.speed = 6
        self.rect = pygame.rect.Rect(self.x, self.y, 20, 20)

    def move(self):
        if self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed
        elif self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed
        #gameDisplay.blit()
        self.rect.topleft = (self.x, self.y)
        pygame.draw.rect(gameDisplay, black, self.rect)

 
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

    
   
    wall_box = wall_boxes()
    x = (display_width * 0.45)
    y = (display_height * 0.5)
    x_change = 0
    y_change = 0

    exit_game = False
    
    player = Player()
    
    obstacle_list = [Obstacle(0),Obstacle(1),Obstacle(2),Obstacle(3),Obstacle(4),Obstacle(5)]
    
    
    projectiles = []

    bigbad = Enemy(random.randint(tile_size,display_width-tile_size-character_size),random.randint(tile_size*2,display_height-(tile_size*2)-character_size))
    
    while not exit_game:
        for event in pygame.event.get():  # event handling loop (inputs and shit)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if not player.can_attack:
            player.attack_clock += 1
            if player.attack_clock >= 60:
                player.attack_clock = 0
                player.can_attack = True
        else:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_UP]:
                projectiles.append(Projectile("UP", player))
                player.can_attack = False
            elif pressed_keys[pygame.K_DOWN]:
                projectiles.append(Projectile("DOWN", player))
                player.can_attack = False
            elif pressed_keys[pygame.K_LEFT]:
                projectiles.append(Projectile("LEFT", player))
                player.can_attack = False
            elif pressed_keys[pygame.K_RIGHT]:
                projectiles.append(Projectile("RIGHT", player))
                player.can_attack = False

        gameDisplay.fill(white) # must order this and next line because otherwise fill would fill over the car
        ### Draw scenery then enemies here ###
        
        room()


        bigbad.move(player) 
        wall_boxes()
        player.move()
        
        for x in projectiles:
            x.move()
            
        for index in range(0,6):
            obstacle_list[index].draw()
            collision(player,obstacle_list[index])
            collision(bigbad,obstacle_list[index])

        #pygame.draw.rect(gameDisplay,green,player.rect)
        #pygame.draw.rect(gameDisplay,red,obstacle.rect)

        if pygame.Rect.collidelist(player.rect,wall_box) != -1 and player.direction == "LEFT":
            player.x = 32 
        if pygame.Rect.collidelist(player.rect,wall_box) != -1 and player.direction == "RIGHT":
            player.x = (display_width - (32+player.image_width ))
        if pygame.Rect.collidelist(player.rect,wall_box) != -1  and player.direction == "UP":
            player.y = 48
        if pygame.Rect.collidelist(player.rect,wall_box) != -1  and player.direction == "DOWN":
            player.y = display_height - (64 + player.image_height)

        if not player.vulnerable:
            player.vulnerability_clock += 1
            if player.vulnerability_clock >= 180:
                player.vulnerability_clock = 0
                player.vulnerable = True

        


        
        ### Draw scenery then enemies here ###
        #player(x, y)

        pygame.display.update() #also can use pygame.display.flip(), update allows a parameter to specifically update
        clock.tick(120) #sets frames per second


game_loop()
pygame.quit() #stop pygame from running
quit() #end program




############################
#TODO: Solidify collision with objects and walls------DONE
#TODO: Enemies walk towards player------DONE
#TODO: Enemy Sprites and animation
#TODO: Enemy damage player when collision boxes touch-----DONE
#TODO: Create system for placing multiple objects around the room