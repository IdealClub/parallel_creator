# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 18:20:13 2017

args: corpusA corpusB no splits

@author: vurga
"""

import sys

## get number of splits
n = int(sys.argv[6])

for i in range(n):
    with open(sys.argv[1]+str(i), 'w'), open(sys.argv[2]+str(i), 'w'):
        pass


## split no files accordingly
with open(sys.argv[5], 'r') as source:
    nos = source.readlines()

split_size = int(len(nos) / n) + 1
a_start = 0
b_start = 0
for i in range(n):
    no_start = i * split_size
    if no_start+split_size < len(nos):
        no_part = nos[no_start:no_start+split_size]
    else:
        no_part = nos[no_start:]   

    a_next = 0
    b_next = 0
    for no in no_part:
        a_next += int(no.strip().split()[0])
        b_next += int(no.strip().split()[1])
        
    with open(sys.argv[1], 'r') as corpusA, open(sys.argv[2], 'r') as corpusB:
        for j in range(a_start):
            next(corpusA)
        for j in range(b_start):
            next(corpusB)
        for j in range(a_next):
            line = next(corpusA)
            with open(sys.argv[1]+str(i), 'a+') as target:
                target.write(line)
                
        for j in range(b_next):
            line = next(corpusB)
            with open(sys.argv[2]+str(i), 'a+') as target:
                target.write(line)

    a_start += a_next
    b_start += b_next
            