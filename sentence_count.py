# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 08:49:05 2017

Count sentences of pseudo-parallel corpora

@author: Adam Varga
"""

import sys

with open(sys.argv[1], 'r') as source:
    lines_1 = source.readlines()
with open(sys.argv[2], 'r') as source:
    lines_2 = source.readlines()    
    
zeros_passed = False
count_1 = 0
count_2 = 0
last_j = 0
for i, line_1 in enumerate(lines_1):
    if int(line_1.strip()) == 0 and zeros_passed:
        count_1 += int(lines_1[i-1].strip()) + 1
        max_2 = 0
        for line_2 in lines_2[last_j:i]:
            if int(line_2.strip()) == 0 and max_2 != 0:
                break
            if int(line_2.strip()) > max_2:
                max_2 = int(line_2.strip())
        last_j = i
        count_2 += max_2 + 1
        zeros_passed = False
    if int(line_1.strip()) != 0:
        zeros_passed = True
        
## last block
count_1 += int(lines_1[:-1].strip()) + 1
max_2 = 0
for line_2 in lines_2[last_j:]:
    if int(line_2.strip()) == 0 and max_2 != 0:
        break
    if int(line_2.strip()) > max_2:
        max_2 = int(line_2.strip())
count_2 += max_2 + 1

        
print("Sentence count 1: "+str(count_1)+'\n')
print("Sentence count 2: "+str(count_2)+'\n')
