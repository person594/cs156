import copy
import random
import traceback

player_number = 0
		
def get_suit(card_number):
	return card_number / 13

def get_rank(card_number):
	return (card_number % 13) + 1
	
def card_string(card_number):
	suits = ['S', 'H', 'D', 'C']
	ranks = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
	return ranks[get_rank(card_number)] + suits[get_suit(card_number)]

def move_string(move):
	if move is None: traceback.print_stack()
	player = move[0]
	card = move[1]
	pretty_card = card_string(card)
	card_picked = move[3]
	
	suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
	if card_picked == 0:
		return "Player "+ str(player) + " plays " + pretty_card +", Suit is now " + suits[move[2]] + "\n"
	elif card_picked == -1:
		return "Player "+ str(player) + "'s turn is skipped\n"
	else:
		return "Player "+ str(player) + " picks up " + str(card_picked) + " cards\n"
	
	
def state_string(state):
	deck = state[0]
	their_hand = state[1]
	partial_state = state[2]
	our_hand = partial_state[2]
	
	out = "Deck:\n";
	try:
		out += reduce(lambda a, b: a + ", " + b, map(card_string, deck)) + "\n"
	except:
		out += "<empty>\n"
	out += "Our Hand:\n"
	try:
		out += reduce(lambda a, b: a + ", " + b, map(card_string, our_hand)) + "\n"
	except:
		out += "<empty>\n"
	out += "Their Hand:\n"
	try:
		out += reduce(lambda a, b: a + ", " + b, map(card_string, their_hand)) + "\n"
	except:
		out += "<empty>\n"
	out += "Top Card: " + card_string(partial_state[0]) + "\n"
	suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
	out += "Suit: " + suits[partial_state[1]] + '\n';
	out += "History length: " + str(len(partial_state[3]))
	return out + "\n"
	
def partial_state_string(partial_state):
	face_up_card = partial_state[0]
	hand = partial_state[2]
	history = partial_state[3]
	out = ""
	out += "Top Card: " + card_string(face_up_card) + "\n"
	out += "Your Hand:\n"
	try:
		out += reduce(lambda a, b: a + ", " + b, map(card_string, hand)) + "\n"
	except:
		out += "<empty\n"
	out += "Move History:\n"
	try:
		out += reduce(lambda a, b: a + ", " + b, map(move_string, history)) + "\n"
	except:
		out += "<empty>"
	return out + "\n"
	#comment to show a change

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
	current_history = partial_state[3]
	current_rank = get_rank(current_card)
	two_special_case = 0

	if (current_rank == 2):
		two_special_case = 1
	if (current_rank == 11 and current_history[-1][3] != -1):
		return [(player_number, current_card, current_suit, -1)]
	if (current_rank == 12 and current_suit == 0):
		return [(player_number, current_card, current_suit, 5)]
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
	#Adds picked operations based on how many 2s were placed previously
	if (two_special_case == 1):
		cards_picked = 2
		hist_index = -1
		iter = 0
		while -hist_index-1 < len(current_history) and get_rank(current_history[hist_index][0]) == 2:
			cards_picked += 2
			hist_index -= 1
			move_list.append((player_number, 0, 0, cards_picked))
	else:
		move_list.append((player_number, 0, 0, 1))
	return move_list

def make_move(move, state, draw_history):
	partial_state = state[2]
	card_played = move[1]
	suit = partial_state[1]
	hand = partial_state[2]
	cards_drawn = move[3]
	can_play = cards_drawn == 0
	deck = state[0]
	while cards_drawn > 0 and deck != []:
		card = deck.pop()
		hand |= {card}
		draw_history.append(card)
		cards_drawn -= 1
	history = partial_state[3]
	history.append(move)
	if (can_play):
		assert card_played in hand
		hand -= {card_played}
		suit = move[2]
		
	end_state = (deck, state[1], (card_played, suit, hand, history))
	return flip_state(end_state)
	
def undo_move(state, draw_history):
	state = flip_state(state)
	move = state[2][3].pop()
	#if (move[0] == 1):
		#flip state
	partial_state = state[2]
	hand = partial_state[2]
	history = partial_state[3]
	cards_drawn = move[3]
	deck = state[0]
	did_play = cards_drawn == 0;
	while cards_drawn > 0 and draw_history != []:
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
	return end_state
	
def is_game_over(state):
	partial_state = state[2]
	if len(state[0]) == 0 or len(state[1]) == 0 or partial_state[2] == 0:
		return True
	return False
	
def get_winner(state):
	partial_state = state[2]
	history = partial_state[3]
	
	# Using this to set the hands appropriately
	player_hands = get_player_hands(state)
	p0_hand = player_hands[0]
	p1_hand = player_hands[1]
		
	# if player 1's hand size is 0
	if len(p1_hand) == 0:
		return 1
		
	# if player 0's hand size is 0	
	if len(p0_hand) == 0:
		return 0
	
	difference = len(p0_hand) - len(p1_hand)
	
	# If player 0's hand is smaller than player 1's hand
	if difference < 0:
		return 0
	
	# If player 1's hand is smaller than player 0's hand
	elif difference > 0:
		return 1
		
	# If both player's hands are equal size	
	elif difference == 0:
		return get_lowest_card_winner(p0_hand, p1_hand)
		
	return -1

#Finds the player with the lowest card in their hand
#Returns 0 if player one has lowest, 1 if player two has the lowest
def get_lowest_card_winner(play_one_hand, play_two_hand):
	one_min = 53
	two_min = 53
	for card in play_one_hand:
		current = card
		if (current < one_min):
			one_min = card
	for card in play_two_hand:
		current = card
		if (current < two_min):
			two_min = card
	if (one_min < two_min):
		winner = 0
	else:
		winner = 1
	return winner
	
#Always returns player 0's hand and player 1's hand
def get_player_hands(state):
	partial_state = state[2]
	history = partial_state[3]
	most_recent_move = history[-1]
	if most_recent_move[0] == 0:
		return (state[1], partial_state[2])	
	return (partial_state[2], state[1])

#Determine the heuristic for choosing wich move to do.
#player 0 wants low numbers, player 1 wants high numbers
def get_heuristic(state):
	hands = get_player_hands(state)
	return len(hands[0]) - len(hands[1])
		
# Minmax Algorithm: min
def ab_min(alpha, beta, state, depth):
	if is_game_over(state):
		winner = get_winner(state)
		if winner == 0:
			return -float('inf')
		else:
			return float('inf')
	
	if depth == 0:
		return get_heuristic(state)
	possible_moves = gen_moves(state[2])
	for move in possible_moves:
		draw_history = []
		new_state = copy.deepcopy(state)
		new_state = make_move(move, new_state, draw_history)
		beta = min(beta, ab_max(alpha, beta, new_state, depth - 1))
		#state = undo_move(state, draw_history)
		if beta < alpha:
			return beta
	return beta

# Minmax Algorithm: max
def ab_max(alpha, beta, state, depth):
	if is_game_over(state):
		winner = get_winner(state)
		if winner == 0:
			return -float('inf')
		else:
			return float('inf')
	
	if depth == 0:
		return get_heuristic(state)
	possible_moves = gen_moves(state[2])
	for move in possible_moves:
		draw_history = []
		new_state = copy.deepcopy(state)
		new_state = make_move(move, new_state, draw_history)
		alpha = max(alpha, ab_min(alpha, beta, new_state, depth - 1))
		#state = undo_move(state, draw_history)
		if alpha > beta:
			return alpha
	return alpha


class CrazyEight:
	def move(self, partial_state):
		return
	def move_perfect_knowlege(self, state):
		current_player = state[2][3][-1][0]
		moves = gen_moves(state[2])
		assert len(moves) > 0
		draw_history = []
		bestMove = None
		bestScore = 0;
		for move in moves:
			state = make_move(move, state, draw_history)
			if current_player == 0:
				score = ab_max(-float('inf'), float('inf'), state, 6)
				if score < bestScore or bestMove is None:
					bestScore = score
					bestMove = move
			else:
				score = ab_min(-float('inf'), float('inf'), state, 6)
				if score > bestScore or bestMove is None:
					bestScore = score
					bestMove = move
			state = undo_move(state, draw_history)
		assert not bestMove is None
		return bestMove
	
	
	
