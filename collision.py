import pygame
import sys

def moving_rect():
    # global x_speed, y_speed 
    rect1.x += x_speed
    rect1.y += y_speed    

    #collision with borders
    # if rect1.right >= screen_width or rect1.left <= 0:
    #    x_speed *= -1
    # if rect1.bottom >= screen_width or rect1.top <= 0:
    #     y_speed *= -1

    #collision with rectangle
        
    pygame.draw.rect(screen, (255,255,255), rect1)
    pygame.draw.rect(screen, (255,0,0), rect2)

def collide(rect1):
       #if it ends there
        if rect1.colliderect(rect2):
            reset_position()

def reset_position():  
    rect1.x = original_x
    rect1.y = original_y

pygame.init()
clock = pygame.time.Clock()
screen_width,screen_height = 800,800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Collision Example")

# Create two rectangles
rect1 = pygame.Rect(100, 200, 100, 100)
x_speed, y_speed = 5, 4

original_x = rect1.x
original_y = rect1.y

rect2 = pygame.Rect(700, 600, 200, 100)
other_speed = 2

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30,30,30))
    moving_rect()
    if rect1.colliderect(rect2):
        collide(rect1)
    pygame.display.flip()
    clock.tick(60)