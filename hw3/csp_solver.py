import operator
import sys

#returns a tuple ({variable:domain}, [relations])
def parse_file(filename):
	varList = []
	relList = []
	upperBound = 0
	file = open(filename, 'r')
	for line in file:
		parseTuple = line.split()
		terms = [parseTuple[0], parseTuple[2]]
		#Checks if the first character in the variables are digits
		second_term_is_var = True
		if terms[0][0].isdigit():
			exit()
		#this is an error, yell at the user
		if terms[1][0].isdigit():
			terms[1] = int(terms[1])
			second_term_is_var = False
		#Checks list of variables for repeats
		if not terms[0] in varList:
			varList.append(terms[0])
		if second_term_is_var and not terms[1] in varList:
			varList.append(terms[1])
		#Adds relation to the relation list
		relation = parseTuple[1]
		if relation == 'ne': relation = operator.ne
		elif relation == 'eq': relation = operator.eq
		elif relation == 'lt': relation = operator.lt
		elif relation == 'gt': relation = operator.gt
		relList.append((terms[0], relation, terms[1]))
		#Finds new upperbound
		if not second_term_is_var:
			if terms[1] > upperBound: upperBound = terms[1]
	varDic = {}
	upperBound = max(upperBound, len(varList)+1)
	for var in varList:
		varDic[var] = set(range(0, upperBound))
	parsed = (varDic, relList)
	file.close()
	return parsedS
	


def flip_relation(rel):
	if (rel[1] == operator.lt):
		return (rel[2], operator.gt, rel[0])
	elif (rel[1] == operator.gt):
		return (rel[2], operator.lt, rel[0])
	else:
		return (rel[2], rel[1], rel[0])


#orders values based on the least-constraining-value heuristic
def order_domain_values(var, csp):
	relations = set()
	for relation in csp[1]:
		if var[0] == relation[0]:
			relations.add(relation)
		elif var[0] == relation[2]:
			relations.add(flip_relation(relation))
	
	inconsistent = set()
	
	def comparator(a, b):
		if a in inconsistent:
			return 1
		if b in inconsistent:
			return -1
		
		possible_a = 1
		possible_b = 1
		
		for rel in relations:
			n_a = 0
			n_b = 0
			for value in csp[0][rel[2]]: #for each value in the other variable's domain
				if rel[1](a, value):
					n_a += 1
				if rel[1](b, value):
					n_b += 1
			possible_a *= n_a
			possible_b *= n_b
			if possible_a == 0:
				inconsistent.add(a)
				return 1
			if possible_b == 0:
				inconsistent.add(b)
				return -1
		return possible_b - possible_a
	
	sorted_domain = sorted(var[1], comparator)
	sorted_consistent = []
	for val in sorted_domain:
		if val in inconsistent:
			break
		sorted_consistent.append(val)
	return sorted_consistent

def Backtracking-Search(csp):
	return Backtrack({},csp)


def Backtrack(assignment, csp):
	variable = None
	for var in csp[0]:
		if not var in assignment:
			#MRV heuristic
			if (variable is None) or (len(var[1]) < len(variable[1])):
				variable = var
	if variable is None:
		return assignment
		
	domain = order_domain_values(variable, csp)
	
	for value in domain
		appended_assignment = assignment.copy()
		appended_assignment[var] = value
		inferences := INFERENCE(csp, var, value) 
				//this might do AC-3 or the like
		if inferences != failure then
				add inferences to assignment
				result := Backtrack(assignment, csp)
				if result != failure then
						return result
		remove {var = value} and inferences from assignment
   return failure


csp = parse_file(sys.argv[1])
for var in csp[0]:
	print var + " e " + str(csp[0][var])

