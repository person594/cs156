import crazy_eights
import copy
import cProfile


def get_human_move(state):
	"""
	Reads the input provided by the person playing and makes the 
	necessary actions that the input requires.
	:param state: The current game state.
	:return: The move provided by the player
	"""
	partial_state = state[2]
	possible_moves = crazy_eights.gen_moves(partial_state)
	counter = 1
	print "Select a move number:\n"
	for moves in possible_moves:
		move_to_print = ""
		move_to_print += "Move " + str(counter) + "\n"
		move_to_print += "\t" + crazy_eights.move_string(moves, True)
		counter += 1
		print move_to_print
	print
	player_move_choice = input('Please select a move: ')
	player_move = possible_moves[player_move_choice - 1]
	return player_move


def get_comp_move(state):
	"""
	Gets the move that the computer makes given the current state.
	:param state: The current game state.
	:return: The move done by the computer.
	"""
	craz8 = crazy_eights.CrazyEight()
	#return craz8.move_perfect_knowlege(state)
	return craz8.move(state[2])


def main():
	"""
	The main function to run the program from.
	"""

	player_choice = input('Would you like to be player 0 or 1? (enter 0 or 1) ')
	state = crazy_eights.gen_initial_state()
	#print state_string(state)
	game_in_progress = True

	to_move = 0

	while(game_in_progress):
		print crazy_eights.history_string(state[2][3])
		if player_choice == to_move:
			print crazy_eights.partial_state_string(state[2])
			move = get_human_move(state)
		else:
			state = crazy_eights.flip_state(state)
			print crazy_eights.partial_state_string(state[2])
			state = crazy_eights.flip_state(state)
			move = get_comp_move(state)
			print crazy_eights.move_string(move) + "\n"
		state = crazy_eights.make_move(move, state, [])
		game_in_progress = not crazy_eights.is_game_over(state)
		to_move = 1 - to_move

	print "Player " + str(crazy_eights.get_winner(state)) + " wins!"
	
main()

