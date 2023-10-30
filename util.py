import pygame
import numpy as np
import math

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
    