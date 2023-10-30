import random
import pygame

damage = 1

class Enemy:
    def __init__(self, screen):
        self.x = random.randint(0, 1000)
        self.y = -50
        self.v = -1
        self.screen = screen
        self.destroy = False

        self.width = self.height = 100

        skins = [
            pygame.transform.scale(pygame.image.load('assets/ghost.png.png'), (self.height, self.width)),
            pygame.transform.scale(pygame.image.load('assets/kid.png.png'), (self.height, self.width)),
            pygame.transform.scale(pygame.image.load('assets/kidWithParent.png.png'), (self.height, self.width)),
        ]
        index = random.randint(0, len(skins)-1)
        self.image = pygame.transform.scale(skins[index], (self.height, self.width))
        self.mask = pygame.mask.from_surface(self.image)

        
    def draw(self):
        # pygame.draw.circle(self.screen, 'purple', (self.x, self.y), 10)
        self.screen.blit(self.image, (self.x, self.y))


    def move(self):
        self.y -= self.v


    def overlap(self, x, y, d):
        rect1 = pygame.Rect(x, y, d, d)
        rect2 = pygame.Rect(self.x, self.y, self.width, self.height)

        return rect1.colliderect(rect2)


    def delete(self):
        self.y = -9999


    def update_health(self, height, health):
        if self.y > height: 
            self.delete()
            return health - damage
        return health

    
