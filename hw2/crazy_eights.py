player_number = 0

def shuffle_deck():
	return
def gen_initial_state():
	return
def gen_moves(partial_state):
	return
def make_move(move, state):
	patrial_state = state[2]
	card_played = move[1]
	suit = partial_state[1]
	hand = partial_state[2]
	cards_drawn = move[3]
	can_play = cards_drawn == 0
	deck = state[0]
	while cards_drawn > 0:
		hand |= {deck.pop()}
		cards_drawn -= 1
	history = partial_state[3]
	history.append(move)
	if (can_play):
		hand -= {card_played}
		suit = move[2]
	
	return (deck, state[1], (card_played, suit, hand, history))
	
	
def undo_move(state):
	return
def is_game_over(state):
	return
def get_winner(state):
	return


class CrazyEight:
	def move(self, partial_state):
		return
	def move_perfect_knowlege(self, state):
		return
