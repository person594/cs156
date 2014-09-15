import sys
import math
import heapq
import copy

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
m = readMaze(textFile)
playerLoc = findChar('@', m)
goalLoc = findChar('%', m)

def euclidian(player, goal):
	dx = player[0] - goal[0]
	dy = player[1] - goal[1]
	return math.sqrt(dx*dx + dy*dy)
	
def manhattan(player, goal):
	dx = player[0] - goal[0]
	dy = player[1] - goal[1]
	return abs(dx) + abs(dy);

manhattanDiag = (len(m) + len(m[0])) 

#this is actually really slow, not a good heuristic at all...
def manhattanSquared(player, goal):
	square = manhattan(player, goal) * manhattan(player, goal)
	return square / manhattanDiag
	
if heur == "euclidian" :
	heuristic = euclidian
elif heur == "manhattan" :
	heuristic = manhattan
else:
	heuristic = manhattanSquared
	
	
def aStar2(start, dest, maze):
	visited = {start}
	current = start
	frontier = set()
	paths = {start : []}
	while current != dest:
		r = current[0]
		c = current[1]
		newFrontier = set()
		if isOpen(r-1, c, maze) and not (r-1, c) in visited:
			newFrontier |= {((r-1, c))}
		if isOpen(r+1, c, maze) and not (r+1, c) in visited:
			newFrontier |= {(r+1, c)}
		if isOpen(r, c-1, maze) and not (r, c-1) in visited:
			newFrontier |= {(r, c-1)}
		if isOpen(r, c+1, maze) and not (r, c+1) in visited:
			newFrontier |= {(r, c+1)}
		
		for node in newFrontier:
			if (not node in paths) or len(paths[node]) > len(paths[current]) + 1:
				newPath = copy.copy(paths[current]);
				newPath.append(current);
				paths[node] = newPath;
				
		frontier |= newFrontier
		#print frontier
		
		def comp(a, b):
			return int((len(paths[a]) + heuristic(a, dest)) - (len(paths[b]) + heuristic(b, dest)))
		
		if frontier == set():
			return None
		frontierList = list(frontier)
		frontierList.sort(comp)
		#print frontierList
		current = frontierList[0]
		visited |= {current}
		frontier -= {current}
	ret = paths[current]
	ret.append(current)
	return ret

def printPath(path, maze):
	if not path:
		print "No solution :("
		return
	step = 0
	for node in path:
		if step == 0:
			print "Initial:"
		else:
			print "Step " + str(step) + ":"
		maze[node[0]][node[1]] = '@'
		printMaze(m)
		maze[node[0]][node[1]] = ' '
		step += 1
		print
	print "Problem Solved! I had some noodles!"

#printPath(aStar2(playerLoc, goalLoc, m), m)
aStar2(playerLoc, goalLoc, m)
