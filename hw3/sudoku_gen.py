for r in range(9):
	for c in range(9):
		print "s" + str(r) + str(c) + " lt 9"
		for r2 in range(r+1, 9):
			print "s" + str(r) + str(c) + " ne s" + str(r2) + str(c)
		for c2 in range(c+1, 9):
			print "s" + str(r) + str(c) + " ne s" + str(r) + str(c2)
		for r2 in range(r+1, (r/3+1)*3):
			for c2 in range(c+1, (c/3+1)*3):
				print "s" + str(r) + str(c) + " ne s" + str(r2) + str(c2)
