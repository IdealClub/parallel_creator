# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 10:26:07 2017

@author: vurga
"""

import sys

with open(sys.argv[1]+'.dist', 'w') as target:
    target.write(",dist\n")
with open(sys.argv[1], 'r') as source:
    lines = source.readlines()
    
distances = []
for line in lines:
    num_lines_source = int(line.strip().split()[0])
    num_lines_target = int(line.strip().split()[1])
    
    ind = 0
    for i in range(0, num_lines_source):
        for j in range(0, num_lines_target):
            distances.append(str(ind)+","+str(abs(i-j)))
            ind += 1

with open(sys.argv[1]+'.dist', 'a+') as target:
    target.write('\n'.join(distances))
            

