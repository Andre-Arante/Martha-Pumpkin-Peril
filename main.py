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

pts = [(50, 50), (200, 600), (800, 200)]

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

    # While loop repeats 60 times per second
    timer.tick(fps)

    # Fetch mouse position 
    mouse_pos = pygame.mouse.get_pos()

    # Draw a target at mouse position
    pygame.draw.circle(screen, 'red', mouse_pos, 10)

    # Draw grandma
    grandma = (WIDTH/2, HEIGHT)
    pygame.draw.circle(screen, 'gray', grandma , 50)

    warp = (WIDTH/2, HEIGHT/2)

    # Draw the beizer curve between two mouse cursor and grandma
    pts = [grandma, warp, (mouse_pos[0], mouse_pos[1])]
    bezier()

    # Allow for the user to quit out of game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
