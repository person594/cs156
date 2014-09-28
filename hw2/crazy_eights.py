
import random

player_number = 0
    
def get_suit(card_number):
	return card_number / 13

def get_rank(card_number):
	return (card_number % 13) + 1
	
def gen_initial_state():
    deck = random.sample(range(52),52)
    p0_hand = []
    p1_hand = []
    count = 0
    while (count < 8)
    	p0_hand.append(deck.pop())
    	p1_hand.append(deck.pop())
    	count += 1
    face_up_card = deck.pop()
    initial_move = (1,face_up_card,get_suit(face_up_card),0)
    initial_partial_state = (face_up_card,get_suit(face_up_card),p0_hand,[initial_move])
    intiail_state = (deck,p1_hand,initial_partial_state)
	return initial_state

def gen_moves(partial_state):
    move_list = {}
	#May screw up everthing!!!
	player_number = 1 - len(partial_state[3]) % 2
    current_card = partial_state[0]
    curernt_suit = partial_state[1]
    current_hand = partial_state[2]
	current_rank = get_rank(current_card)
	two_special_case= 0
	if (current_rank == 2):
		two_special_case = 1
	if (current_rank == 11):
		return (player_number, current_card, current_suit, -1)
	if (current_rank == 12):
		return (player_number, current_card, current_suit, 5)
	#Searches through hand for moves
	for card in current_hand:
		pos_rank = get_rank(card)
		pos_suit = get_suit(card)
		#Checks for eights in hand
		if(pos_rank == 8 and two_special_case == 0):
			eight_suit = 0
			while eight_suit < 4:
				move_list.append(player_number, card, eight_suit, 0)
				eight_suit += 1
		#Two special case
		elif(two_special_case == 1 and pos_rank == 2):
			move_list.append(player_number, card, pos_suit, 0)
		#checks for same number or suit
		elif((current_suit == pos_suit or current_rank == pos_rank) and two_special_case == 0):
			move_list.append(player_number, card, pos_suit, 0)
	return move_list
	
	

def make_move(move, state, draw_history):
	if move[0] == 1:
		#flip state
	partial_state = state[2]
	card_played = move[1]
	suit = partial_state[1]
	hand = partial_state[2]
	cards_drawn = move[3]
	can_play = cards_drawn == 0
	deck = state[0]
	while cards_drawn > 0:
		card = deck.pop()
		hand |= {card}
		draw_history.append(card)
		cards_drawn -= 1
	history = partial_state[3]
	history.append(move)
	if (can_play):
		hand -= {card_played}
		suit = move[2]
	
	end_state = (deck, state[1], (card_played, suit, hand, history))
	# flip back if needed
	
	return return end_state
	
def undo_move(state, draw_history):
	move = state[2][3].pop()
	if (move[0] == 1):
		#flip state
	partial_state state[2]
	hand = partial_state
	history = partial_state[3]
	cards_drawn = move[3]
	deck = state[0]
	did_play = cards_drawn == 0;
	while cards_drawn > 0:
		card = draw_history.pop()
		hand = hand - {card}
		deck.append(card)
		cards_drawn -= 1
	if did_play:
		card_played = move[1]
		hand = hand | {card_played}
	prior_move = history[-1]
	top_card = prior_move[1]
	top_suit = prior_move[2]
	end_state = (deck, state[1], (top_card, top_suit, hand, history))
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
