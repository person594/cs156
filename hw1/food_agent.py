import sys
import math

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

m = readMaze(textFile)
playerLoc = findChar('@', m)
goalLoc = findChar('%', m)
print heuristic((0, 0), (5, 12))
