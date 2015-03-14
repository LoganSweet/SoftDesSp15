def histo(string):
	d = dict()
	for letter in string:
		if letter not in d:
			d[letter] = 1
		else:
			d[letter] += 1


	print d


if __name__ == '__main__':
	histo('brontosaurus')