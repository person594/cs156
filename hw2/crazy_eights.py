import random
    
def get_suit(card_number):
	#Suit is an integer among 0,1,2,3
	# 0 - Spades
	# 1 - Hearts
	# 2 - Diamonds
	# 3 - Clubs
	if card_number >= 0 and card_number <= 12
		return 0
	if card_number >= 13 and card_number <= 25
		return 1
	if card_number >= 26 and card_number <= 38
		return 2
	if card_number >= 39 and card_number <= 51
		return 3
	return -1

def get_rank(card_number):
	return (card_number % 13) + 1
	
def gen_initial_state():
    deck = random.sample(range(52),52)
	return
def gen_moves(partial_state):
    return
def make_move(move, state):
    return
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
