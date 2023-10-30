import pygame
import numpy as np
import math

pumpkinSpin = [pygame.image.load('./assets/pumpkin/pumpkin.png'), pygame.image.load('./assets/pumpkin/pumpkin-2.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-3.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-4.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-5.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-6.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-7.png.png')]

coordArr = np.array([])

# Bezier
def bezier(pts, screen):
    N = len(pts)
    n = N-1
    density = 0.1
    for t in np.arange(0, 1, density):
        z = np.zeros(2)
        for i in range(N):
            z += np.dot((math.factorial(n)/(math.factorial(i)*math.factorial(n-i)))
                        *((1-t)**(n-i))*(t**i),pts[i])

        # pygame.draw.circle(screen, (255, 0, 0), z.astype(int), 3) 

        # screen.blit(pumpkinSpin[int((t*100) % 7)], z.astype(int)) 

        np.append(coordArr, z.astype(int))
    
    return coordArr
    