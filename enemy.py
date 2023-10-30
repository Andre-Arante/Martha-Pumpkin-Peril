import random
import pygame

damage = 1

class Enemy:
    def __init__(self, screen):
        self.x = random.randint(0, 1000)
        self.y = 0
        self.v = -1
        self.screen = screen
        self.destroy = False
        

    def draw(self):
        pygame.draw.circle(self.screen, 'purple', (self.x, self.y), 10)

    def move(self):
        self.y -= self.v

    def update_health(self, height, health):
        if self.y > height and not self.destroy: 
            self.destory = not self.destroy
            return health - damage
        return health

    
