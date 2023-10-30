import pygame
import numpy as np
import math

# Bezier
def bezier(pts, screen):
    N = len(pts)
    n = N-1
    for t in np.arange(0, 1, 0.01):
        z = np.zeros(2)
        for i in range(N):
            z += np.dot((math.factorial(n)/(math.factorial(i)*math.factorial(n-i)))
                        *((1-t)**(n-i))*(t**i),pts[i])

        pygame.draw.circle(screen, (255, 0, 0), z.astype(int), 3)
