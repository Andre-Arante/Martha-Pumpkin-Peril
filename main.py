# https://github.com/Andre-Arante/Martha-s-Pumpkin  

import pygame


from enemy import *
from util import *

pygame.init()


# Main Gameplay Screen
def gameplay():

    # Initial Setup Variables
    WIDTH = 1000
    HEIGHT = 500
    fps = 60
    timer = pygame.time.Clock()
    health = 10
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    # Turn mouse invisible
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    # Set background image for game
    background = pygame.image.load('./assets/lawn.png')

    # Velociaty and acceleration for the oscilation of the target
    v = 1
    a = 1

    # Play background music 
    

    # Tracks number of frames since program initialization
    counter = 0

    # Stores enemy data
    enemies = []
    spawnRate = 100

    run = True
    holding = False

    # Load Assets

    pumpkin_width = pumpkin_height = 75
    pumpkinSpin = [pygame.transform.scale(pygame.image.load('./assets/pumpkin/pumpkin.png'), 
                                          (pumpkin_width, pumpkin_height)), 
                                          pygame.transform.scale(pygame.image.load('./assets/pumpkin/pumpkin-2.png.png'), 
                                          (pumpkin_width, pumpkin_height)), 
                                          pygame.transform.scale(pygame.image.load('./assets/pumpkin/pumpkin-3.png.png'), 
                                          (pumpkin_width, pumpkin_height)), 
                                          pygame.transform.scale(pygame.image.load('./assets/pumpkin/pumpkin-4.png.png'), 
                                          (pumpkin_width, pumpkin_height)), 
                                          pygame.transform.scale(pygame.image.load('./assets/pumpkin/pumpkin-5.png.png'), 
                                          (pumpkin_width, pumpkin_height)), 
                                          pygame.transform.scale(pygame.image.load('./assets/pumpkin/pumpkin-6.png.png'), 
                                          (pumpkin_width, pumpkin_height)), 
                                          pygame.transform.scale(pygame.image.load('./assets/pumpkin/pumpkin-7.png.png'), 
                                          (pumpkin_width, pumpkin_height))
                                          ]
    cycleVar = 0
    released = False
    pumpkinPath = [0]

    grandma_image = pygame.transform.scale(pygame.image.load('assets/grandmama.jpeg'), (75, 75))

    candy_size = 50
    candy_image = pygame.transform.scale(pygame.image.load('assets/candy.png.png'), (candy_size, candy_size))


    while run:

        # Background
        screen.blit(background, (0, 0))
        timer.tick(fps) # While loop repeats 60 times per second

        # Fetch mouse position 
        mouse_pos = pygame.mouse.get_pos()

        # Draw grandma
        grandma = (WIDTH/2, HEIGHT)
        
        # Draw health bar (candies)
        screen.blit(candy_image, (100, 100))

        offset = 75
        screen.blit(grandma_image, (WIDTH/2-offset, HEIGHT-offset))

        # Draw the beizer curve between two mouse cursor and grandma
        target = (mouse_pos[0], mouse_pos[1])
        warp = (WIDTH/2, HEIGHT/2)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                holding = True

            if event.type == pygame.MOUSEBUTTONUP:
                pumpkinPath = bezier(pts, screen)
                holding = False
                released = True

        if released == True:
            if cycleVar <= len(pumpkinPath) - 1: 
                screen.blit(pumpkinSpin[cycleVar % 7], pumpkinPath[cycleVar])

                # Collision
                for e in enemies:
                    if e.overlap(pumpkinPath[cycleVar][0], pumpkinPath[cycleVar][1], pumpkin_height):
                        e.delete()

                cycleVar += 1
            else: 
                released = False
                cycleVar = 0
                
        if holding:
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

        pts = [grandma, warp, target]
        bezier(pts, screen)

        # Mouse curur

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
                # you_died()
                pass



        # Allow for the user to quit out of game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        counter += 1

        pygame.display.flip()

    pygame.quit()

gameplay()