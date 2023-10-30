import pygame, sys

from util import *
from enemy import *

import numpy as np
import math

pygame.init()

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

    


pumpkinSpin = [pygame.image.load('./assets/pumpkin/pumpkin.png'), pygame.image.load('./assets/pumpkin/pumpkin-2.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-3.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-4.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-5.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-6.png.png'), pygame.image.load('./assets/pumpkin/pumpkin-7.png.png')]

coordArr = np.array([])

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

def bezier(pts, screen):
    list = []
    N = len(pts)
    n = N-1
    density = 0.05
    for t in np.arange(0, 1, density):
        z = np.zeros(2)
        for i in range(N):
            z += np.dot((math.factorial(n)/(math.factorial(i)*math.factorial(n-i)))
                        *((1-t)**(n-i))*(t**i),pts[i])

        pygame.draw.circle(screen, (255, 0, 0), z.astype(int), 3) 
        # screen.blit(pumpkinSpin[int((t*100) % 7)], z.astype(int)) 

        # print('append', z.astype(int))
        # np.append(coordArr, np.array(z.astype(int)))
        list.append(z.astype(int))
    
    return list
    

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    
    # Initial Setup Variables
    WIDTH = 1280
    HEIGHT = 720
    fps = 30
    timer = pygame.time.Clock()
    health = 3
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    # Turn mouse invisible
    pygame.mouse.set_visible(False)

    # Set background image for game
    background = pygame.transform.scale((pygame.image.load('./assets/lawn.png')), (1280, 720))

    # Play Background Music
    
    pygame.mixer.init()
    pygame.mixer.music.load("./assets/audio/musicSongShit.mp3") 
    pygame.mixer.music.play(-1,0.0)

    # Velociaty and acceleration for the oscilation of the target
    v = 1
    a = 1

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
    keydown_left = False
    keydown_right = False
    pumpkinPath = [0]


    candy_size = 75
    candy_image = pygame.transform.scale(pygame.image.load('assets/candy.png.png'), (candy_size, candy_size))
    black_candy_image = pygame.transform.scale(pygame.image.load('assets/blackCandy.png.png'), (candy_size, candy_size))
    
    splat_size = 250
    splat_image = pygame.transform.scale(pygame.image.load('assets/splat.png'), (splat_size, splat_size))
    splat_x = splat_y = 0
    splatted = False
    splat_count = 0

    grandma_size = 125
    grandma_front = pygame.transform.scale(pygame.image.load('assets/grandmaFront.png.png'), (grandma_size, grandma_size))
    grandma_hand_down = pygame.transform.scale(pygame.image.load('assets/grandmaHandDown.png.png'), (grandma_size, grandma_size))
    grandma_hand_up = pygame.transform.scale(pygame.image.load('assets/grandmaHandUp.png.png'), (grandma_size, grandma_size))
    

    grandma_img = grandma_front

    target_x = WIDTH/2
    target_y = HEIGHT
    target = (target_x, target_y)

    while run:

        # If counter >= 3600 ( 1 min ) display win screen
        if counter >= 3600:
            pygame.mouse.set_visible(True)
            you_won()

        # Background
        screen.blit(background, (0, 0))
        timer.tick(fps) # While loop repeats 60 times per second

        # Fetch mouse position 
        mouse_pos = pygame.mouse.get_pos()

        # Draw grandma
        grandma = (WIDTH/2, HEIGHT)
        # screen.blit(grandma_img, grandma) 
        
        # Draw health bar (candies)
        for i in range(0, health):
            screen.blit(candy_image, (100+50*i, 140))
        for j in range(health, 3):
            screen.blit(black_candy_image, (100+50*j, 140))

        offset = 75
        screen.blit(grandma_img, (WIDTH/2-offset, HEIGHT-offset-25))

        # Draw the beizer curve between two mouse cursor and grandma
        # target = (mouse_pos[0], mouse_pos[1])
        target = (target_x, target_y)
        warp = (WIDTH/2, HEIGHT/2)
        
        for event in pygame.event.get():
            # checking if key "A" was pressed

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    keydown_left = True
                if event.key == pygame.K_RIGHT:
                    keydown_right = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    keydown_left = False
                if event.key == pygame.K_RIGHT:
                    keydown_right = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                holding = True

                grandma_img = grandma_hand_up

            if event.type == pygame.MOUSEBUTTONUP:
                pumpkinPath = bezier(pts, screen)
                holding = False
                released = True
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('./ESM_Karate_Throw_Whoosh_Explainer_Video__Mobile_App_Game_Swish_Swoosh_Movement.wav'))
                grandma_img = grandma_hand_down

        if released == True:
            # Reset the target
            target_x = WIDTH/2
            target_y = HEIGHT

            # stufff
            if cycleVar <= len(pumpkinPath) - 1: 
                screen.blit(pumpkinSpin[cycleVar % 7], pumpkinPath[cycleVar])

                # Collision
                for e in enemies:
                    if e.overlap(pumpkinPath[cycleVar][0], pumpkinPath[cycleVar][1], pumpkin_height):
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('./splatSound.mp3'))
                        e.delete()
                        splat_x = pumpkinPath[cycleVar][0]
                        splat_y = pumpkinPath[cycleVar][1]
                        splatted = True



                cycleVar += 1
            else: 
                released = False
                cycleVar = 0
        
        if splatted == True:
            screen.blit(splat_image, (splat_x-splat_size/2, splat_y-splat_size/2))
            splat_count += 1
            if splat_count > 12:
                splatted = False
                splat_count = 0

        if holding:
            target_y -= 5
            # # Oscilate the target position
            # v += a
            # d = 1
            # upper = 20
            # lower = -20
        
            # # Change velocity if we hit upper or lower bound 
            # if v > upper or v < lower:
            #     a *= -1

            # # If on right side of screen, oscilate along y=-x line
            # if mouse_pos[0] > WIDTH/2:
            #     d = -1
            
            # target = (mouse_pos[0]+v, mouse_pos[1]+v*d)

        x_speed = 15
        if keydown_left and target_x > 15:
            target_x -= x_speed
            
        if keydown_right and target_x < WIDTH-15:
            target_x += x_speed

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
                pygame.mouse.set_visible(True)
                you_died()

        # Allow for the user to quit out of game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        counter += 1

        # Display Number of Candies Left
        text = get_font(90).render(str(int(counter/60)), True, "#b68f40")
        text_rect = text.get_rect(center=(100, 75))
        screen.blit(text, text_rect)

        # Draw health bar (candies)
        for i in range(0, health):
            screen.blit(candy_image, (100+50*i, 140))
        for j in range(health, 3):
            screen.blit(black_candy_image, (100+50*j, 140))

        pygame.display.flip()

    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("TUTORIAL", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(100, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_TEXT = get_font(35).render("Long ago there was an old grumpy grandma who hated trick-o-treaters. The trick-o-treaters are trying to get to her front doorstep and get some candy she has put out. There are only three candies so 3 trick-o-traters can get candy (You only have three lives ). Once there are no more candies the trick-o-treaters overwhelm the grandma and she loses (you lose). To defend the candies the grandma has set up a precise pumpkin shooting mechanism to hit the trick-o-treaters on their way up the front lawn.  ", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def you_died():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("YOU DIED", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY AGAIN", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def you_won():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("YOU WON", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY AGAIN", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()