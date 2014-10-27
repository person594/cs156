for r in range(4):
	for c in range(4):
		print "s" + str(r) + str(c) + " lt 4"
		for r2 in range(r+1, 4):
			print "s" + str(r) + str(c) + " ne s" + str(r2) + str(c)
		for c2 in range(c+1, 4):
			print "s" + str(r) + str(c) + " ne s" + str(r) + str(c2)
		if r%2 == 0 and c%2 == 0:
			print "s" + str(r) + str(c) + " ne s" + str(r+1) + str(c+1)
