# -*- coding: utf-8 -*-
"""
Created on Fri May  5 09:38:49 2017

Ranks according to similarities

Args: extraction_file corpusA corpusB ctxA ctxB nos

@author: vurga
"""

import sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict as ddict
import math
import unicodedata
import string
import pandas as pd
import pickle
import re

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

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
   
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

def lf(line1, line2):
    return math.exp(-.5*((((len(line2)/len(line1))-1.133)/0.415))**2)
      

def extract_fea(tA, tB):
    
    ngram_cosine_sims = {}
    for n in range(2,6):
        ngram_cosine_sims[n] = char_ngram(tA, tB, n) 
    
    cognate_cosine_sims = cognate(tA, tB)
    lfs = lf(tA, tB)
    #tokens = (len(tA.split()), len(tB.split()))
    #chars=(sum([len(word) for word in tA.split()]), sum([len(word) for word in tB.split()]))
    
    return np.array([ngram_cosine_sims[2], ngram_cosine_sims[3], ngram_cosine_sims[4], ngram_cosine_sims[5], cognate_cosine_sims, lfs])

with open(sys.argv[1], 'r') as source:
    extractions = source.readlines()
with open(sys.argv[6], 'r') as source:
    nos = source.readlines()

with open(sys.argv[6]+'.srank', 'w'):
     pass

for extraction in extractions:
    article_id = int(extraction.strip().split()[0])
    a_id = int(extraction.strip().split()[1])
    b_id = int(extraction.strip().split()[2])

    index_a = 0
    index_b = 0
    for no in nos:
            for i in range(article_id):
                index_a += int(no.strip().split()[1])
                index_b += int(no.strip().split()[2])
            else:
                index_a += a_id
                index_b += b_id
    
            with open(sys.argv[2], 'r') as corpusA, open(sys.argv[3], 'r') as corpusB, open(sys.argv[4], 'r') as ctxA, open(sys.argv[5], 'r') as ctxB:
                ## get to position
                for i in range(index_a):
                    l_a = next(corpusA)
                    c_a = next(ctxA)
                for i in range(index_b):
                    l_b = next(corpusB)
                    c_b = next(ctxB)
                
            
            ## compute cosine sim
            cvec_1 = np.fromstring(c_a.strip(), sep=" ")
            cvec_2 = np.fromstring(c_b.strip(), sep=" ")
            ## compute cosine sim
            sim = cosine_similarity(cvec_1, cvec_2)
                                
            ## extract all sx feas
            feas = extract_fea(l_a, l_b)
            feas_c = np.append(sim, feas)
            
            with open(sys.argv[6]+'.srank', 'a+') as target:
                score = np.mean(feas_c[:-1]) * feas[-1]
                target.write(str(score) + '\n')
            
        
    