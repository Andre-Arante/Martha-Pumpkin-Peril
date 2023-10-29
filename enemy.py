import random
import pygame

class Enemy:
    def __init__(self, screen):
        self.x = random.randint(0, 1000)
        self.y = 0
        self.v = -1
        self.screen = screen

    def draw(self):
        pygame.draw.circle(self.screen, 'purple', (self.x, self.y), 10)

    def move(self):
        self.y -= self.v


    
