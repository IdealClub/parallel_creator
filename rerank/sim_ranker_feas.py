# -*- coding: utf-8 -*-
"""
Created on Fri May  5 11:20:41 2017

Similarity ranker on pre-computed features

args: feas

@author: vurga
"""

import sys

with open(sys.argv[1], 'r') as source:
    lines = source.readlines()
with open(sys.argv[1]+'.srank', 'w'):
    pass
    
for line in lines:
    n1 = float(line.strip().split()[1])
    n2 = float(line.strip().split()[2])
    n3 = float(line.strip().split()[3])
    n4 = float(line.strip().split()[4])
    cog = float(line.strip().split()[7])
    ctx = float(line.strip().split()[11])
    
    score = (n1 + n2 + n3 + n4 + cog + ctx) / 6
    with open(sys.argv[1]+'.srank', 'a+') as target:
        target.write(str(score)+'\n')