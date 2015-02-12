# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014
@author: Logan Sweet
"""
# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

def get_complement(nucleotide):
    """ Returns the complementary nucleotide
        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
        ####two additional doctests added to ensure that all 4 pairs are tested
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    >>> get_complement('T') 
    'A'
    >>> get_complement('G')
    'C'
    """
    if nucleotide == 'A' :  #relpaces A with T
        return 'T' 
    if nucleotide == 'T' :  #replaces T with A
        return 'A' 
    if nucleotide == 'G' :  #replaces G with C
        return 'C' 
    if nucleotide == 'C' :  #replaces C with G
        return 'G' 

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
        #####No added unit tests since all inputted dna strings will follow this form 
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    index = len(dna)                                   #sets index at # of nucleotides
    reverse = dna[::-1]                                #reverses dna order
    revcomp  = ''                                      # creates an empty string called revcomp
    for n in reverse : 
        revcomp = revcomp + get_complement(n)          #assigns each new compliment to the string revcomp
    return revcomp
        
def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        Stop codons: TAG, TAA, TGA
        returns: the open reading frame represented as a string
    #######    I added an additional unit test for third stop codon
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    >>> rest_of_ORF("ATGTTATAA")
    'ATGTTA'
    >>> rest_of_ORF('ATGCATGAATGTTAG')
    'ATGCATGAATGT'
    """
    length = len(dna)
    n = 0
    stopcod = ['TAG' , 'TAA', 'TGA']
    while n < (length) :           #does not go all the way to avoid running out of sets of 3
        if dna[n:n+3] in stopcod :
            return dna[:n]          
        else :
            n = n+3
    if n == (length - 2):          #if you reach the last group of three and it is not a stop, end the loop
        return dna
    return dna


def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.    

        returns: a list of non-nested ORFs

        ############no added unit tests: these had open reading frames in multiple reference frames

    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    """
    length = len(dna)  
    n = 0
    thing = []
    startcod = 'ATG'  
    while n < length-2:
        if startcod in dna[n:n+3]: 
            found_orf = rest_of_ORF(dna[n:])
            thing.append(found_orf)
            n = n + len(found_orf)
        else :
            n += 3
    return thing

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
         possible frames and returns them as a list.  By non-nested we mean that if an
         ORF occurs entirely within another ORF and they are both in the same frame,
         it should not be included in the returned list of ORFs.

         returns: a list of non-nested ORFs
         ##########added another unit test that did not begin with ATG
    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """

    orfs = []
    orfs += (find_all_ORFs_oneframe(dna[0:]))
    orfs += (find_all_ORFs_oneframe(dna[1:]))
    orfs += (find_all_ORFs_oneframe(dna[2:]))
    return orfs

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
       strands.
       returns: a list of non-nested ORFs
       ####no additional unit tests: ones provided had ATG in both directions
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
  """
    orfs = []
    for i in find_all_ORFs(dna):
        orfs.append(i)
    for i in find_all_ORFs(get_reverse_complement(dna)):
        orfs.append(i)
    return orfs


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
  """
    longorf = ''
    for element in (find_all_ORFs_both_strands(dna)):
        if len(element) > len(longorf): 
            longorf = element
    return longorf

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    length = 0
    for n in range (0 , num_trials) :
        shuff_dna = shuffle_string(dna)
        if len(longest_ORF(shuff_dna)) > length : 
            length = len(longest_ORF(shuff_dna))
    return length

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
        input DNA fragment
    >>> coding_strand_to_AA("ATGCGA")
    'MR'
    >>> coding_strand_to_AA("ATGCCCGCTTT")
    'MPA'
  """
    
    acidlist = ''
    for n in range (0,len(dna)-2,3):
        amino = dna[n] + dna [n+1] + dna[n+2]
        amino_acid = aa_table[amino]
        acidlist = acidlist + amino_acid 
    return acidlist

def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        returns: a list of all amino acid sequences coded by the sequence dna.
  """
    gene = []
    threshold = longest_ORF_noncoding(dna,1500)
    print threshold                           ##########################################################
    for element in find_all_ORFs_both_strands(dna):
        if len(element) > threshold:
            # print element
            gene.append(coding_strand_to_AA(element))
    return gene


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    dna = load_seq("./data/X73525.fa")
    genes = gene_finder(dna)
    print len(genes)
    print genes

    #print get_complement('C')
    #print get_reverse_complement('AAG')
    #print rest_of_ORF('ATGTCATAA')
    #print find_all_ORFs_oneframe('ATGCATGAATGTAGATAGATGTGCCC')
    #print find_all_ORFs_both_strands(dna)


    #print find_all_ORFs('ATGCATGAATGTAG')
    #print rest_of_ORF

