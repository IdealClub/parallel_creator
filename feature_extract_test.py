# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 10:34:32 2017

Args: corpusA corpusB ctxA ctxB nos

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
from sklearn import svm, ensemble

with open(sys.argv[5]+'.csim', 'w'):
    pass
with open(sys.argv[5]+'.ssim', 'w'):
    pass
with open(sys.argv[5]+'.asim', 'w'):
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
    return math.exp(-.5*((((len(line2)/len(line1))-1.133)/0.415))**2)
      

def extract_fea(tA, tB):
    
    ngram_cosine_sims = {}
    for n in range(2,6):
        ngram_cosine_sims[n] = char_ngram(tA, tB, n) 
#    n2 = pd.DataFrame(ngram_cosine_sims[2])
#    n2.columns = ['2-gram-cos']
#    n3 = pd.DataFrame(ngram_cosine_sims[3])
#    n3.columns = ['3-gram-cos']
#    n4 = pd.DataFrame(ngram_cosine_sims[4])
#    n4.columns = ['3-gram-cos']
#    n5 = pd.DataFrame(ngram_cosine_sims[5])
#    n5.columns = ['5-gram-cos']
    
    
    cognate_cosine_sims = cognate(tA, tB)
    lfs = lf(tA, tB)
    tokens = (len(tA.split()), len(tB.split()))
    chars=(sum([len(word) for word in tA.split()]), sum([len(word) for word in tB.split()]))
    #c1 = pd.DataFrame(chars[0])
    #c1.columns = []
    
    return np.array([ngram_cosine_sims[2], ngram_cosine_sims[3], ngram_cosine_sims[4], ngram_cosine_sims[5], chars[0], chars[1], cognate_cosine_sims, lfs, tokens[0], tokens[1]])

with open(sys.argv[5], 'r') as source:
    nos = source.readlines()
    
with open(sys.argv[1], 'r') as corpusA, open(sys.argv[2]) as corpusB, open(sys.argv[3]) as ctxA, open(sys.argv[4]) as ctxB:

    with open('sx_ensemble.pkl', 'rb') as fid:
        e_s = pickle.load(fid)
    with open('all_ensemble.pkl', 'rb') as fid:
        e_a = pickle.load(fid)
    
    for n, num in enumerate(nos):
        source_nos = int(num.strip().split()[0])
        target_nos = int(num.strip().split()[1])
        
        textA = []
        textB = []
        contxA = []
        contxB = []
        
        for i in range(source_nos):
            textA.append(next(corpusA))
            contxA.append(next(ctxA))
        for i in range(target_nos):
            textB.append(next(corpusB))
            contxB.append(next(ctxB))
        
        for i, tA in enumerate(textA):
            for j, tB in enumerate(textB):
                
                r = len(tA.split()) / len(tB.split())
                #if r > 2.0 or r < 0.5:
                #    continue
                #else:
                    ## compute cosine sim
                cvec_1 = np.fromstring(contxA[i].strip(), sep=" ")
                cvec_2 = np.fromstring(contxB[j].strip(), sep=" ")
                sim = cosine_similarity(cvec_1, cvec_2)
                
                if sim > 0.42:
                    with open(sys.argv[5]+'.csim', 'a+') as target:
                        target.write('%d %d %d \n' % (n, i, j))
                        
                ## extract all sx feas
                feas = extract_fea(tA, tB)
                preds = e_s.predict(feas)
                if preds[0] == 1:
                    with open(sys.argv[5]+'.ssim', 'a+') as target:
                        target.write('%d %d %d \n' % (n, i, j))
                
                ## compute cosine sim
                feas = np.append(feas, sim)
                preds = e_a.predict(feas)
                if preds[0] == 1:
                    with open(sys.argv[5]+'.asim', 'a+') as target:
                        target.write('%d %d %d \n' % (n, i, j))
                    
                
    
    