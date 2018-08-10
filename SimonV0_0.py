# Simon V0 - Text-based
from random import randint
from time import sleep, time

HighScoreFileName = "score.txt"
try:
	openfile = open(HighScoreFileName, 'r')
	high_score = openfile.read().split(',')
	openfile.close()
except FileNotFoundError:
	high_score = []
	f = open(HighScoreFileName, 'w')
	f.close()

options = ['right', 'left', 'up', 'down']

solution = []


def prompt_start():
	"""
	Prompts the user to start a new game. If 'Y', a new game starts. Game ends with any other input.
	:return: None
	"""
	current_high_score()
	start = input("Play Simon Says? [Y/N]>> ")
	if start.lower() in 'yes':
		play_game()
	else:
		close()


def play_game():
	"""
	The main game engine. Performs all game functions and processes user input.
	:return: None
	"""
	userin = None
	add_action()
	play_solution()
	for index, item in enumerate(solution):
		userin = input(">>")
		if userin.lower() in solution[index]:
			pass
		else:
			print("Loser!")
			print("Score: %i" % len(solution))
			check_high_score()
			sleep(3)
			restart()
			return
	print("Correct!")
	print("Score: %i" % len(solution))
	sleep(1)
	play_game()


def play_solution():
	"""
	Displays the sequence of button presses the user must repeat. One instruction is shown at a time, and remains
	presented for 1 second. The command then hides itself by printing multiple new lines.
	:return: None
	"""
	for action in solution:
		start = time()
		end = start + 1
		curr = start
		print('\n')
		print(action, end=' ')
		while time() <= end:
			if time() - curr >= 0.1:
				curr = time()
				print('-', end='')
		print('\n' * 50)


def add_action():
	"""
	Appends the solution by one action. Solution is global because there is no security risk
	:return: None
	"""
	global solution
	index = randint(0, len(options) - 1)
	solution.append(options[index])


def restart():
	"""
	Clears the solution list, issues user prompt.
	:return:
	"""
	global solution
	solution[:] = []
	prompt_start()


def check_high_score():
	"""
	Checks to see if current score is the new high score. If so, overwrites existing score document.
	:return:
	"""
	global high_score
	if len(solution) > len(high_score):
		print("New High Score!!")
		high_score = solution
		openfile = open(HighScoreFileName, 'w')
		data = ','.join(solution)
		openfile.write(data)
		openfile.close()


def current_high_score():
	print("\nCurrent High Score: {0}\n".format(len(high_score)))


def close():
	print("Goodbye!")


prompt_start()
