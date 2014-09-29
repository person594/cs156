
import random

player_number = 0
		
def get_suit(card_number):
	return card_number / 13

def get_rank(card_number):
	return (card_number % 13) + 1
	
	
def flip_state(state):
	partial_state = state[2]
	deck = state[0]
	old_hand = partial_state[2]
	new_hand = state[1]
	
	return (deck, old_hand, (partial_state[0], partial_state[1], new_hand, partial_state[3]))
	
def gen_initial_state():
	deck = random.sample(range(52),52)
	p0_hand = set()
	p1_hand = set()
	count = 0
	while count < 8:
		p0_hand |= {deck.pop()}
		p1_hand |= {deck.pop()}
		count += 1
	face_up_card = deck.pop()
	initial_move = (1,face_up_card,get_suit(face_up_card),0)
	initial_partial_state = (face_up_card, get_suit(face_up_card), p0_hand, [initial_move])
	initial_state = (deck, p1_hand, initial_partial_state)
	return initial_state

def gen_moves(partial_state):
	move_list = []
	#May screw up everthing!!!
	player_number = 1 - len(partial_state[3]) % 2
	current_card = partial_state[0]
	current_suit = partial_state[1]
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
				move_list.append((player_number, card, eight_suit, 0))
				eight_suit += 1
		#Two special case
		elif(two_special_case == 1 and pos_rank == 2):
			move_list.append((player_number, card, pos_suit, 0))
		#checks for same number or suit
		elif((current_suit == pos_suit or current_rank == pos_rank) and two_special_case == 0):
			move_list.append((player_number, card, pos_suit, 0))
	return move_list
	
	

def make_move(move, state, draw_history):
	#if move[0] == 1:
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
	
	return end_state
	
def undo_move(state, draw_history):
	move = state[2][3].pop()
	#if (move[0] == 1):
		#flip state
	partial_state = state[2]
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
	partial_state = state[2]
	if state[0].len == 0 or state[1].len == 0 or partial_state[2] == 0:
		return true
	return false
	
def get_winner(state):
	partial_state = state[2]
	history = partial_state[3]
	
	# Using this to set the hands appropriately
	p0_hand = set()
	p1_hand = set()
	most_recent_move = history[-1]
	if most_recent_move[0] == 0:
		p1_hand = partial_state[2]
		p0_hand = state[1]
	elif most_recent_move[0] == 1:
		p1_hand = state[1]
		p0_hand = partial_state[2]
		
	# if player 1's hand size is 0
	if p1_hand.len == 0:
		return 1
		
	# if player 0's hand size is 0	
	if p0_hand.len == 0:
		return 0
	
	difference = p0_hand.len - p1_hand.len
	
	# If player 0's hand is smaller than player 1's hand
	if difference < 0:
		return 0
	
	# If player 1's hand is smaller than player 0's hand
	elif difference > 0:
		return 1
		
	# If both player's hands are equal size	
	elif difference == 0:
		return get_lowest_card_winner(p0_hand, p1_hand)
		
	return - 1

#Finds the player with the lowest card in their hand
#Returns 0 if player one has lowest, 1 if player two has the lowest
def get_lowest_card_winner(play_one_hand, play_two_hand):
	one_min = 53
	two_min = 53
	for card in play_one_hand:
		current = card
		if (current < card):
			one_min = card
	for card in play_two_hand:
		current = card
		if (current < card):
			two_min = card
	return (one_min < two_min)

class CrazyEight:
	def move(self, partial_state):
		return
	def move_perfect_knowlege(self, state):
		return
		
state = gen_initial_state()
print (state)
print gen_moves(state[2])
