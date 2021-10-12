import pygame

display_width = 640
display_height = 640

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height)) #set up frame for game
pygame.display.set_caption('Rogue-Like') #change title on the game window
clock = pygame.time.Clock() #pygame clock based off frames apparently

playerImg = pygame.image.load('baldGuy.png') #load load player image

def player(x, y):
    gameDisplay.blit(playerImg, (x,y)) #draw carImg onto background at (x,y) coordinates


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
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_UP:
                    y_change = -5
                if event.key == pygame.K_DOWN:
                    y_change = 5

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
        

        ### Draw scenery then enemies here ###
        player(x, y)

        pygame.display.update() #also can use pygame.display.flip(), update allows a parameter to specifically update
        clock.tick(60) #sets frames per second


game_loop()
pygame.quit() #stop pygame from running
quit() #end program