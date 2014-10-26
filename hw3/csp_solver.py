import operator

#returns a tuple ([list_of variables], [list_of_relations], domain_upper_bound)
def parse_file(filename):
	varList = []
	relList = []
	upperBound = 0
	file = open('filename', 'r')
	for line in file:
		parseTuple = line.split()
		terms = [parseTuple[0], parsetuple[2]]
		#Checks if the first character in the variables are digits
		second_term_is_var = True
		if terms[0][0].isdigit():
			#this is an error, yell at the user
		if newVars[1][0].isdigit():
			terms[0] = int(terms[0])
			second_term_is_var = False
		#Checks list of variables for repeats
		if not terms[0] in varList:
			varList.append(terms[0])
		if second_term_is_var and not terms[1] in varList:
			varList.append(terms[1])
		#Adds relation to the relation list
		relation = parsedTuple[1]
		if relation == 'ne': relation = operator.ne
		elif relation == 'eq': relation = operator.eq
		elif relation == 'lt': relation = operator.lt
		elif relation == 'gt': relation = operator.gt
		relList.append((terms[0], relation, terms[1]))
		#Finds new upperbound
		if not second_term_is_var
			if terms[1] > upperBound: upperBound = terms[1]
	parsed = (varList, relList, upperBound)
	return parsed


