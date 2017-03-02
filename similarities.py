# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 17:17:40 2017

Calculates various similarity measures for sentence pairs.

@author: Adam Varga
"""

import sys
from collections import defaultdict as ddict
import math
import unicodedata
import string

def read_lfs(infile):
    
    with open(infile, 'r') as source:
        lines = source.readlines()
        
    statdict = ddict(lambda: ddict(lambda: ddict(lambda: None)))
    
    for line in lines:
        try:
            [lang1, lang2] = line.strip().split('//')[1].split('-')
            mean = float(line.strip().split(',')[0][1:6])
            sd = float(line.strip().split(',')[1][1:6])
            statdict[lang1][lang2]['m'] = mean
            statdict[lang1][lang2]['sd'] = sd
        except IndexError:
            continue
            
    return statdict

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
   
def cosine_sim(dictionary):
    
    cosine_sim = 0
    for value in dictionary.values():
        cosine_sim += value[0] * value[1]

    length1 = sum([value[0] ** 2 for value in dictionary.values()]) 
    length2 = sum([value[1] ** 2 for value in dictionary.values()])
    
    try:            
        cosine_sim /= math.sqrt(length1) * math.sqrt(length2)
    except ZeroDivisionError:
        cosine_sim = None
        
    return cosine_sim

def char_ngram(line1, line2, n=2):
    
    ngramdict = ddict(lambda: ddict(lambda: 0))
    line_pair = [line1, line2]
    
    for i, line in enumerate(line_pair):
        line = ''.join(line.split())
        j = 0
        while (j + (n - 1)) < len(line):
            ngramdict[line[j:j+n]][i] += 1
            j += 1
    
    return cosine_sim(ngramdict)
   

def cognate(line1, line2):
    
    cognatedict = ddict(lambda: ddict(lambda: 0))
    line_pair = [line1, line2]
    
    for i, line in enumerate(line_pair):
        for word in line.split():
            if word.isdigit():
                cognatedict[word][i] += 1
            elif len(word) >= 4:
                cognatedict[strip_accents(word[:4])][i] += 1
            elif len(word) == 1 and word in string.punctuation:
                cognatedict[word][i] += 1

    return cosine_sim(cognatedict)

def lf(line1, line2, lang1, lang2, sdict):

    return math.exp(-.5*((((len(line2)/len(line1))-sdict[lang1][lang2]['m'])/sdict[lang1][lang2]['sd']))**2)
      
def context_vector(infile1, infile2, context_vectors, outfile):
   
    pass
            
def calculate(infile1, infile2, sdict, outfile, n=2):
    
    ngram_cosine_sims = ddict(lambda: [])
    cognate_cosine_sims = []
    lfs = []
    tokens = []
    chars = []
    
    lang1 = infile1.split('.')[-2]
    lang2 = infile2.split('.')[-2]
    
    with open(infile1, 'r') as source1, open(infile2, 'r') as source2:
        while True:
            try:
                line1 = next(source1)
                line2 = next(source2)
                for n in range(2,6):
                    ngram_cosine_sims[n].append(char_ngram(line1, line2, n))   
                cognate_cosine_sims.append(cognate(line1, line2))
                lfs.append(lf(line1, line2, lang1, lang2, sdict))
                tokens.append((len(line1.split()), len(line2.split())))
                sum([len(word) for word in line1.split()])
                chars.append((sum([len(word) for word in line1.split()]), sum([len(word) for word in line2.split()])))
            
            except StopIteration:
                break
            
    return ngram_cosine_sims, cognate_cosine_sims, lfs, tokens, chars
if __name__ == '__main__':
    
    infile1 = sys.argv[1]
    infile2 = sys.argv[2]
    
    sdict = read_lfs(sys.argv[3])

    ngram_cosine_sims, cognate_cosine_sims, lfs, tokens, chars = calculate(sys.argv[1], sys.argv[2], sdict, sys.argv[4])
    print(cognate_cosine_sims)