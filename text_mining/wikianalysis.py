""" MiniProject 3: Text Mining and Analysis


 """

#import random
#import math
from pattern.web import Wikipedia

# def a():
#     """ What it does 
#         what each variable is 

#     """
#     from pattern.web import *
#     w = Wikipedia()
#     for article_title in w.index():
#         print article_title

# def b():
#     """ What it does 
#         what each variable is 

#     """
#     from pattern.web import *
#     w = Wikipedia()
#     olin_article = w.search('Olin College')
#     print olin_article.sections


# def c():
#     from pattern.en import *      #first part: sentiment || second part: subjectivity
#     print sentiment('Software Design is not my favorite class!')    

def d():
    dalist = [] 
    article = Wikipedia().search('List of horror fiction writers')
    for section in article.links:
        dalist.append(section)
    print dalist
    

if __name__ == '__main__':
    print d()

