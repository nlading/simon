import pygame
from random import randint
from time import sleep, time

# Initialize all needed pygame modules
pygame.init()

# Define RGB colors
# Background colors
white = (255, 255, 255)
black = (0,0,0)
# Button colors
dark_red = (153, 0, 0)
dark_yellow = (153, 153, 0)
dark_blue = (0, 0, 179)
dark_green = (64, 128, 0)

light_red = (255, 26, 26)
light_yellow = (255, 255, 0)
light_blue = (102, 102, 255)
light_green = (153, 255, 51)

grey = (128, 128, 128)

# Determine size of the screen to define height and width
min_width = 660
min_height = 390
info = pygame.display.Info()
win_width = int(info.current_w * 0.4)
win_height = (13/22) * win_width

# Check to verify window is equal to or greater in size than the mins
if win_height < min_height or win_width < min_height:
	win_width = min_width
	win_height = min_height

# Define scaled units to implement a grid system
width_unit = int(win_width / 22)
height_unit = int(win_height / 13)

# Instantiate the window
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Simon')

# Define rectangles play
rect1 = pygame.Rect([width_unit*2, height_unit*5, width_unit*3, height_unit*3])
rect2 = pygame.Rect([width_unit*7, height_unit*5, width_unit*3, height_unit*3])
rect3 = pygame.Rect([width_unit*12, height_unit*5, width_unit*3, height_unit*3])
rect4 = pygame.Rect([width_unit*17, height_unit*5, width_unit*3, height_unit*3])
# New Game Button Attributes
rectng = pygame.Rect([width_unit*5, height_unit*9, width_unit*5, height_unit*2])
smallText = pygame.font.Font("freesansbold.ttf",20)
largeText = pygame.font.Font("freesansbold.ttf",100)

# Text objects
title = largeText.render('SIMON', True, black)
new_game_text = smallText.render('NEW GAME', True, black)
score_label = smallText.render('SCORE:', True, black)
score_display = smallText.render('5', True, black)

def draw_grid():
	for i in range(int(win_width / width_unit)):
		pygame.draw.line(screen, black, (i*width_unit,0), (i*width_unit,win_height))
	for i in range(int(win_height / height_unit)):
		pygame.draw.line(screen, black, (0,i*height_unit), (win_width,i*height_unit))


def main():
	winExit = False

	screen.fill(white)
	pygame.draw.rect(screen, dark_red, rect1)
	pygame.draw.rect(screen, dark_yellow, rect2)
	pygame.draw.rect(screen, dark_blue, rect3)
	pygame.draw.rect(screen, dark_green, rect4)
	pygame.draw.rect(screen, grey, rectng)
	screen.blit(title, (width_unit*5, height_unit*1))
	screen.blit(new_game_text, (width_unit*5.5, height_unit*9.75))
	screen.blit(score_label, (width_unit*12, height_unit*9.75))
	screen.blit(score_display, (width_unit*15, height_unit*9.75))
	# draw_grid()
	pygame.display.update()

	while not winExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				winExit = True


main()
