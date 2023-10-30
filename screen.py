import pygame, sys
from button import Button

from util import *
from enemy import *

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    
    # Turn mouse invisible
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))


    # Initial Setup Variables
    WIDTH = 1000
    HEIGHT = 500
    fps = 60
    timer = pygame.time.Clock()
    health = 3

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

        # if pygame.mouse.get_pressed()[0]:

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
                
                # Display game screen
                you_died()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('shoot')

        # Allow for the user to quit out of game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        counter += 1

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
                    play_again()
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
                    play_again()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()