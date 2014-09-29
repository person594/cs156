import crazy_eights



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
		print crazy_eights.partial_state_string(state[2])
		if player_choice == to_move:
			move = get_human_move(state)
		else:
			move = get_comp_move(state)
			print crazy_eights.move_string(move)
		state = crazy_eights.make_move(move, state, [])
		game_in_progress = not crazy_eights.is_game_over(state)
		to_move = 1 - to_move





moves = gen_moves(state[2])
draw_history = []
bestMove = None
bestScore = 0;
for move in moves:
	state = make_move(move, state, draw_history)
	score = ab_max(-999999999999, 99999999999, state, 13)
	if score < bestScore or move is None:
		bestScore = score
		bestMove = move
print move_string(bestMove)





