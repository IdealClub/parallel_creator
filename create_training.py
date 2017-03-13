# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 09:57:48 2017

@author: vurga
"""

import sys
import numpy as np
from collections import defaultdict as ddict

## Convert string codes to line nos
def code2index(code):
    return int(code.split('-')[1]) - 1

with open(sys.argv[1]+'.train', 'w'), open(sys.argv[2]+'.train', 'w'):
    pass

with open(sys.argv[1], 'r') as source1, open(sys.argv[2], 'r') as source2, open(sys.argv[3],'r') as source3:
    lines1 = source1.readlines()
    lines2 = source2.readlines()
    lines_gold = source3.readlines()

## Create matching dictionary    
matching = ddict(lambda: ddict(lambda: None))
for line in lines_gold:
    [code1, code2] = line.strip().split()
    index1 = code2index(code1)
    index2 = code2index(code2)
    matching[index1] = index2
    
for key, value in matching.items():   
    with open(sys.argv[1]+'.train', 'a+') as target1, open(sys.argv[2]+'.train', 'a+') as target2:
        target1.write(' '.join(lines1[key].split()[1:])+'\n')
        target2.write(' '.join(lines2[value].split()[1:])+'\n')

for i in range(0, len(lines_gold)):
    
    index1 = np.random.randint(0, len(lines1))
    index2 = np.random.randint(0, len(lines2))
    while matching[index1] == index2:
        index1 = np.random.randint(0, len(lines1))
        index2 = np.random.randint(0, len(lines2))
    
    with open(sys.argv[1]+'.train', 'a+') as target1, open(sys.argv[2]+'.train', 'a+') as target2:
        target1.write(' '.join(lines1[index1].split()[1:])+'\n')
        target2.write(' '-join(lines2[index2].split()[1:])+'\n')
    
    