import pygame
import pygame.midi
from queue import Queue
from random import randint

# Initialize all needed pygame modules
pygame.init()

# Define RGB colors
# Background colors
white = (255, 255, 255)
black = (0, 0, 0)
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
win_height = int((13 / 22) * win_width)

# Check to verify window is equal to or greater in size than the mins
if win_height < min_height or win_width < min_height:
	win_width = min_width
	win_height = min_height

# Define scaled units to implement a grid system
width_unit = int(win_width / 22)
height_unit = int(win_height / 13)

# Timing variables
clock_ticks = 10
on_limit = int(clock_ticks/3)

# Instantiate the window
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Simon')

# Define rectangles play
rect1 = pygame.Rect([width_unit * 2, height_unit * 5, width_unit * 3, height_unit * 3])
rect2 = pygame.Rect([width_unit * 7, height_unit * 5, width_unit * 3, height_unit * 3])
rect3 = pygame.Rect([width_unit * 12, height_unit * 5, width_unit * 3, height_unit * 3])
rect4 = pygame.Rect([width_unit * 17, height_unit * 5, width_unit * 3, height_unit * 3])
# New Game Button Attributes
rectng = pygame.Rect([width_unit * 5, height_unit * 9, width_unit * 5, height_unit * 2])
smallText = pygame.font.Font("freesansbold.ttf", 20)
largeText = pygame.font.Font("freesansbold.ttf", 100)

# Text objects
title = largeText.render('SIMON', True, black)
score_label = smallText.render('SCORE:', True, black)
score_display = smallText.render('0', True, black)

# Audio Objects
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(87)  # 87 = Lead 7 (fifths)

red_note = 55
yellow_note = 60
blue_note = 65
green_note = 70


class GameLogic:
	def __init__(self, options, timer_length):
		"""
		Manages all behind-the-scenes game mechanics.
		:param options: The possible actions that can be included in the solution.
		:param timer_length: The length of time a game element should remain in an active state
		"""
		self.options = options
		self.solution = []              # The current correct sequence of actions to be repeated
		self.display_history = []       # Tracks the actions that have been presented or guessed
		self.user_input_q = Queue()     # Allows for sequential tracking of button presses from outside the class
		self.current_display = None     # Tracks which element is currently active
		self.display_timer = 0          # The amount of time an element has been active
		self.display_timer_length = timer_length
		self.score = 0
		self.current_state = self.idle
		self.message = ''               # Messages to present to the user beneath the score

	def get_score(self):
		return self.score

	def update(self):
		"""
		Processes the current state method set in self.current_state.
		:return:
		"""
		self.current_state()

	def get_message(self):
		return self.message

	def new_game(self):
		"""
		Restarts the game. Clears all current status variables.
		:return:
		"""
		self.solution = []
		self.display_history = []
		self.score = 0
		self.message = ''
		self.add_solution()

	def idle(self):
		"""
		A hold state when waiting to begin a new game. The GUI can remain interactive without performing game actions
		:return:
		"""
		pass

	def player_turn(self):
		"""
		Processes the player's input. 3 states.
		:return:
		"""
		if not self.user_input_q.empty():
			check = self.user_input_q.get()
			if check == self.solution[len(self.display_history)]:
				# State 1: User has guessed correctly but has not guessed the entire sequence
				self.display_history.append(check)
			else:
				# State 2: Player has guessed incorrectly. Game over.
				self.game_over()
			if len(self.display_history) == len(self.solution):
				# State 3: Player has guessed the entire sequence correctly. Round over. Computer's turn.
				self.display_timer = 0
				self.display_history = []
				self.current_state = self.round_over
				self.score += 1

	def round_over(self):
		"""
		Pauses the game for 8/10s of a second, then continues.
		:return:
		"""
		round_pause = 8 / clock_ticks
		if self.display_timer >= round_pause:
			self.display_timer = 0
			self.current_state = self.add_solution
		else:
			self.display_timer += 1

	def user_input(self, obj):
		"""
		External use method. Allows the GUI to communicate with GameLogic while letting the class process passed info.
		:param obj: The object that the game must process
		:return:
		"""
		self.user_input_q.put(obj)

	def add_solution(self):
		"""
		Adds a single action to self.solution chosen at random from self.options
		:return:
		"""
		index = randint(0, len(self.options)-1)
		self.solution.append(self.options[index])
		self.current_state = self.display_solution

	def display_solution(self):
		"""
		Presents the solution to the player. Self.display_timer ensures only one presented object is active at a time.
		:return:
		"""
		if not self.current_display:
			current = len(self.display_history)
			self.solution[current].ignite()
			self.display_history.append(self.solution[current])
			self.current_display = self.solution[current]
		elif self.display_timer > self.display_timer_length:
			if not self.current_display.get_state():
				self.display_timer = 0
				self.current_display = None
		else:
			self.display_timer += 1
		if self.solution and len(self.solution) == len(self.display_history):
			self.display_timer = 0
			self.current_state = self.player_turn
			self.display_history = []

	def game_over(self):
		"""
		Player guessed incorrectly. Check if the player earned a high score and process, then wait for new game command.
		:return:
		"""
		self.check_high_score()
		self.current_state = self.idle

	def check_high_score(self):
		"""
		Checks to see if current score is the new high score. If so, overwrites existing score document.
		:return:
		"""
		HighScoreFileName = "score.txt"
		try:
			openfile = open(HighScoreFileName, 'r')
			high_score = openfile.read()
			openfile.close()
		except FileNotFoundError:
			high_score = []
			f = open(HighScoreFileName, 'w')
			f.write('0')
			f.close()
		if str(self.score) > str(high_score):
			self.message = "New High Score!!"
			openfile = open(HighScoreFileName, 'w')
			openfile.write(str(self.score))
			openfile.close()


class RectButton:
	def __init__(
		self,
		surface,
		location=None,
		on_color=None,
		off_color=None,
		tone=None,
		on_timer=0,
		on_limit=10,
		text='',
		font=pygame.font.Font("freesansbold.ttf", 20),
		player_obj=None,
		state=False,
	):
		self.surface = surface
		self.location = location
		self.on_color = on_color
		self.off_color = off_color
		self.tone = tone
		self.on_timer = on_timer
		self.on_limit = on_limit
		self.text = text
		self.font = font
		self.text_color = (0, 0, 0)
		self.player = player_obj
		self.state = state          # Init to off
		self.base_state = state     # Does not change

	def set_to_base(self):
		# Draw the body of the button on the surface
		if self.base_state:
			pygame.draw.rect(self.surface, self.on_color, self.location)
		else:
			pygame.draw.rect(self.surface, self.off_color, self.location)
		self.center_text()

	def center_text(self):
		text_obj = self.font.render(self.text, True, self.text_color)
		text_w, text_h = self.font.size(self.text)
		x_pos = self.location.centerx - int(text_w / 2)
		y_pos = self.location.centery - int(text_h / 2)
		self.surface.blit(text_obj, (x_pos, y_pos))

	def set_text(self, text):
		self.text = text

	def get_text(self):
		return self.text

	def get_state(self):
		return self.state

	def extinguish(self):
		pygame.draw.rect(self.surface, self.off_color, self.location)
		self.center_text()
		if self.player:
			self.player.note_off(self.tone)
		self.on_timer = 0
		self.state = False

	def ignite(self):
		pygame.draw.rect(self.surface, self.on_color, self.location)
		self.center_text()
		if self.player:
			self.player.note_on(self.tone, 100)
		self.on_timer = 1
		self.state = True

	def check_clicked(self, click):
		xclick, yclick = click.dict.get('pos')
		if self.location.left < xclick < self.location.right and \
			self.location.top < yclick < self.location.bottom:
			self.ignite()
			return True
		return False

	def update(self):
		if self.on_timer >= self.on_limit:
			self.state = False
			self.extinguish()
		else:
			self.on_timer += 1
		if self.state:
			pygame.draw.rect(self.surface, self.on_color, self.location)
		else:
			pygame.draw.rect(self.surface, self.off_color, self.location)
		self.center_text()


RedButton = RectButton(screen, rect1, light_red, dark_red, red_note, on_limit=on_limit, player_obj=player)
YellowButton = RectButton(screen, rect2, light_yellow, dark_yellow, yellow_note, on_limit=on_limit, player_obj=player)
BlueButton = RectButton(screen, rect3, light_blue, dark_blue, blue_note, on_limit=on_limit, player_obj=player)
GreenButton = RectButton(screen, rect4, light_green, dark_green, green_note, on_limit=on_limit, player_obj=player)
NewGameButton = RectButton(screen, rectng, light_grey, dark_grey, on_limit=on_limit, text='NEW GAME')

game_buttons = [RedButton, YellowButton, BlueButton, GreenButton, NewGameButton]
current_game = GameLogic(game_buttons[:-1], on_limit+5)


# ---------------------------------------------------------------------------------------
# Game Methods
# ---------------------------------------------------------------------------------------
def reset():
	global score_display, current_game
	for button in game_buttons:
		button.set_to_base()
	score_display = smallText.render('0', True, black)
	current_game.new_game()


def update_score():
	global score_display
	score = current_game.get_score()
	score_display = smallText.render(str(score), True, black)


# ---------------------------------------------------------------------------------------
# Begin GUI
# ---------------------------------------------------------------------------------------
def draw_grid():
	"""
	Draws a uniform grid across the entire screen
	:return: None
	"""
	for i in range(int(win_width / width_unit)):
		pygame.draw.line(screen, black, (i*width_unit, 0), (i*width_unit, win_height))
	for i in range(int(win_height / height_unit)):
		pygame.draw.line(screen, black, (0, i*height_unit), (win_width, i*height_unit))


def handle_click(event):
	for button in game_buttons:
		if button.check_clicked(event) and button.get_text() == 'NEW GAME':
			reset()
		elif button.check_clicked(event):
			current_game.user_input(button)
	pygame.display.flip()


def refresh_gui():
	"""
	Contains all base GUI attributes. "Blank Slate" or "Idle" attributes.
	:return: None
	"""
	screen.fill(white)
	update_score()
	for button in game_buttons:
		button.update()
	screen.blit(title, (width_unit * 5, height_unit * 1))
	screen.blit(score_label, (width_unit * 12, height_unit * 9.75))
	screen.blit(score_display, (width_unit * 15, height_unit * 9.75))
	msg_display = smallText.render(current_game.get_message(), True, black)
	screen.blit(msg_display, (width_unit * 12, height_unit * 10.75))


def main():
	winExit = False
	clock = pygame.time.Clock()

	# Define allowed interactions - Allows only mouse down actions, and closing the window
	pygame.event.set_allowed(None)
	pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN, pygame.QUIT])

	display_counter = 0

	while not winExit:
		# Limits while loop to a max of 10 times per second
		clock.tick(clock_ticks)
		refresh_gui()

		# Event handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				winExit = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				handle_click(event)

		# Game logic
		if current_game:
			current_game.update()

		# draw_grid()
		pygame.display.update()


main()
del player
pygame.midi.quit()
