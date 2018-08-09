# Simon V1 - Text-based
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
	
options = ['right','left','up','down']

run_game = True
solution = []

def prompt_start():
	current_high_score()
	start = input("Play Simon Says? [Y/N]>> ")
	if start.lower() in 'yes':
		play_game()
	else:
		close()
	
def play_game():
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
		print('\n'*50)
	
def add_action():
	global solution
	index = randint(0, len(options)-1)
	solution.append(options[index])
	
def restart():
	global solution
	solution[:] = []
	prompt_start()
	
def check_high_score():
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
