""" Analyzes the word frequencies in a book downloaded from
	Project Gutenberg """

import string
import re
from collections import Counter

def get_word_list(file_name):
    f = open(file_name,'r')
    lines = f.readlines()
    punct = "[!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]"
    lineswithoutpunct = ""
    curr_line = 0
    while lines[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
        curr_line += 1
    lines = lines[curr_line+1:]
    for line in lines:                                        #does each line seperately
		removepunct = re.sub(punct,"", line)                  #removes all punctuation
		lineswithoutpunct += re.sub("\n", " ", removepunct)   # changes new lines into spaces
    return lineswithoutpunct.split()                          # returns as a list


def get_top_n_words(word_list, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_list: a list of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequentlyoccurring
	"""

	words_to_count = (word for word in word_list if word[:1].isupper())
	c = Counter(words_to_count)
	return c.most_common(n)
                            # source:  http://stackoverflow.com/users/61974/mark-byers 
                            # at http://stackoverflow.com/questions/3594514/how-to-find-most-common-elements-of-a-list

#print get_word_list("book.txt")
print get_top_n_words(get_word_list("book.txt"), 100)