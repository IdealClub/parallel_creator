# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 18:20:13 2017

args: corpusA corpusB contextA contextB no splits

@author: vurga
"""

import sys

## get number of splits
n = int(sys.argv[6])

for i in range(n):
    with open(sys.argv[5]+str(i), 'w'), open(sys.argv[1]+str(i), 'w'), open(sys.argv[2]+str(i), 'w'), open(sys.argv[3]+str(i), 'w'), open(sys.argv[4]+str(i), 'w'):
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
    with open(sys.argv[5]+str(i), 'a+') as target:
        target.write(''.join(no_part))

    a_next = 0
    b_next = 0
    for no in no_part:
        a_next += int(no.strip().split()[0])
        b_next += int(no.strip().split()[1])
        
    with open(sys.argv[1]) as corpusA, open(sys.argv[2]) as corpusB, open(sys.argv[3]) as contextA, open(sys.argv[4]) as contextB:
        for j in range(a_start):
            #print('skipping', j)
            next(corpusA)
            next(contextA)
        for j in range(b_start):
            #print('skipping', j)
            next(corpusB)
            next(contextB)
        for j in range(a_next):
            #print('a', j)
            line = next(corpusA)
            cnx = next(contextA)
            #print(line)
            with open(sys.argv[1]+str(i), 'a+') as target:
                target.write(line)
            with open(sys.argv[3]+str(i), 'a+') as target:
                target.write(cnx)
                
        for j in range(b_next):
            #print('b',j)
            line = next(corpusB)
            cnx = next(contextB)
            #print(line)
            with open(sys.argv[2]+str(i), 'a+') as target:
                target.write(line)
            with open(sys.argv[4]+str(i), 'a+') as target:
                target.write(cnx)
                
    a_start += a_next
    b_start += b_next
            