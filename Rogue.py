import os
import pygame
import random
from pygame import sprite
from pygame import image
from pygame import mixer
from pygame.sprite import collide_mask, collide_rect, collide_rect_ratio
import math



os.getcwd()
pygame.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100,16,2,512)



pygame.init()

# must be an even multiple of 32
display_width = 640
display_height = 640
global game_beat
game_beat = False
global high_score
high_score = 0
global score
score = 0
global points
points = 0

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# levels are in tuples (# of enemies at a time, enemy health, # of waves, boolean bossfight)
levels = [(2, 16, 1, False), (2, 16, 3, False), (4, 16, 2, False), (5, 16, 3, False), (5, 20, 2, False), (3, 20, 1, True), (5, 30, 3, False), (6, 25, 2, False), (6, 30, 3, False), (7, 30, 3, False), (0, 60, 0, True)]
global current_level
current_level = 0#CHAnGE BACK TO 0 

tile_size = 32 # pixel size per tile
character_size = 32

player_speed = 3 # number of pixels player moves per action

obstacle_grid = [[0 for i in range(int(display_height/32-2))] for j in range(int(display_width/32-4))]

global projectile_damage
projectile_damage = 2
global projectile_speed
projectile_speed = 6
global fire_rate
fire_rate = 50


enemies = []
dead_enemies = []
projectiles = []
obstacle_list = []

gameDisplay = pygame.display.set_mode((display_width, display_height)) #set up frame for game
pygame.display.set_caption('Rogue-Like') #change title on the game window
clock = pygame.time.Clock() #pygame clock based off frames apparently  



class Obstacle(pygame.sprite.Sprite):#creates a class of obstacles for loading and spawning

    obstacle_list = ['./Art/barrel.png','./Art/table_no_cloth.png','./Art/table_cloth.png','./Art/potted_plant.png'
    ,'./Art/lab_bench_no_chem.png','./Art/lab_bench_chem.png','./Art/old_server.png']# list of sprites to be loaded in as obstacles

    def __init__(self, index, row, col):
        pygame.sprite.Sprite.__init__(self)
        super()
        self.image = pygame.image.load(self.obstacle_list[index])#can be used to blit later

        self.x = col*32 + 32
        self.y = row*32 + 64
        self.width  = self.image.get_width()
        self.height =  self.image.get_height()#if ~8 pixels are subtracted can be used to make depth but then have to figure out redraw so you dont slid under other sprites
        self.rect = self.image.get_rect()# creates a rectangle and may not be strictly necessary if using collide_mask
        self.rect.topleft = (self.x,self.y)
        self.rect.inflate(-10,-10)

        obstacle_grid[row][col] = 1
        for i in range(0, int(self.height/32)):
            if i >= len(obstacle_grid):
                break
            for j in range(0, 0+int(self.width/32)):
                if j >= len(obstacle_grid[i]):
                    break
                obstacle_grid[i+row][j+col] = 1

        self.draw()
        
    def draw(self):
        gameDisplay.blit(self.image, (self.x, self.y,))#this is currently bliting barrel probably a better way to do this

class Building(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.height = image.get_height()
        self.width = image.get_width()
    
    def draw(self):
        gameDisplay.blit(self.image, (self.x, self.y,))

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
    
def collision(character, obstacle):
    if collide_rect (character,obstacle) and abs(character.rect.left - obstacle.rect.right) <= character.speed:#collision_mask checks for sprite mask collision which goes beyond rectangles i think
            character.x = obstacle.rect.right #sets player speed to zero if collides from the left and repeat for other ifs
            return True
    if collide_rect (character,obstacle) and abs(character.rect.right - obstacle.rect.left) <= character.speed:
            character.x = obstacle.rect.left - (character.width)
            return True
    if collide_rect (character,obstacle) and abs(character.rect.top - obstacle.rect.bottom) <= character.speed:
            character.y = obstacle.rect.bottom
            return True
    if collide_rect (character,obstacle) and abs(character.rect.bottom - obstacle.rect.top) <= character.speed:
            character.y = obstacle.rect.top - (character.height)
            return True
   
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
        self.speed = 3
        self.direction = "UP"
        self.walk_count = 0
        self.health = 6
        self.vulnerable = True
        self.can_attack = True
        self.vulnerability_clock = 0
        self.attack_clock = 0
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a]:
            if self.speed == 0 and self.direction != "LEFT": #makes it so you can move right away from obstacle applies to all of the things 
                self.speed = 3
            if self.direction != "LEFT" or self.walk_count + 1 >= 27:
                self.walk_count = 0
            self.direction = "LEFT"
            self.x -= self.speed
            self.image = pygame.image.load(self.walk_left[self.walk_count//9])
            self.walk_count += 1
        elif pressed_keys[pygame.K_d]:
            if self.speed == 0 and self.direction != "RIGHT":
                self.speed = 3
            if self.direction != "RIGHT" or self.walk_count + 1 >= 27:
                self.walk_count = 0
            self.direction = "RIGHT"
            self.x += self.speed
            self.image = pygame.image.load(self.walk_right[self.walk_count//9])
            self.walk_count += 1
        elif pressed_keys[pygame.K_s]:
            if self.speed == 0 and self.direction != "DOWN":
                self.speed = 3
            if self.direction != "DOWN" or self.walk_count + 1 >= 27:
                self.walk_count = 0
            self.direction = "DOWN"
            self.y += self.speed
            self.image = pygame.image.load(self.walk_down[self.walk_count//9])
            self.walk_count += 1
        elif pressed_keys[pygame.K_w]:
            if self.speed == 0 and self.direction != "UP":
                self.speed = 3
            if self.direction != "UP" or self.walk_count + 1 >= 27:
                self.walk_count = 0
            self.direction = "UP"
            self.y -= self.speed
            self.image = pygame.image.load(self.walk_up[self.walk_count//9])
            self.walk_count += 1
        else:
            self.walk_count = 0
            if self.direction == "UP":
                self.image = pygame.image.load(self.walk_up[0])
            elif self.direction == "DOWN":
                self.image = pygame.image.load(self.walk_down[0])
            elif self.direction == "RIGHT":
                self.image = pygame.image.load(self.walk_right[0])
            elif self.direction == "LEFT":
                self.image = pygame.image.load(self.walk_left[0])

        self.draw()
        self.rect.topleft = (self.x, self.y)
        #pygame.draw.rect(gameDisplay, black, self.rect)

    def draw(self):
        gameDisplay.blit(self.image, (self.x, self.y))
        
    def update(self):
        pass

    def attack(self):
        pass

player = Player()


class Enemy(object):
    normal_up = ["./Art/BigBad_Up.png", "./Art/BigBad_Up_Left.png", "./Art/BigBad_Up_Right.png"]
    normal_right = ["./Art/BigBad_Right.png", "./Art/BigBad_Right_Left.png", "./Art/BigBad_Right_Right.png"]
    normal_left = ["./Art/BigBad_Left.png", "./Art/BigBad_Left_Left.png", "./Art/BigBad_Left_Right.png"]
    normal_down = ["./Art/BigBad_Down.png", "./Art/BigBad_Down_Left.png", "./Art/BigBad_Down_Right.png"]
    dead_normal = ["./Art/BigBad_Dead.png"]

    boss_up = ["./Art/Boss_Up.png", "./Art/Boss_Up_Left.png", "./Art/Boss_Up_Right.png"]
    boss_right = ["./Art/Boss_Right.png", "./Art/Boss_Right_Left.png", "./Art/Boss_Right_Right.png"]
    boss_left = ["./Art/Boss_Left.png", "./Art/Boss_Left_Left.png", "./Art/Boss_Left_Right.png"]
    boss_down = ["./Art/Boss_Down.png", "./Art/Boss_Down_Left.png", "./Art/Boss_Down_Right.png"]
    dead_boss = ["./Art/dead_boss.png"]

    walk_up = []
    walk_right = []
    walk_left = []
    walk_down = []
    dead_zombie = []

    def __init__(self, x, y, health, speed, boss):
        self.x= x
        self.y = y
        self.image = pygame.image.load('./Art/BigBad_Down.png')
        self.walk_count = 0
        self.speed = speed
        self.rect = self.image.get_rect()
        self.direction = "UP"
        self.health = health
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.collision_side = "NONE"
        self.dead = False
        self.boss = boss
        if boss:
            self.walk_up = self.boss_up
            self.walk_right = self.boss_right
            self.walk_left = self.boss_left
            self.walk_down = self.boss_down
            self.dead_zombie = self.dead_boss
        else:
            self.walk_up = self.normal_up
            self.walk_right = self.normal_right
            self.walk_left = self.normal_left
            self.walk_down = self.normal_down
            self.dead_zombie = self.dead_normal


    def move(self, player,boss):
        if not self.dead:
            # Find direction vector (dx, dy) between enemy and player.
            dx, dy = player.x - self.x, player.y - self.y
            dist = math.hypot(dx, dy)
            dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            self.x += dx * self.speed
            self.y += dy * self.speed
            if self.damage(player, dx, dy):
                return True

            self.walkCount = 0
            if self.collision_side != "NONE":
                if self.collision_side == "UP":
                    if dx >= 0:
                        self.x += self.speed
                    else:
                        self.x -= self.speed
                elif self.collision_side == "DOWN":
                    if dx >= 0:
                        self.x += self.speed
                    else:
                        self.x -= self.speed
                elif self.collision_side == "LEFT":
                    if dy >= 0:
                        self.y += self.speed
                    else:
                        self.y -= self.speed
                elif self.collision_side == "RIGHT":
                    if dy >= 0:
                        self.y += self.speed
                    else:
                        self.y -= self.speed
            else:
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
        self.draw()

        self.rect.topleft = (self.x, self.y)
        return False

    def normal_move(self, dx, dy):
        self.walkCount = 0
        self.x += dx * self.vel
        self.y += dy * self.vel
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

    def damage(self, player, dx, dy):
        if collision(self, player) and player.vulnerable:
            pygame.mixer.Sound("./Sound/hit-3.wav").play()
            player.health -= 1
            #player.x += dx * 15
            #player.y += dy * 15
            player.vulnerable = False
            if player.health <= 0:
                pygame.mixer.music.pause()
                pygame.mixer.Sound("./Sound/lose-7.wav").play()
                pygame.time.delay(2000)
                global score
                global high_score
                if score > high_score:
                    high_score = score
                score = 0
                return True
        return False

    def draw(self):
        if self.dead:
            self.image = pygame.image.load(self.dead_zombie[0])
            self.walk_count += 1
            if self.walk_count >= 60:
                return True
        gameDisplay.blit(self.image, (self.x, self.y))
        return False


class Projectile(object):
    def __init__(self, direction, player):
        super()
        self.damage = projectile_damage
        self.x = player.x
        self.y = player.y
        self.direction = direction
        self.speed = projectile_speed
        if self.direction == "UP":
            self.image = pygame.image.load("./Art/bullet_up.png")
        if self.direction == "DOWN":
            self.image = pygame.image.load("./Art/bullet_down.png")
        if self.direction == "LEFT":
            self.image = pygame.image.load("./Art/bullet_left.png")
        if self.direction == "RIGHT":
            self.image = pygame.image.load("./Art/bullet_right.png")
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

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
        self.draw()

    def draw(self):
        gameDisplay.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(gameDisplay, black, self.rect)
 
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

def draw_things():
    room()
    for obstacle in obstacle_list:
        obstacle.draw()
    for dead_enemy in dead_enemies:
        dead_enemy.draw()
    for enemy in enemies:
        enemy.draw()
    for projectile in projectiles:
        projectile.draw()
    player.draw()
    for i in range(0, player.health):
        gameDisplay.blit(pygame.image.load("./Art/heart.png"), (i*20 + 10, 5))
    print_level()

def print_score(highscore):
    global high_score
    global score
    if highscore:
        font = pygame.font.SysFont(None, 25)
        text = font.render("High Score: " + str(high_score), True, black)
        gameDisplay.blit(text, (display_width-128, 10))
    else:
        font = pygame.font.SysFont(None, 25)
        text = font.render("Score: " + str(score), True, black)
        gameDisplay.blit(text, (display_width-128, 10))

def print_level():
    global current_level
    font = pygame.font.SysFont(None, 25)
    text = font.render("Level: " + str(current_level+1), True, black)
    gameDisplay.blit(text, (display_width/2 - 20, 10))

def print_points():
    global points
    font = pygame.font.SysFont(None, 25)
    text = font.render("Points: " + str(points), True, blue)
    gameDisplay.blit(text, (display_width-128, 10))


def increment_score():
    global score
    score += 1
    global points
    if score % 2 == 0:
        points += 1

def open_shop():
    image = pygame.image.load('./Art/shop.png')
    while True:
        draw_things()
        print_points()
        gameDisplay.blit(image, (0, 0))
        gameDisplay.blit(pygame.image.load('./Art/Pause_menu.png'), (0, 0))
        pygame.display.update()
        for event in pygame.event.get():  # event handling loop (inputs and shit)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return -1
                if event.key == pygame.K_p:
                    return 0

                global points
                if event.key == pygame.K_g:
                    #increase damage
                    global projectile_damage
                    if points >= 5 and projectile_damage < 10:
                        projectile_damage += 1
                        points -= 5
                        
                if event.key == pygame.K_h:
                    #increase fire rate
                    global fire_rate
                    if points >= 5 and fire_rate > 10:
                        fire_rate -= 5
                        points -= 5


def pause_game():
    pygame.mixer.music.set_volume(.2) 
    image = pygame.image.load('./Art/Pause_menu.png')
    gameDisplay.blit(image, (0, 0))
    pygame.display.update()
    while True:
        draw_things()
        print_points()
        gameDisplay.blit(image, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():  # event handling loop (inputs and shit)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.set_volume(1)
                    return
                if event.key == pygame.K_p:
                    if open_shop() == -1:
                        pygame.mixer.music.set_volume(1)
                        return

def spawn_enemy(health, speed, boss):
    random_x = random.randint(tile_size,display_width-tile_size-character_size)
    random_y = random.randint(tile_size*2,display_height-(tile_size*2)-character_size)
    while random_x - player.x > -128 and random_x - player.x < 128 and random_y - player.y > -128 and random_y - player.y < 128:
        random_x = random.randint(tile_size,display_width-tile_size-character_size)
        random_y = random.randint(tile_size*2,display_height-(tile_size*2)-character_size)
    enemies.append(Enemy(random_x, random_y, health, speed, boss))

def game_loop(level):

    shoot_obstacle = pygame.mixer.Sound('./Sound/footstep1.wav')
    hit_enemy = pygame.mixer.Sound("./Sound/hit-1.wav")
    enemy_die = pygame.mixer.Sound("./Sound/explode-1.wav")
    shoot = pygame.mixer.Sound("./Sound/laser-7.wav")

    wall_box = wall_boxes()

    exit_game = False
    
    #player = Player()

    
            
    #obstacle1 = Obstacle(0)#makes Obstacle easier to work with
    #obstacle2 = Obstacle(1)
    if level == 0:
        obstacle_count = 0
        for row in range(0, len(obstacle_grid)-1):
            for col in range(0, len(obstacle_grid[0])-1):
                if obstacle_count < 5:
                    if obstacle_grid[row][col] != 1 and random.randint(0,50) == 1:
                        obstacle_list.append(Obstacle(random.randrange(0, 6), row, col))
                        obstacle_count += 1
        
    enemy_health = levels[level][1]
    for index in range(0, levels[level][0]):
        spawn_enemy(enemy_health, 1, False)
    if levels[level][3]:
        spawn_enemy(enemy_health*5, 2.5, True)
    zombie_count = (levels[level][2]-1)*levels[level][0]
    while not exit_game:
        # spawn new enemy if less than level wave count
        if zombie_count > 0 and len(enemies) < levels[level][0]:
            spawn_enemy(enemy_health, 1, False)
            zombie_count -= 1
            

        if zombie_count <= 0 and len(enemies) <= 0:
            return True

        for event in pygame.event.get():  # event handling loop (inputs and shit)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_game()

        # handle player attack and cooldown
        global fire_rate
        if not player.can_attack:
            player.attack_clock += 1
            if player.attack_clock >= fire_rate:
                player.attack_clock = 0
                player.can_attack = True
        else:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_UP]:
                shoot.play()
                projectiles.append(Projectile("UP", player))
                player.can_attack = False
            elif pressed_keys[pygame.K_DOWN]:
                shoot.play()
                projectiles.append(Projectile("DOWN", player))
                player.can_attack = False
            elif pressed_keys[pygame.K_LEFT]:
                shoot.play()
                projectiles.append(Projectile("LEFT", player))
                player.can_attack = False
            elif pressed_keys[pygame.K_RIGHT]:
                shoot.play()
                projectiles.append(Projectile("RIGHT", player))
                player.can_attack = False

        gameDisplay.fill(white) # must order this and next line because otherwise fill would fill over the car
        ### Draw scenery then enemies here ###
        
        room()

        dead_enemies_length = len(dead_enemies)
        dead_enemies_index = 0
        while dead_enemies_index < dead_enemies_length:
            dead_enemy = dead_enemies[dead_enemies_index]
            if dead_enemy.draw():
                dead_enemies.remove(dead_enemy)
                dead_enemies_length -= 1
                dead_enemies_index -= 1
            dead_enemies_index += 1

        # move enemies towards player and blit

        for obstacle in obstacle_list:
            obstacle.draw()
            collision(player,obstacle)
            for enemy in enemies:    
                collision(enemy,obstacle)
        
        player.move()
        
        for enemy in enemies:
            if enemy.move(player,False):
                return False
        
        wall_boxes()
        


        # iterate through projectile list: moving and checking for collision with objects and enemies
        projectiles_length = len(projectiles)
        projectile_index = 0
        while projectile_index < projectiles_length:
            projectile = projectiles[projectile_index]
            projectile.move()
            projectile_removed = False
            enemy_index = 0
            enemies_length = len(enemies)
            while enemy_index < enemies_length:
                enemy = enemies[enemy_index]
                if collide_rect(projectile, enemy):
                    enemy.health -= projectile.damage
                    projectiles.remove(projectile)
                    projectiles_length -= 1
                    projectile_index -= 1
                    hit_enemy.play() 
                    projectile_removed = True
                    if enemy.health <= 0:
                        enemy_die.play() 
                        enemy.dead = True
                        dead_enemies.append(enemy)
                        if enemy.boss:
                            for i in range(0,5):
                                increment_score()
                        else:
                            increment_score()
                        enemies.remove(enemy)
                    break
                enemy_index += 1
            if not projectile_removed:
                for obstacle in obstacle_list:
                    if collide_rect(projectile, obstacle):
                        projectiles.remove(projectile)
                        projectiles_length -= 1
                        projectile_index -= 1
                        projectile_removed = True
                        break
            if not projectile_removed:
                if pygame.Rect.collidelist(projectile.rect,wall_box) != -1:
                    projectiles.remove(projectile)
                    projectiles_length -= 1
                    projectile_index -= 1
            projectile_index += 1

        print_score(False)
        print_level()
            
        # player and enemy collision with obstacles

        for enemy1 in enemies:
            for enemy2 in enemies:
                if enemy1 != enemy2:
                    collision(enemy1, enemy2)
            

        #pygame.draw.rect(gameDisplay,green,player.rect)
        #pygame.draw.rect(gameDisplay,red,obstacle.rect)

        if pygame.Rect.collidelist(player.rect,wall_box) != -1 and player.direction == "LEFT":
            player.x = 32 
        elif pygame.Rect.collidelist(player.rect,wall_box) != -1 and player.direction == "RIGHT":
            player.x = (display_width - (32+player.width ))
        elif pygame.Rect.collidelist(player.rect,wall_box) != -1  and player.direction == "UP":
            player.y = 48
        elif pygame.Rect.collidelist(player.rect,wall_box) != -1  and player.direction == "DOWN":
            player.y = display_height - (64 + player.height)

        for i in range(0, player.health):
            gameDisplay.blit(pygame.image.load("./Art/heart.png"), (i*20 + 10, 5))
        
        ### Draw scenery then enemies here ###

        if not player.vulnerable:
            player.vulnerability_clock += 1
            if player.vulnerability_clock >= 180:
                player.vulnerability_clock = 0
                player.vulnerable = True

        pygame.display.update() #also can use pygame.display.flip(), update allows a parameter to specifically update
        clock.tick(180) #sets frames per second

def credits():
    pygame.mixer.music.load('./Sound/Three Red Hearts.wav')
    pygame.mixer.music.play(-1)
    texts = ["./Art/Credits/title.png", "./Art/Credits/andy_fiore.png", "./Art/Credits/scott_creation.png", "./Art/Credits/matt_shiber.png","./Art/Credits/silveira_neto.png", "./Art/Credits/nicolae_berbece.png", "./Art/Credits/scott_sullivan.png", "./Art/Credits/evan_miller.png", "./Art/Credits/abstraction.png"]
    player.x = 400
    player.y = 400
    timer = 0
    while True:
        if timer//120 >= len(texts):
            pygame.mixer.music.load("./Sound/Sanctuary.wav")
            pygame.mixer.music.play(-1)
            return
        image = pygame.image.load(texts[timer//120])
        for event in pygame.event.get():  # event handling loop (inputs and shit)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.load("./Sound/Sanctuary.wav")
                pygame.mixer.music.play(-1)
                if event.key == pygame.K_ESCAPE:
                    return

        gameDisplay.fill(black)
        gameDisplay.blit(image, (0, 0))
        gameDisplay.blit(pygame.image.load("./Art/curtain.png"), (0, 0))
        pygame.display.update()
        timer += 1
        clock.tick(180)

        

        

def main_menu():
    print(game_beat)
    pygame.mixer.music.load('./Sound/Sanctuary.wav')
    pygame.mixer.music.play(-1)
    player.health = 3
    enemies.clear()
    obstacle_list.clear()
    player.x = 400
    player.y = 400
    while True:
        for event in pygame.event.get():  # event handling loop (inputs and shit)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    projectiles.append(Projectile("UP", player))
                    player.can_attack = False
                elif event.key == pygame.K_DOWN:
                    projectiles.append(Projectile("DOWN", player))
                    player.can_attack = False
                elif event.key == pygame.K_LEFT:
                    projectiles.append(Projectile("LEFT", player))
                    player.can_attack = False
                elif event.key == pygame.K_RIGHT:
                    projectiles.append(Projectile("RIGHT", player))
                    player.can_attack = False
        global fire_rate
        if not player.can_attack:
            player.attack_clock += 1
            if player.attack_clock >= fire_rate:
                player.attack_clock = 0
                player.can_attack = True
        
        



        building_top = Building(pygame.image.load("./Art/building_top.png"), 160, 192)
        building_left = Building(pygame.image.load("./Art/building_left.png"), 160, (192 + building_top.height))
        right_image = pygame.image.load("./Art/building_right.png")
        building_right = Building(right_image, (160 + building_top.width - right_image.get_width()), (192 + building_top.height))

        game_zone = pygame.Rect((160+building_left.width), (190+building_top.height), building_left.width, (building_left.height+2))

        hall_top = Building(pygame.image.load("./Art/hall_top.png"), 400, 232)
        hall_left = Building(pygame.image.load("./Art/hall_left.png"), 400, (232 + hall_top.height))
        right_image = pygame.image.load("./Art/hall_right.png")
        hall_right = Building(right_image, (400 + hall_top.width - right_image.get_width()), (232 + hall_top.height))

        score_zone = pygame.Rect((398+hall_left.width), (230+hall_top.height), hall_left.width, (hall_left.height + 2))

        gameDisplay.blit(pygame.image.load("./Art/title_screen.png"), (0, 0))

        pygame.draw.rect(gameDisplay,black,score_zone)
        if score_zone.colliderect(player.rect):
            credits()
        pygame.draw.rect(gameDisplay,black,game_zone)

        building_top.draw()
        building_left.draw()
        building_right.draw()

        hall_top.draw()
        hall_left.draw()
        hall_right.draw()

        player.move()
        gameDisplay.blit(pygame.image.load("./Art/title.png"), (0, 0))
        print_score(True)
        collision(player, building_top)
        collision(player, building_left)
        collision(player, building_right)
        collision(player, hall_top)
        collision(player, hall_left)
        collision(player, hall_right)
        
            
        if game_zone.colliderect(player.rect):
            pygame.mixer.music.load('./Sound/Box Jump.wav')
            pygame.mixer.music.play(-1)
            return True


        projectiles_length = len(projectiles)
        projectile_index = 0
        while projectile_index < projectiles_length:
            projectile = projectiles[projectile_index]
            projectile.move()
            if projectile.y < 0 and projectile.direction == "UP":
                projectiles.remove(projectile)
                projectile_index -= 1
                projectiles_length -= 1
            elif projectile.y + projectile.height > display_height and projectile.direction == "DOWN":
                projectiles.remove(projectile)
                projectile_index -= 1
                projectiles_length -= 1
            elif projectile.x < 0 and projectile.direction == "LEFT":
                projectiles.remove(projectile)
                projectile_index -= 1
                projectiles_length -= 1
            elif projectile.x + projectile.width > display_width and projectile.direction == "RIGHT":
                projectiles.remove(projectile)
                projectile_index -= 1
                projectiles_length -= 1
            projectile_index += 1

        pygame.display.update()
        clock.tick(180)


while True:
    if main_menu():
        while game_loop(current_level) and current_level < len(levels)-1:
            current_level += 1
            if game_beat:
                i = random.randrange(0, 7)
                if i != 1:
                    levels.append((random.randrange(7, 12), random.randrange(7, 12)*5, random.randrange(1, 5), random.randrange(0, 7) == 6))
                else:
                    levels.append((0, random.randrange(8, 20)*10, 0, True))

            if current_level >= len(levels)-1 and player.health > 0 and not game_beat:
                pygame.mixer.music.stop()
                pygame.mixer.Sound('./Sound/win-8.wav').play()
                pygame.time.delay(2000)
                pygame.mixer.music.load("./Sound/Three Red Hearts.wav")
                credits()
                high_score = score
                score = 0
                game_beat = True
        if current_level >= len(levels)-1:
            high_score = score
            score = 0
            game_beat = True
        current_level = 0
#game_loop()
pygame.quit() #stop pygame from running
quit() #end program




############################
#TODO: Solidify collision with objects and walls------DONE
#TODO: Enemies walk towards player------DONE
#TODO: Enemy Sprites and animation-------DONE
#TODO: Enemy damage player when collision boxes touch-----DONE
#TODO: Create system for placing multiple objects around the room
#TODO: Make is so when player stops moving resets animation to both legs down
