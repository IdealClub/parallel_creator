# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 14:04:06 2017

@author: vurga
"""

import sys
from collections import defaultdict as ddict
import math
import unicodedata
import string

def lf(line1, line2):

    return math.exp(-.5*((((len(line2)/len(line1))-1.133)/.415))**2)


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


with open(sys.argv[1], 'r') as source:
    s_lines = source.readlines()
with open(sys.argv[2], 'r') as source:
    t_lines = source.readlines()
k = int(sys.argv[3])
with open(sys.argv[4], 'w'):
    pass

for i, s_line in enumerate(s_lines):
    for j in range(k):
        s_line = s_line.strip()
        t_line = t_lines[i*k+j].strip()
        
        g2 = char_ngram(s_line, t_line, 2)
        g3 = char_ngram(s_line, t_line, 3)
        g4= char_ngram(s_line, t_line, 4)
        g5 = char_ngram(s_line, t_line, 5)
        cg = cognate(s_line, t_line)
        l = lf(s_line, t_line)
        try:
            av = l * ((g2 + g3 + g4 + g5 + cg) / 5)
        except:
            av = 0.0
        with open(sys.argv[4], 'a+') as target:
            try:
                target.write(str(g2)+' '+str(g3)+' '+str(g4)+' '+str(g5)+' '+str(cg)+' '+str(l)+' '+str(av)+' \n')
            except:
                target.write('0 0 0 0 0 0 0 \n') 
        
    

    