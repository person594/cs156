import sys

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
		for el in row:
			print el,
		print
		

printMaze(readMaze(textFile))
