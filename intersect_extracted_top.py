# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 09:42:56 2017

Args: file1 file2 file3 output

@author: vurga
"""

import sys

with open(sys.argv[4], 'w'):
    pass

with open(sys.argv[1], 'r') as source:
    lines_1 = source.readlines()
    
s1 = set()
for line in lines_1:
    article = line.strip().split()[0]
    sentA = line.strip().split()[1]
    sentB = line.strip().split()[2]
    partition = line.strip().split()[-1]
    s1.add((article, sentA, sentB, partition))
    
with open(sys.argv[2], 'r') as source:
    lines_2 = source.readlines()
    
s2 = set()
for line in lines_2:
    article = line.strip().split()[0]
    sentA = line.strip().split()[1]
    sentB = line.strip().split()[2]
    partition = line.strip().split()[-1]
    s2.add((article, sentA, sentB, partition))
    
with open(sys.argv[3], 'r') as source:
    lines_3 = source.readlines()
    
s3 = set()
for line in lines_3:
    article = line.strip().split()[0]
    sentA = line.strip().split()[1]
    sentB = line.strip().split()[2]
    partition = line.strip().split()[-1]
    s3.add((article, sentA, sentB, partition))
    
intersect = s1 & s2 & s3

for element in intersect:
    with open(sys.argv[4], 'a+') as target:
        target.write(' '.join(element))
        