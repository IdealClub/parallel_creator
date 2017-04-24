# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 17:25:40 2017

@author: vurga
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 10:34:32 2017

Args: corpusA corpusB ctxA ctxB classifier

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

with open(sys.argv[4]+'.class', 'w'):
    pass

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
    return math.exp(-.5*((((len(line2)/len(line1))-.914)/0.313))**2)
      

def extract_fea(tA, tB, l):
    
    ngram_cosine_sims = {}
    for n in range(2,6):
        ngram_cosine_sims[n] = char_ngram(tA, tB, n) 
    
    cognate_cosine_sims = cognate(tA, tB)
    #lfs = lf(tA, tB)
    tokens = (len(tA.split()), len(tB.split()))
    chars=(sum([len(word) for word in tA.split()]), sum([len(word) for word in tB.split()]))
    
    return np.array([ngram_cosine_sims[2], ngram_cosine_sims[3], ngram_cosine_sims[4], ngram_cosine_sims[5], chars[0], chars[1], cognate_cosine_sims, l, tokens[0], tokens[1]])

    
with open(sys.argv[1], 'r') as corpusA, open(sys.argv[2]) as corpusB, open(sys.argv[3]) as ctxA, open(sys.argv[4]) as ctxB:

    with open(sys.argv[5], 'rb') as fid:
        model = pickle.load(fid)
        
    while True:
        try:
            textA = next(corpusA)
            textB = next(corpusB)
            contxA = next(ctxA)
            contxB = next(ctxB)
            
            l = lf(textA, textB)
            if l > .6329 and l < 1.0393:
                cvec_1 = np.fromstring(contxA.strip(), sep=" ")
                cvec_2 = np.fromstring(contxB.strip(), sep=" ")
                sim = cosine_similarity(cvec_1, cvec_2)
                feas = extract_fea(textA, textB, l)
                feas_c = np.append(feas, sim)
                
                try:
                    pred = model.predict(feas_c)
                    with open(sys.argv[4]+'.class', 'a+') as target:
                        target.write(str(pred)+'\n')
                except:
                    continue
                
        except StopIteration:
            break
        
       
        
       
