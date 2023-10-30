# https://github.com/Andre-Arante/Martha-s-Pumpkin  

import pygame


from enemy import *
from util import *

pygame.init()


# Main Gameplay Screen
def gameplay():

    # Turn mouse invisible
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))


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

    pumpkinSpin = [pygame.image.load('./assets/pumpkin/pumpkin.png'), pygame.image.load('./assets/pumpkin/pumpkin-2.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-3.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-4.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-5.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-6.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-7.png.png')]
    screen.blit(pumpkinSpin[1], (0, 0))
    cycleVar = 0
    released = False

    while run:

        # Background
        screen.fill('white')
        timer.tick(fps) # While loop repeats 60 times per second

        # Fetch mouse position 
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(pumpkinSpin[1], mouse_pos)

        # Draw grandma
        grandma = (WIDTH/2, HEIGHT)
        pygame.draw.circle(screen, 'gray', grandma , 50)

        # Draw the beizer curve between two mouse cursor and grandma
        target = (mouse_pos[0], mouse_pos[1])
        warp = (WIDTH/2, HEIGHT/2)
        pts = [grandma, warp, target]
        bezier(pts, screen)

        # Click detection

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Oscilate the target position
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
                print('shoot')

            if event.type == pygame.MOUSEBUTTONUP:
                pumpkinPath = bezier(pts, screen)
                
                print('released')
                released = True

        if released == True:
            if cycleVar <= pumpkinPath.size - 1: 
                screen.blit(pumpkinSpin[cycleVar % 7], pumpkinPath[cycleVar])
                cycleVar += 1
            else: 
                released = False
                

        pygame.draw.circle(screen, 'red', target, 5)
        
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