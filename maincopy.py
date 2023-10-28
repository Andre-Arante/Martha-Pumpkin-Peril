import pygame
import numpy as np
import math

pygame.init()

WIDTH = 1000
HEIGHT = 500
fps = 60
timer = pygame.time.Clock()


screen = pygame.display.set_mode([WIDTH, HEIGHT])

run = True

moving_rect = pygame.Rect(350,350,100,100)
x_speed, y_speed = 5,4

other_rect = pygame.Rect(300,600,200,100)
other_speed = 2

#Bezier
def bezier():
    N = len(pts)
    n = N-1
    for t in np.arange(0, 1, 0.01):
        z = np.zeros(2)
        for i in range(N):
            z += np.dot((math.factorial(n)/(math.factorial(i)*math.factorial(n-i)))
                        *((1-t)**(n-i))*(t**i),pts[i])

        pygame.draw.circle(screen, (255, 0, 0), z.astype(int), 3)

def oscilate(upper, lower, x, v):
    if x > upper: 
        v *= -1
    if x < lower:
        v *= -1
    return x + v


while run:

    # Background
    screen.fill('white')
    timer.tick(fps) # While loop repeats 60 times per second

    # Fetch mouse position 
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, 'red', mouse_pos, 10)

    # Draw grandma
    grandma = (WIDTH/2, HEIGHT)
    pygame.draw.circle(screen, 'gray', grandma , 50)

    # Oscilate the target position
    target = (mouse_pos[0], mouse_pos[1])
    var = 15
    target = (oscilate(target[0]+var, target[0]-var, target[0], 1), oscilate(target[1]+var, target[1]-var, target[1], 1)) # oscilate y

    # Draw the beizer curve between two mouse cursor and grandma
    warp = (WIDTH/2, HEIGHT/2)
    pts = [grandma, warp, target]
    bezier()

    # Allow for the user to quit out of game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.draw.rect(screen, (255,255,255), moving_rect)
    pygame.draw.rect(screen, (255,255,255), moving_rect)
    
    pygame.display.flip()



pygame.quit()
