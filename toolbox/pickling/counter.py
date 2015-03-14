""" A program that stores and updates a counter using a Python pickle file"""

from os.path import exists
import sys
from pickle import dump, load

def update_counter(file_name, reset=False):
	""" Updates a counter stored in the file 'file_name'

		A new counter will be created and initialized to 1 if none exists or if
		the reset flag is True.

		If the counter already exists and reset is False, the counter's value will
		be incremented.

		file_name: the file that stores the counter to be incremented.  If the file
				   doesn't exist, a counter is created and initialized to 1.
		reset: True if the counter in the file should be rest.
		returns: the new counter value

	>>> update_counter('blah.txt',True)
	1
	>>> update_counter('blah.txt')
	2
	>>> update_counter('blah2.txt',True)
	1
	>>> update_counter('blah.txt')
	3
	>>> update_counter('blah2.txt')
	2
	"""

	if exists(file_name):                      # if the file already exists
		data = load(open(file_name, "r+"))     # set data to the number stored in the file
		data += 1                              # then inciment up one in data
		if reset:                              #  if the counter needs to be reset
			data = 1                           # set data to 1
	else:                                      # if the file doesn't exist
		data = 1                               # set data to one
	
	dump (data, open(file_name, "w+"))         # write the info in data to the file   
	return data                                


if __name__ == '__main__':
	if len(sys.argv) < 2:
		import doctest
		doctest.testmod()
	else:
		print "new value is " + str(update_counter(sys.argv[1]))