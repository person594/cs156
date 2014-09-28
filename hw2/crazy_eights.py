def shuffle_deck():
    
def gen_initial_state():

def gen_moves(partial_state):
    move_list = {}
    current_card = partial_state[1]
    curernt_suit = partial_state[2]
    current_hand = partial_state[3]
	current_rank = get_rank(current_card)
	#Searches through hand for 
	for card in current_hand:
		pos_rank = get_rank(card)
		pos_suit = get_suit(card)
		#checks for eights in hand
		if(pos_rank == 8):
			eight_suit = 0
			while eight_suit < 4:
				move_list.append(player_number, card, eight_suit, 0)
				eight_suit += 1
		#checks for same number or suit
		elif(current_suit == pos_suit or current_rank == pos_rank):
			move_list.append(player_number, card, pos_suit, 0)
	return move_list
	
	
    
    
    

def make_move(move, state):
    
def undo_move(state):

def is_game_over(state):

def get_winner(state):



class CrazyEight:
    def move(self, partial_state):
    
    def move_perfect_knowlege(self, state):
    
