import pygame
from pygame import Rect, rect

pygame.init()

window = pygame.display.set_mode((300, 300)) #creates a window dimensions of 300px by 300px

rect1 = pygame.Rect(*window.get_rect().center,0,0).inflate(50,80) #creates a static rectangle in the center of the window
rect2 = pygame.Rect(0,0,75,75)#creates a rectangle to be reassigned later to center on the mouse and move around it

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False

    rect2.center = pygame.mouse.get_pos()#centers rect2 on the mouse coords and will follow as it moves
    collide = rect1.colliderect(rect2)#makes a bool that is true when the two rectangles collide
    color = (255,0,0) if collide else (255,255,255)#changes the color of rect1 depending on whether collide is true
            #changes from white to red if collide is true

    window.fill(0)
    pygame.draw.rect(window, color, rect1)#draws rect1
    pygame.draw.rect(window, (0,255,0), rect2, 6,1)#draws rect2 just the edges around the mouse
    pygame.display.flip()

    if collide:#creates an event wheresomething changes when collide is true
       
        pygame.mouse.set_pos(0,0)#moves mouse coords to bottom right when collide is true

pygame.quit()
exit()