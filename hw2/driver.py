import crazy_eights
import copy


def get_human_move(state):
    partial_state = state[2]
    possible_moves = crazy_eights.gen_moves(partial_state)
    
    counter = 1
    for moves in possible_moves:
        move_to_print = ""
        move_to_print += "Move " + str(counter) + "\n"
        move_to_print += crazy_eights.move_string(moves)
        counter += 1
        print move_to_print
    
    player_move_choice = input('Please select a move: ')
    player_move = possible_moves[player_move_choice - 1]
    return player_move


def get_comp_move(state):
		partial_state = state[2]
		moves = crazy_eights.gen_moves(partial_state)
		craz8 = crazy_eights.CrazyEight()
		return craz8.move_perfect_knowlege(state)




player_choice = input('Would you like to be player 0 or 1? (enter 0 or 1) ')
state = crazy_eights.gen_initial_state()
#print state_string(state)
game_in_progress = True

to_move = 0

while(game_in_progress):
		if player_choice == to_move:
			print crazy_eights.state_string(state)
			move = get_human_move(state)
		else:
			state = crazy_eights.flip_state(state)
			print crazy_eights.state_string(state)
			state = crazy_eights.flip_state(state)
			move = get_comp_move(state)
			print crazy_eights.move_string(move)
		state = crazy_eights.make_move(move, state, [])
		game_in_progress = not crazy_eights.is_game_over(state)
		to_move = 1 - to_move


