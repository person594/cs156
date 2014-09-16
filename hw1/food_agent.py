import sys
import math
import heapq
import copy
import time

if len(sys.argv) != 3 :
    print "Usage : python food_agent.py file_name heuristic"
    quit()
fileName = sys.argv[1]

textFile = open(fileName)

#given a text file f, returns a 2d list of characters from f
def read_maze(f) :
    maze = []
    for line in f :
        row = []
        for char in line :
            if char != '\n' :
                row.append(char)
        maze.append(row)
    return maze

#prints maze m to the terminal
def print_maze(m) :
    for row in m:
        s = ""
        for el in row:
            s += el
        print s
        
#locates the first occurence of character c in m, and returns (row, col)
def find_char(ch, m) :
    r = 0
    for row in m:
        c = 0
        for el in row:
            if el == ch:
                return r, c
            c += 1
        r += 1
        
#returns true iff maze[row][col] is passable        
def is_open(row, col, maze):
    if 0 <= row < len(maze) and 0 <= col < len(maze[row]):
        return maze[row][col] != '#'
    else: return False

heur = sys.argv[2]
m = read_maze(textFile)
playerLoc = find_char('@', m)
goalLoc = find_char('%', m)
if not (playerLoc and goalLoc):
	print "No solution :(\nNo soup for you"
	quit()

#euclidian distance between two points
def euclidian(player, goal):
    dx = player[0] - goal[0]
    dy = player[1] - goal[1]
    return math.sqrt(dx*dx + dy*dy)
    
#manhattan distance between two points
def manhattan(player, goal):
    dx = player[0] - goal[0]
    dy = player[1] - goal[1]
    return abs(dx) + abs(dy);

#our custom heuristic, mostly follows the manhattan heuristic but
#takes advantage of minimal preprocessing of the maze
#if the player shares a row or column with the goal, and the goal is not
#within the player's line of sight, we know the minimum distance must be
#2 + the manhattan distance
def custom(player, goal):
    if player[1] == goal[1] and (player[0] < rowMin or player[0] > rowMax):
		    return manhattan(player, goal) + 2
		
    if player[0] == goal[0] and (player[1] < colMin or player[1] > colMax):
		    return manhattan(player, goal) + 2
    else:
	      return manhattan(player, goal)

def preprocessMaze(goal, maze):
	r = goal[0]
	c = goal[1]
	global rowMin, rowMax, colMin, colMax
	while r > 0 and is_open(r, c, maze):
		r-= 1
	rowMin = r
	r = goal[0]
	while r < len(maze) and is_open(r, c, maze):
		r += 1
	rowMax = r
	r = goal[0]
	
	while c > 0 and is_open(r, c, maze):
		c-= 1
	colMin = c
	c = goal[1]
	while c < len(maze[r]) and is_open(r, c, maze):
		c += 1
	colMax = c
    
if heur == "euclidian" :
    heuristic = euclidian
elif heur == "manhattan" :
    heuristic = manhattan
else:
    heuristic = custom
    
#the A* algorithm, returns a lists of coordinates visited along the shortest
#path from start to dest in maze    
def a_star(start, dest, maze):
    visited = {start}
    current = start
    frontier = []
    paths = {start : []}
    traveled = {start : 0}
    while current != dest:
        r = current[0]
        c = current[1]
        newFrontier = set()
        if is_open(r-1, c, maze) and not (r-1, c) in visited:
            newFrontier |= {((r-1, c))}
        if is_open(r+1, c, maze) and not (r+1, c) in visited:
            newFrontier |= {(r+1, c)}
        if is_open(r, c-1, maze) and not (r, c-1) in visited:
            newFrontier |= {(r, c-1)}
        if is_open(r, c+1, maze) and not (r, c+1) in visited:
            newFrontier |= {(r, c+1)}
        
        newPath = copy.copy(paths[current]);
        newPath.append(current);
        for node in newFrontier:
            if (not node in traveled) or traveled[node] > traveled[current] + 1:
                paths[node] = newPath;
                traveled[node] = traveled[current]+1
            heapq.heappush(frontier, (traveled[node] + 
							heuristic(node, dest), node))
        
        if frontier == []:
            return None
        visited |= {current}
        while current in visited:
            current = heapq.heappop(frontier)[1]
        
    ret = paths[current]
    ret.append(current)
    return ret

#given a list of visited coordinates and a maze, prints the progress one
#step at a time
def print_path(path, maze):
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
        print_maze(m)
        maze[node[0]][node[1]] = '.'
        step += 1
        print
    print "Problem Solved! I had some noodles!"


beginTime = time.clock()
if heuristic == custom:
    preprocessMaze(goalLoc, m)
path = a_star(playerLoc, goalLoc, m)
#uncomment the following line to print the runtime of the A* algorithm
#print "Runtime: " + str(time.clock() - beginTime)
print_path(path, m)
