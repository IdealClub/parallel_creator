# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 13:12:00 2017

args: corpusA corpusB nos matches

@author: vurga
"""

import sys

with open(sys.argv[4]+'.a', 'w'), open(sys.argv[4]+'.b', 'w'):
    pass

with open(sys.argv[3], 'r') as source:
    nos = source.readlines()
with open(sys.argv[1], 'r') as source:
    corpusA = source.readlines()
with open(sys.argv[2], 'r') as source:
    corpusB = source.readlines()
with open(sys.argv[4], 'r') as source:
    matches = source.readlines()
    
lengthsA = []
lengthsB = []
for no in nos:
    lengthsA.append(int(no.strip().split()[0]))
    lengthsB.append(int(no.strip().split()[1]))
    
for match in matches:
    article = int(match.strip().split()[0])
    sntA = int(match.strip().split()[1])
    sntB = int(match.strip().split()[2])
    
    startA = sum(lengthsA[:article])
    startB = sum(lengthsB[:article])
    
    with open(sys.argv[4]+'.a', 'a+') as target:
        target.write(corpusA[startA+sntA])
    with open(sys.argv[4]+'.b', 'a+') as target:
        target.write(corpusB[startB+sntB])
        