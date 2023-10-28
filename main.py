import pygame
import numpy as np
import math

pygame.init()

WIDTH = 1000
HEIGHT = 500
fps = 60
timer = pygame.time.Clock()
v = 1
a = 1

screen = pygame.display.set_mode([WIDTH, HEIGHT])

run = True

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


while run:

    # Background
    screen.fill('white')
    timer.tick(fps) # While loop repeats 60 times per second

    # Fetch mouse position 
    mouse_pos = pygame.mouse.get_pos()
    
    # Draw grandma
    grandma = (WIDTH/2, HEIGHT)
    pygame.draw.circle(screen, 'gray', grandma , 50)

    # Oscilate the target position
    target = (mouse_pos[0], mouse_pos[1])
    v += a
    d = 1
    upper = 20
    lower = -20
    
    # Change velocity if we hit upper or lower bound 
    if v > upper or v < lower:
        a *= -1

    # If on right side of screen, oscilate along y=-x line
    if mouse_pos[0] > WIDTH/2:
        d = -1
    
    target = (mouse_pos[0]+v, mouse_pos[1]+v*d)
    
    pygame.draw.circle(screen, 'red', target, 10)

    # Draw the beizer curve between two mouse cursor and grandma
    warp = (WIDTH/2, HEIGHT/2)
    pts = [grandma, warp, target]
    bezier()

    # Allow for the user to quit out of game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
