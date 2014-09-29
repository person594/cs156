# import crazy_eights

player_choice = input('Would you like to be player 0 or 1? (enter 0 or 1) ')

print(player_choice)

state = gen_initial_state()
#print state_string(state)
game_in_progress = True

while(game_in_progress):
    if player_choice == 0:
        human_move = get_human_move(state)
        state = make_move(human_move, state, [])
        
        get_comp_move(state)
    if player_choice == 1:
        get_comp_move(state)
        human_move = get_human_move(state)
        state = make_move(human_move, state, [])





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



def get_human_move(state):
    partial_state = state[2]
    partial_state_string(partial_state)
    possible_moves = gen_moves(partial_state)
    
    counter = 1
    for moves in possible_moves:
        move_to_print = ""
        move_to_print += "Move " + str(counter) + "\n"
        move_to_print = move_string(moves)
        counter += 1
    
    player_move_choice = input('Please select a move')
    player_move = possible_moves(player_move_choice - 1)
    return player_move


def get_comp_move(state):
    partial_state = state[2]
    moves = gen_moves(partial_state)
    
    
    
    
    return









