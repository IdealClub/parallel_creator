# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 11:07:31 2017

@author: vurga
"""
import sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

with open(sys.argv[3], 'w'):
    pass

with open(sys.argv[1], 'r') as source_1, open(sys.argv[2], 'r') as source_2:
    while True:
        try:
            line_1 = next(source_1)
            line_2 = next(source_2)
            cvec_1 = np.fromstring(line_1.strip(), sep=" ")
            cvec_2 = np.fromstring(line_2.strip(), sep=" ")
            sim = cosine_similarity(cvec_1, cvec_2)
            
            with open(sys.argv[3], 'a+') as target:
                target.write(str(sim[0][0])+'\n')
        except StopIteration:
            break