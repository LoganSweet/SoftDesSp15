""" MiniProject 3: Text Mining and Analysis
    For each run, type the name of a wikipedia article 
    that contains a list of authors. After a very long runtime, 
    an ordered pair will be produced. The first element
    is the sentiment value, and the second element is the 
    subjectivity value. 

 """

from pattern.web import Wikipedia     
from pattern.en import *              # allows it to run sentiment for english


def authors(ArtName):                 # returns list of authors mentioned in that article
    authorlist = [] 
    article = Wikipedia().search(ArtName)  # Searches for the provided article name
    for section in article.links:          
        authorlist.append(section)         # adds each author name to the list
    return authorlist

def listtest(list):
    sent = 0
    subj = 0
    for element in list:
        sent += element[0]               # 0th elemt: sentiment
        subj += element[1]               # 1st element: subjectivity
        sentiment = sent / len(list)     
        subjectivity = subj / len(list)  #gives an average value for each
        return sentiment, subjectivity

def evaluate(ArtName):
    sentimentlist = []
    authorlist = authors(ArtName)
    w = Wikipedia()
    for author in authorlist: 
        article = w.search(author)      #finds article for each author
        sentimentlist.append(sentiment(article.string))  # records the sentiment vanlues
    return listtest(sentimentlist)

if __name__ == '__main__':
    #print evaluate('List of Christian fiction authors')
    print evaluate('List of science fiction authors')
