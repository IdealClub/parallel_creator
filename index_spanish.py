# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 10:34:13 2017

python index_spanish.py <non-unique sentences> <unique sentences> <unique context vectors> <non-unique context vector output>


@author: vurga
"""

import sys

with open(sys.argv[4], 'w'):
    pass

sentence_dict = {}
context_dict = {}
with open(sys.argv[2], 'r') as source_1, open(sys.argv[3], "r") as source_2:
    i = 0
    while True:
        try:
            line_1 = next(source_1)
            line_2 = next(source_2)
            sentence_dict[line_1] = i
            context_dict[i] = line_2
            i += 1
        except StopIteration:
            break

with open(sys.argv[1], 'r') as source:
    while True:
        try:
            line = next(source)
            with open(sys.argv[4], 'a+') as target:
                target.write(context_dict[sentence_dict[line]])
        except KeyError:
            sys.stderr.write('Sentence not found!!')
        except StopIteration:
            break