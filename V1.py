import pygame
import pygame.midi
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

dark_grey = (128, 128, 128)
light_grey = (230, 230, 230)

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
score_display = smallText.render('0', True, black)

# Audio Objects
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)
notes_on = {}
tone_length = 2

red_note = 55
yellow_note = 60
blue_note = 65
green_note = 70


def draw_grid():
	"""
	Draws a uniform grid across the entire screen
	:return: None
	"""
	for i in range(int(win_width / width_unit)):
		pygame.draw.line(screen, black, (i*width_unit,0), (i*width_unit,win_height))
	for i in range(int(win_height / height_unit)):
		pygame.draw.line(screen, black, (0,i*height_unit), (win_width,i*height_unit))


def handle_click(event):
	"""
	Determines which button is pressed
	:param event: The pygame event containing the coordinates of the user's click
	:return: None
	"""
	x, y = event.dict.get('pos')
	pygame.draw.circle(screen, black, [x, y], 20, 5)
	# Check for new game button press
	if height_unit*9 < y < height_unit*11 and width_unit*5 < x < width_unit*10:
		pygame.draw.rect(screen, light_grey, rectng)
		screen.blit(new_game_text, (width_unit * 5.5, height_unit * 9.75))
	# Check for color button presses
	if height_unit*5 < y < height_unit*8:
		if width_unit*2 < x < width_unit*5:
			player.note_on(red_note, 100)
			notes_on[red_note] = 1
			pygame.draw.rect(screen, light_red, rect1)
		elif width_unit*7 < x < width_unit*10:
			player.note_on(yellow_note, 100)
			notes_on[yellow_note] = 1
			pygame.draw.rect(screen, light_yellow, rect2)
		elif width_unit*12 < x < width_unit*15:
			player.note_on(blue_note, 100)
			notes_on[blue_note] = 1
			pygame.draw.rect(screen, light_blue, rect3)
		elif width_unit*17 < x < width_unit*20:
			player.note_on(green_note, 100)
			notes_on[green_note] = 1
			pygame.draw.rect(screen, light_green, rect4)
	pygame.display.flip()


def main():
	global notes_on
	winExit = False
	clock = pygame.time.Clock()

	# Define allowed interactions - Allows only mouse down actions, and closing the window
	pygame.event.set_allowed(None)
	pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN, pygame.QUIT])

	while not winExit:
		# Limits while loop to a max of 10 times per second
		clock.tick(5)

		screen.fill(white)
		pygame.draw.rect(screen, dark_red, rect1)
		pygame.draw.rect(screen, dark_yellow, rect2)
		pygame.draw.rect(screen, dark_blue, rect3)
		pygame.draw.rect(screen, dark_green, rect4)
		pygame.draw.rect(screen, dark_grey, rectng)
		screen.blit(title, (width_unit * 5, height_unit * 1))
		screen.blit(new_game_text, (width_unit * 5.5, height_unit * 9.75))
		screen.blit(score_label, (width_unit * 12, height_unit * 9.75))
		screen.blit(score_display, (width_unit * 15, height_unit * 9.75))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				winExit = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				handle_click(event)

		turned_off = []
		for note, val in notes_on.items():
			if val >= tone_length:
				player.note_off(note)
				turned_off.append(note)
			else:
				notes_on[note] += 1
		for note in turned_off:
			del notes_on[note]

		# draw_grid()
		pygame.display.update()


main()
del player
pygame.midi.quit()