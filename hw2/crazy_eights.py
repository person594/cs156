import copy
import random
import traceback

player_number = 0

def hand_size_from_hist(history, player_number):
	"""
	Calculates the hand size of the player given from the 
	history of a state.
	:param history: The history of a state.
	:param player_number: The player by which the hand amount is calculated.
	:return:  The hand size of the given player.
	"""
	hand_size = 8
	first_card = True
	for move in history:
		if first_card:
			first_card = False
			continue
		if move[0] != player_number: continue
		if move[3] == 0:
			hand_size -= 1
		elif move[3] > 0:
			hand_size += move[3]
	return hand_size

def get_mystery_cards(partial_state):
	"""
	Estimates the cards of the other player given the cards played in prior turns
	:param partial_state: The state of the game without the contents of the 
						  deck or the other player's cards.
	:return: A set of cards that could be within the other player's hand.
	"""
	mystery = set(range(52))
	history = partial_state[3]
	for move in history:
		if move[3] != 0: continue
		mystery.remove(move[1])
	hand = partial_state[2]
	mystery -= hand
	return mystery
	
def random_state_from_partial(partial_state):
	"""
	Generates a random state given the possible cards that could still be in play
	:param partial_state: The state that the player currently has access to.
	:return: A estimated state of the current game.
	"""
	history = partial_state[3]
	our_player_number = 1 - history[-1][0]
	their_hand_size = hand_size_from_hist(history, 1 - our_player_number)
	mystery = get_mystery_cards(partial_state)
	their_hand = set(random.sample(mystery, their_hand_size))
	mystery -= their_hand
	deck = random.sample(mystery, len(mystery))
	
	return (deck, their_hand, partial_state)
	


def get_suit(card_number):
	"""
	Finds the suit of the card given its number in the deck.
	:param card_number: The number of the card within the deck.
	:return: The suit of the card where spades = 0, hearts = 1, 
			 diamonds = 2, and clubs = 3
	"""
	return card_number / 13

def get_rank(card_number):
	"""
	Finds the rank of the card given the card's number in the deck.
	:param card_number: The number of the card.
	:return: The rank of the card where 1-10 are there respective numbers
			 and 11-13 are the face cards in thier order in typical card layouts
	"""
	return (card_number % 13) + 1
	
def card_string(card_number):
	"""
	Creates a string from a card that is more easily viewed.
	:param card_number: The number of the card in the deck.
	:return: A string where the card is displayed as [card rank][card suit]
	"""
	suits = ['S', 'H', 'D', 'C']
	ranks = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
	return ranks[get_rank(card_number)] + suits[get_suit(card_number)]

def move_string(move, present_tense=False, first_turn=False):
	"""
	Creates a string from a move that is more easily viewed.
	:param move: The move that is to be made into a string.
	:param presend_tense: If the sentance being printed should be in the present tense.
	:param first_turn: If the move is the first turn.
	:return: A string where the move is displayed.
	"""
	player = move[0]
	card = move[1]
	pretty_card = card_string(card)
	card_picked = move[3]
	suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
	if first_turn:
		return pretty_card + " was revealed!"
	if present_tense:
		if card_picked == 0:
			return "Play " + pretty_card +", making the current suit " + suits[move[2]]
		elif card_picked == -1:
			return "Skip your turn"
		else:
			if card_picked == 1:
				return "Pick up a card"
			else:
				return "Pick up " + str(card_picked) + " cards"
	else:
		if card_picked == 0:
			return "Player "+ str(player) + " played " + pretty_card +", making the suit " + suits[move[2]]
		elif card_picked == -1:
			return "Player "+ str(player) + "'s turn was skipped"
		else:
			if card_picked == 1:
				return "Player "+ str(player) + " picked up a card"
			else:
				return "Player "+ str(player) + " picked up " + str(card_picked) + " cards"
	
def state_string(state):
	"""
	Creates a string from a state that is more easily viewed.
	:param state: the state that is to be made into a string.
	:return: A string where the state is displayed.
	"""
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
	return out
	
def history_string(history):
	"""
	Creates a string from a history that is more easily viewed.
	:param history: The history that is to be made into a string.
	:return: A string where the history is displayed.
	"""
	hist_string = "Game History:\n"
	first = True
	for move in history:
		if first:
			first = False
			hist_string += "* " + move_string(move, False, True) 
		elif move[3] != -1:
			hist_string = hist_string + "* " + move_string(move)
		hist_string += "\n"
	return hist_string;
			
def partial_state_string(partial_state):
	"""
	Creates a string from a partial state that is more easily viewed.
	:param partial_state: The partial state that is to be made into a string.
	:return: A string where the partial state is displayed.
	"""
	face_up_card = partial_state[0]
	hand = partial_state[2]
	history = partial_state[3]
	out = ""
	out += "Top Card: " + card_string(face_up_card) + "\n"
	out += "Your Hand:\n"
	try:
		out += reduce(lambda a, b: a + ", " + b, map(card_string, hand)) + "\n"
	except:
		out += "<empty>\n"
	return out;

def flip_state(state):
	"""
	Generates a state where the cards in the hand are the other player's hand.
	:param state: The state to be fliped.
	:return: A state where the other player's hand is currently featured in the
			 state
	"""
	partial_state = state[2]
	deck = state[0]
	old_hand = partial_state[2]
	new_hand = state[1]
	return (deck, old_hand, (partial_state[0], partial_state[1], new_hand, partial_state[3]))
	
def gen_initial_state():
	"""
	Generates a state where the deck is shuffled and each player has 5 random cards.
	:return: An initial state to play off of.
	"""
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
	"""
	Generates a list of possible moves a player can play given their hand 
	as well as the card that is currently face up.
	:param partial_state: The state that contains the face up card as well
						  as the player hand and history.
	:return: A list of moves that the current player can legally play.
	"""
	move_list = []
	#May screw up everthing!!!
	player_number = 1 - len(partial_state[3]) % 2
	current_card = partial_state[0]
	current_suit = partial_state[1]
	current_hand = partial_state[2]
	current_history = partial_state[3]
	current_rank = get_rank(current_card)
	two_special_case = False
	last_move = current_history[-1]
	last_rank = get_rank(last_move[1])
	last_suit = last_move[2]
	last_draw = last_move[3]

	#special cases: only apply when a card was played last turn, i.e. no cards drawn
	if last_draw == 0:
		if (last_rank == 2):
			two_special_case = True
		if (last_rank == 11):
			return [(player_number, current_card, current_suit, -1)]
		if (last_rank == 12 and last_suit == 0):
			return [(player_number, current_card, current_suit, 5)]
	#Searches through hand for moves
	for card in current_hand:
		pos_rank = get_rank(card)
		pos_suit = get_suit(card)
		#Checks for eights in hand
		if(pos_rank == 8 and not two_special_case):
			eight_suit = 0
			while eight_suit < 4:
				move_list.append((player_number, card, eight_suit, 0))
				eight_suit += 1
		#Two special case
		elif(two_special_case and pos_rank == 2):
			move_list.append((player_number, card, pos_suit, 0))
		#checks for same number or suit
		elif((current_suit == pos_suit or current_rank == pos_rank) and not two_special_case):
			move_list.append((player_number, card, pos_suit, 0))
	#Adds picked operations based on how many 2s were placed previously
	if (two_special_case):
		cards_picked = 0
		from_back = 1
		while from_back <= len(current_history) and get_rank(current_history[-from_back][1]) == 2 and current_history[-from_back][3] == 0:
			cards_picked += 2
			from_back += 1
		move_list.append((player_number, 0, 0, cards_picked))
	else:
		move_list.append((player_number, 0, 0, 1))
	return move_list

def make_move(move, state, draw_history):
	"""
	Makes a move on the current state.
	:param move: The move to be played.
	:param state: The state to be played on.
	:param draw_history: The history of cards played.
	:return: A new state where the move has been made and it is
			 the opposing player's turn.
	"""
	partial_state = state[2]
	hand = partial_state[2]
	cards_drawn = move[3]
	can_play = cards_drawn == 0
	new_top_card = partial_state[0]
	suit = partial_state[1]
	deck = state[0]
	card_played = move[1]
	while cards_drawn > 0 and deck != []:
		card = deck.pop()
		hand.add(card)
		draw_history.append(card)
		cards_drawn -= 1
	history = partial_state[3]
	history.append(move)
	if (can_play):
		assert card_played in hand
		hand.remove(card_played)
		new_top_card = card_played
		suit = move[2]
		
	end_state = (deck, state[1], (new_top_card, suit, hand, history))
	return flip_state(end_state)
	
def undo_move(state, draw_history):
	"""
	Generates a state back to the previous state in the history.
	:param state: The state to be reverted.
	:param draw_history: The history of cards played.
	:return: The state in it's previous state.
	"""
	state = flip_state(state)
	partial_state = state[2]
	hand = partial_state[2]
	history = partial_state[3]
	move = history.pop()
	cards_drawn = move[3]
	deck = state[0]
	did_play = cards_drawn == 0;
	while cards_drawn > 0 and draw_history != []:
		card = draw_history.pop()
		hand .remove(card)
		deck.append(card)
		cards_drawn -= 1
	if did_play:
		card_played = move[1]
		hand.add(card_played)
	prior_move = history[-1]
	top_card = prior_move[1]
	top_suit = prior_move[2]
	end_state = (deck, state[1], (top_card, top_suit, hand, history))
	return end_state
	
def is_game_over(state):
	"""
	Tests to see in a give state whether a game is over.
	:param state: The state given.
	:return: True if the game is over.
	"""
	partial_state = state[2]
	if len(state[0]) == 0 or len(state[1]) == 0 or partial_state[2] == 0:
		return True
	return False
	
def get_winner(state):
	"""
	Finds the winner of a given game.
	:param state: The given game state.
	:return: The player who has won the game.
	"""
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


def get_lowest_card_winner(play_one_hand, play_two_hand):
	"""
	Finds the player with the lowest card in their hand
	:param play_one_hand: Player one's hand.
	:param play_two_hand: Player two's hand.
	:return: The player with the lowest card in their hand.
	"""
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
	
def get_player_hands(state):
	"""
	Finds the cards in each of the player's hands.
	:param state: The current game state.
	:return: Two lists containg each of the player's hands.
	"""
	partial_state = state[2]
	history = partial_state[3]
	most_recent_move = history[-1]
	if most_recent_move[0] == 0:
		return (state[1], partial_state[2])	
	return (partial_state[2], state[1])


def get_heuristic(state):
	"""
	Determines the heuristic for choosing which move to do.
	:param state: The current game state.
	:return: The calculated heuristic for the current game state.
	"""
	hands = get_player_hands(state)
	return (len(hands[0]) - len(hands[1])) / (len(hands[0]) + len(hands[1]))
		
# Minmax Algorithm: min
def ab_min(alpha, beta, state, depth):
	"""
	Minimum component of the minmax algorithm used to find the minimum calculated
	possible move set from the state provided where the move value is
	determined by our heuristic.
	:param alpha: The maximum limit of the minimum that determines if the
				  current branch will continue to be searched.
	:param beta: The minimum limit of the maximum that determines if the
				  current branch will continue to be searched.
	:param state: The current state of the game.
	:param depth: The maximum depth in a tree allowed to be searched.
	:return: The minimum move value from the state provided.
	"""
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
		state = make_move(move, state, draw_history)
		beta = min(beta, ab_max(alpha, beta, state, depth - 1))
		state = undo_move(state, draw_history)
		if beta <= alpha:
			return alpha
	return beta

# Minmax Algorithm: max
def ab_max(alpha, beta, state, depth):
	"""
	Maximum component of the minmax algorithm used to find the maximum calculated
	possible move set from state provided where the move value is determined by
	our heuristic.
	:param alpha: The maximum limit of the minimum that determines if the
				  current branch will continue to be searched.
	:param beta: The minimum limit of the maximum that determines if the
				  current branch will continue to be searched.
	:param state: The current state of the game.
	:param depth: The maximum depth in a tree allowed to be searched.
	:return: The minimum move value from the state provided.
	"""
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
		state = make_move(move, state, draw_history)
		alpha = max(alpha, ab_min(alpha, beta, state, depth - 1))
		state = undo_move(state, draw_history)
		if alpha >= beta:
			return beta
	return alpha


class CrazyEight:
	depth = 11
	def move(self, partial_state):
		"""
		Makes a move to the given partial state.
		:param partial_state: The state that is being played on.
		"""
		possibilities_tried = 25
		moves = {}
		for p in range(possibilities_tried):
			state = random_state_from_partial(partial_state)
			move = self.move_perfect_knowlege(state)
			if (move in moves):
				moves[move]+= 1
			else:
				moves[move] = 1
		mode = None
		count = 0
		for move in moves:
			if moves[move] > count:
				mode = move
				count = moves[move]
		return mode
	def move_perfect_knowlege(self, state):
		"""
		Makes a move based off of complete knowledge of both players hands and
		the cards remaining in the deck.
		:param state: The current game state.
		:return: The best move for the player to make
		"""
		#this makes sense, trust me
		current_player = 1 - state[2][3][-1][0]
		moves = gen_moves(state[2])
		assert len(moves) > 0
		draw_history = []
		bestMove = None
		bestScore = 0;
		for move in moves:
			new_state = copy.deepcopy(state)
			new_state = make_move(move, new_state, draw_history)
			if current_player == 0:
				score = ab_max(-float('inf'), float('inf'), new_state, self.depth)
				if score < bestScore or bestMove is None:
					bestScore = score
					bestMove = move
			else:
				score = ab_min(-float('inf'), float('inf'), new_state, self.depth)
				if score > bestScore or bestMove is None:
					bestScore = score
					bestMove = move
		return bestMove
	
	
	
