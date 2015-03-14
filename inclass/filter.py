def filter(alist):
	non = []
	for element in alist: 
		if element > 0:
			non.append(element)
	return non