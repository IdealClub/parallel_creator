# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 11:46:57 2017

Aligns sentence from one article  with every sentence from the paired artice.

Usage: python multiply_sentences.py <source> <target> <sentence counts>

@author: Adam Varga
"""

import sys

with open(sys.argv[1]) as source:
    sources = source.readlines()
with open(sys.argv[2]) as source:
    targets = source.readlines()
with open(sys.argv[3]) as source:
    nos = source.readlines()
    
with open(sys.argv[1]+".al", "w"):
    pass
with open(sys.argv[2]+".al", "w"):
    pass
  
source_start = 0
target_start = 0

for num in nos:
    source_aligned = []
    target_aligned = []
    source_nos = int(num.strip.split()[0])
    target_nos = int(num.strip.split()[1])
    for source in sources[source_start:source_start+source_nos]:
        for i in range(target_start, target_start+target_nos):
            source_aligned.append(source)
            target_aligned.append(targets[i])
    source_start += source_nos
    target_start += target_nos
    with open(sys.argv[1]+".al", "a+") as t:
        t.write("".join(source_aligned))
    with open(sys.argv[2]+".al", "a+") as t:
        t.write("".join(target_aligned))