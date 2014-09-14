import sys
import math
import heapq

if len(sys.argv) != 3 :
	print "Usage : python food_agent.py file_name heuristic"
	quit()
fileName = sys.argv[1]
	
textFile = open(fileName)

def readMaze(f) :
	maze = []
	for line in f :
		row = []
		for char in line :
			if char != '\n' :
				row.append(char)
		maze.append(row)
	return maze

def printMaze(m) :
	for row in m:
		s = ""
		for el in row:
			s += el
		print s
		
def findChar(ch, m) :
	r = 0
	for row in m:
		c = 0
		for el in row:
			if el == ch:
				return r, c
			c += 1
		r += 1
		
		
def isOpen(row, col, maze):
	if 0 <= row < len(maze) and 0 <= col < len(maze[row]):
		return maze[row][col] != '#'
	else: return False

heur = sys.argv[2]

if heur == "euclidian" :
	def heuristic(player, goal) :
		dx = player[0] - goal[0]
		dy = player[1] - goal[1]
		return math.sqrt(dx*dx + dy*dy)
elif heur == "manhattan" :
		def heuristic(player, goal) :
			dx = player[0] - goal[0]
			dy = player[1] - goal[1]
			return abs(dx) + abs(dy);
	
	
frontier = []
costs = {}
def aStar(start, dest, traveled, maze):
	if start == dest:
		return []
	r0 = start[0]
	c0 = start[1]
	r1 = dest[0]
	c1 = dest[1]
	currentFrontier = []
	if isOpen(r0-1, c0, maze):
		currentFrontier.append((r0-1, c0))
	if isOpen(r0+1, c0, maze):
		currentFrontier.append((r0+1, c0))
	if isOpen(r0, c0-1, maze):
		currentFrontier.append((r0, c0-1))
	if isOpen(r0, c0+1, maze):
		currentFrontier.append((r0, c0+1))
		
	for node in currentFrontier:
		if node in costs:
			costs[node] = min(costs[node], traveled + 1 + heuristic(node, dest))
		else: costs[node] = heuristic(node, dest) + 1
		
	def comp(a, b):
		#print (a, b, costs[a], costs[b], costs[a] - costs[b])
		return int(costs[a] - costs[b])
	
	#print currentFrontier
	currentFrontier.sort(comp)
	#print currentFrontier
	for node in frontier:
		if
	
	

m = readMaze(textFile)
playerLoc = findChar('@', m)
goalLoc = findChar('%', m)
costs[playerLoc] = heuristic(playerLoc, goalLoc)
aStar(playerLoc, goalLoc, 0, m)
