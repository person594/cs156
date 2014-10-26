import operator

#returns a tuple ([list_of variables], [list_of_relations], domain_upper_bound)
#tuple will actually probably be ([(variable, domain)], [relations])
#just kidding, it will really be ({variable:domain}, [relations])
def parse_file(filename):

def flip_relation(rel):
	if (rel[1] == operator.lt):
		return (rel[2], operator.gt, rel[0])
	elif (rel[1] == operator.gt):
		return (rel[2], operator.lt, rel[0])
	else:
		return (rel[2], rel[1], rel[0])


#orders values based on the least-constraining-value heuristic
def order_domain_values(var, assignment, csp):
	relations = set()
	for relation in csp[1]:
		if var[0] == relation[0]:
			relations.add(relation)
		elif var[0] == relation[2]:
			relations.add(flip_relation(relation))
	
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
				return 1
			if possible_b == 0:
				return -1
		return possible_b - possible_a
	
	return sorted(var[1], comparator)

def Backtracking-Search(csp):
	return Backtrack({},csp)


def Backtrack(assignment, csp):
	variable = None
	for var in csp[0]:
		if not var[0] in assignment:
			#MRV heuristic
			if (variable is None) or (len(var[1]) < len(variable[1])):
				variable = var
	if variable is None:
		return assignment;
	
	
	
		
   for each value in Order-Domain-Values(var, assignment, csp) do
        if value is consistent with assignment then
            add {var= value} to assignment
            inferences := INFERENCE(csp, var, value) 
                //this might do AC-3 or the like
            if inferences != failure then
                add inferences to assignment
                result := Backtrack(assignment, csp)
                if result != failure then
                    return result
        remove {var = value} and inferences from assignment
   return failure
