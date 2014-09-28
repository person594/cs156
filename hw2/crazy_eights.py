
import random

player_number = 0
    
def get_suit(card_number):
	return card_number / 13

def get_rank(card_number):
	return (card_number % 13) + 1
	
def gen_initial_state():
    deck = random.sample(range(52),52)
    p0_hand[]
    p1_hand[]
    count = 0
    while (count < 8)
    	p0_hand.append(deck.pop())
    	p1_hand.append(deck.pop())
    	count += 1
    face_up_card = deck.pop()
    initial_move = (1,face_up_card,get_suit(face_up_card),0)
    initial_partial_state = (face_up_card,get_suit(face_up_card),p0_hand,initial_move)
    intiail_state = (deck,p1_hand,initial_partial_state)
	return initial_state

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
	
	

def make_move(move, state, draw_history):
	if move[0] == 1:
		#flip state
	patrial_state = state[2]
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
	
	return (deck, state[1], (card_played, suit, hand, history))
	
def undo_move(state, draw_history):
	move = state[2][3].pop()
	if (move[0] == 1):
		#flip state
	partial_state state[2]
	hand = partial_state
	history = partial_state[3]
	cards_drawn = move[3]
	did_play = cards_drawn == 0;
	while cards_drawn > 0:
		card = draw_history.pop()
		
		cards_drawn -= 1
	
def is_game_over(state):
	return
def get_winner(state):
	return


class CrazyEight:
	def move(self, partial_state):
		return
	def move_perfect_knowlege(self, state):
		return
