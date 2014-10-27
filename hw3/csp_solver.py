import operator
import sys
import copy

def parse_file(filename):
	"""
	Parses a file to a dictionary of variables to their domain
	and a list of relation
	:param filename: The name of the file to pull data from.
	:return: tuple of ({variable:domain}, [relations])
	"""
	var_list = []
	rel_list = []
	upper_bound = 0
	file = open(filename, 'r')
	for line in file:
		parse_tuple = line.split()
		terms = [parse_tuple[0], parse_tuple[2]]
		#Checks if the first character in the variables are digits
		second_term_is_var = True
		if terms[0][0].isdigit():
			exit()
		#this is an error, yell at the user
		if terms[1][0].isdigit():
			terms[1] = int(terms[1])
			second_term_is_var = False
		#Checks list of variables for repeats
		if not terms[0] in var_list:
			var_list.append(terms[0])
		if second_term_is_var and not terms[1] in var_list:
			var_list.append(terms[1])
		#Adds relation to the relation list
		relation = parse_tuple[1]
		if relation == 'ne': relation = operator.ne
		elif relation == 'eq': relation = operator.eq
		elif relation == 'lt': relation = operator.lt
		elif relation == 'gt': relation = operator.gt
		rel_list.append((terms[0], relation, terms[1]))
		#Finds new upperbound
		if not second_term_is_var:
			if terms[1] > upper_bound: upper_bound = terms[1]
	var_dic = {}
	upper_bound = max(upper_bound, len(var_list)+1)
	for var in var_list:
		var_dic[var] = set(range(0, upper_bound))
		
	culled_rel_list = []
	for rel in rel_list:
		try:
			n = int(rel[2])
			new_domain = set()
			for val in var_dic[rel[0]]:
				if rel[1](val, n):
					new_domain.add(val)
			var_dic[rel[0]] = new_domain
		except:
			culled_rel_list.append(rel)
			continue
	parsed = (var_dic, culled_rel_list)
	file.close()
	return parsed
	


def flip_relation(rel):
	"""
	Flips a relation so that an equivilent relation for the
	latter variable is given to the first variable.
	:param rel: the relation to be fliped.
	:return: The relation with an equivilent but fliped relation
	"""
	if (rel[1] == operator.lt):
		return (rel[2], operator.gt, rel[0])
	elif (rel[1] == operator.gt):
		return (rel[2], operator.lt, rel[0])
	else:
		return (rel[2], rel[1], rel[0])


#orders values based on the least-constraining-value heuristic
def order_domain_values(var, csp):
	"""
	Orders values based on the least constraining value
	heuristic.
	:param var: The variable being ordered.
	:param assignemnt: list of assignemnts for each variable
	in the csp.
	:param csp: The varaible dictionary and relations
	:return: An orderlist of the values in var ordered by the
	least constraining value heuristic.
	"""
	relations = set()
	for relation in csp[1]:
		if var == relation[0]:
			relations.add(relation)
		elif var == relation[2]:
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
	
	sorted_domain = sorted(csp[0][var], comparator)
	sorted_consistent = []
	for val in sorted_domain:
		if val in inconsistent:
			break
		sorted_consistent.append(val)
	return sorted_consistent


#def ac_3_single_variable(new_csp, var):

def backtracking_search(csp):
	return backtrack({},csp)


def backtrack(assignment, csp):
	"""
	Recurssively assigns each varible so that each relation
	is consistant with each other.
	:param assignment: List of assignments for each variable
	in the csp.
	:param csp: An orderlist of the values in var ordered by the
	least constraining value heuristic.
	:return: The list of consistant assignments for each
	variable in the csp or false if it is not possibe.
	"""
	variable = None
	for var in csp[0]:
		if not var in assignment:
			#MRV heuristic
			if (variable is None) or (len(var[1]) < len(variable[1])):
				variable = var
	if variable is None:
		return assignment
		
	domain = order_domain_values(variable, csp)
	
	for value in domain:
		new_assignment = assignment.copy()
		new_assignment[variable] = value
		new_csp = copy.deepcopy(csp)
		new_csp[0][variable] = {value}
		if forward_search:
			inferences = ac_3_single_variable(new_csp, var)
		else:
			inferences = {}
		if inferences != False:
				new_assignment.update(inferences)
				result = backtrack(new_assignment, new_csp)
				if result:
					return result
	return False


csp = parse_file(sys.argv[1])
#print csp
#exit()
forward_search = False
print backtracking_search(csp)

