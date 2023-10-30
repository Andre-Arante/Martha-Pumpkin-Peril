# https://github.com/Andre-Arante/Martha-s-Pumpkin  

import pygame


from enemy import *
from util import beizer

pygame.init()


# Main Gameplay Screen
def gameplay():

    # Initial Setup Variables
    WIDTH = 1000
    HEIGHT = 500
    fps = 60
    timer = pygame.time.Clock()
    health = 10

    # Velociaty and acceleration for the oscilation of the target
    v = 1
    a = 1

    # Tracks number of frames since program initialization
    counter = 0

    # Stores enemy data
    enemies = []
    spawnRate = 100

    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    run = True

    pumpkinSpin = [pygame.image.load('./assets/pumpkin.png')]
    screen.blit(pumpkinSpin, (0, 0))

    while run:

        # Background
        screen.fill('white')
        timer.tick(fps) # While loop repeats 60 times per second

        # Fetch mouse position 
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(pumpkinSpin, mouse_pos)
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
        bezier(pts, screen)


        # Spawn enemies at a random position at the top
        
        if(counter % spawnRate == 0):
            new = Enemy(screen) 
            enemies.append(new)

        for e in enemies:
            e.move()
            e.draw()

            # Check if enemy has passed 

            health = e.update_health(HEIGHT, health)
            if health <= 0:
                pass
                # Display game screen

        print(health)


        # Allow for the user to quit out of game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        counter += 1

        pygame.display.flip()

    pygame.quit()

gameplay()