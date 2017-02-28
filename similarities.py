# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 17:17:40 2017

Calculates various similarity measures for sentence pairs.

@author: Adam Varga
"""

import sys
from collection import defaultdict as ddict
import math
import re
import unicodedata
import string

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
   
def cosine_sim(dictionary):
    
    cosine_sim = 0
    for value in dictionary.values():
        if value[1] and value[2]:
            cosine_sim += 1

    length1 = sum([value[1] for value in dictionary.values()]) 
    length2 = sum([value[2] for value in dictionary.values()])
    cosine_sim /= math.sqrt(length1) * math.sqrt(length2)

    return cosine_sim

def char_ngram(line1, line2, n=2):
    
    ngramdict = ddict(lambda: ddict(lambda: 0))
    for word in line1.split():
        if len(word) >= n:
            j = 0
            while (j + (n - 1)) < len(word):
                ngramdict[word[j:j+n]][1] = 1
    for word in line2.split():
        if len(word) >= n:
            j = 0
            while (j + (n - 1)) < len(word):
                ngramdict[word[j:j+n]][2] = 1
    
    return cosine_sim(ngramdict)
   

def cognate(line1, line2):
    
    cognatedict = ddict(lambda: ddict(lambda: 0))
    for word in line1.split():
        if re.search(r'\d', word):
            cognatedict[word][1] == 1
        elif len(word) >= 4:
            cognatedict[strip_accents(word[:4])][1] == 1
        elif len(word) == 1 and word in string.punctuation:
            cognatedict[word][1] == 1
    for word in line2.split():
        if re.search(r'\d', word):
            cognatedict[word][2] == 1
        elif len(word) >= 4:
            cognatedict[strip_accents(word[:4])][2] == 1
        elif len(word) == 1 and word in string.punctuation:
            cognatedict[word][2] == 1
    
    return cosine_sim(cognatedict)
        
def context_vector(infile1, infile2, context_vectors, outfile):
   
    pass
            
def calculate(infile1, infile2, outfile, n=2):
    
    ngram_cosine_sims = []
    cognate_cosine_sims = []
    lfs = []
    tokens = []
    chars = []
    with open(infile1, 'r') as source1:
        for i, line1 in enumerate(source1):
            with open(infile2, 'r') as  source2:
                line2 = source2[i]
            ngram_cosine_sims.append(char_ngram(line1, line2, n))   
            cognate_cosine_sims.append(cognate(line1, line2))
            lfs.append(len(line1.split())/len(line2.split()))
            tokens.append((len(line1.split()), len(line2.split())))
            sum([len(word) for word in line1.split])
            chars.append((sum([len(word) for word in line1.split]), sum([len(word) for word in line2.split])))
            
    return ngram_cosine_sims, cognate_cosine_sims, lfs, tokens, chars
if __name__ == '__main__':
    
    infile1 = sys.argv[1]
    infile2 = sys.argv[2]

    ngram_cosine_sims, cognate_cosine_sims, lfs, tokens, chars = calculate(sys.argv[1], sys.argv[2], sys.argv[3])