"""
Homework 3
CSP solver
Intro to Artificial Intelligence
Professor Pollett

Authors:
Sean Papay 007323511
Ryan Lichtig 007264348
Dakota Polenz 007879664
"""


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
			if possible_b == 0:
				inconsistent.add(b)
		if possible_b  > possible_a:
			return 1
		else:
			return -1
	
	sorted_domain = sorted(csp[0][var], comparator)
	sorted_consistent = []
	for val in sorted_domain:
		if val in inconsistent:
			break
		sorted_consistent.append(val)
	return sorted_consistent
	
def ac_3_complete(csp):
    """
    Finds all arcs within a given csp.
    :param csp: The given set of relations.
    :return: A set of all arcs in the csp.
    """
	relations = []
	for relation in csp[1]:
		relations.append(relation)
		relations.append(flip_relation(relation))
	return ac_3_partial(csp, relations)
	
def ac_3_single_variable(csp, var):
    """
    Finds all arcs pertaining to a single variable throughout
    a csp.
    :param csp: The given set of realtions.
    :param var: The varible to find all arcs and relations to and from
    :return: A set of arcs to and from the given variable.
    """
	relations = []
	for relation in csp[1]:
		if relation[2] == var:
			relations.append(relation)
		if relation[0] == var:
			relations.append(flip_relation(relation))
	return ac_3_partial(csp, relations)	
	
def revise(csp, relation):
    """
    Given a realtion attempts to infer any other reductions
    in assignments to the given values.
    :param csp: The given csp.
    :param relation: The given relation to use as a basis for 
    reducing the number of relations in the given csp.
    :return: true if the given csp has realtions that are not necessary
    """
	revised = False
	i = relation[0]
	j = relation[2]
	rel = relation[1]
	new_d_i = csp[0][i].copy()
	for i_val in csp[0][i]:
		for j_val in csp[0][j]:
			if rel(i_val, j_val):
				break;
		else:
			revised = True
			new_d_i.remove(i_val)
	csp[0][i] = new_d_i
	return revised
				
	
def ac_3_partial(csp, arcs):
    """
    Finds all arcs for the remaining csp given a set of arcs.
    :param csp: The given csp.
    :param arcs: The arcs already found or otherwise excluded.
    :return: A set of arcs for the remaining csp.
    """
	assignment = {}
	while len(arcs) > 0:
		arc = arcs[0]
		del arcs[0]
		variable = arc[0]
		if revise(csp, arc):
			domain = csp[0][variable]
			if len(domain) == 0: 
				return False
			if len(domain) == 1: (assignment[variable],) = domain
			for relation in csp[1]:
				if relation[2] == variable:
					arcs.append(relation)
				elif relation[0] == variable:
					arcs.append(flip_relation(relation))
	return assignment
	
	



def backtracking_search(csp):
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
	def backtrack(assignment, csp):
		variable = None
		for var in csp[0]:
			if not var in assignment:
				#MRV heuristic
				if (variable is None) or (len(csp[0][var]) < len(csp[0][variable])):
					variable = var
		if variable is None:
			return assignment
			
		domain = order_domain_values(variable, csp)
		
		for value in domain:
			new_assignment = assignment.copy()
			new_assignment[variable] = value
			new_csp = copy.deepcopy(csp)
			new_csp[0][variable] = {value}
			if forward_search == 1:
				inferences = ac_3_single_variable(new_csp, variable)
			else:
				inferences = {}
			if inferences != False:
					new_assignment.update(inferences)
					result = backtrack(new_assignment, new_csp)
					if result:
						return result
		return False
		
	return backtrack({},csp)


forward_search = int(sys.argv[2])
csp = parse_file(sys.argv[1])
#print csp
#exit()
sol = backtracking_search(csp);
if sol:
	var_list = sorted(list(sol.keys()))
	for var in var_list:
		print var + "=" + str(sol[var])
else:
	print 'NO SOLUTION'

