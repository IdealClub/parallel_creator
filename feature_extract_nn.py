
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 10:34:32 2017

Args: corpusA corpusB ctxA ctxB nos model

@author: vurga
"""

import sys
import numpy as np
from keras.models import load_model
import re

with open(sys.argv[5]+'.nnsim', 'w'):
    pass
with open(sys.argv[5], 'r') as source:
    nos = source.readlines()
    
with open(sys.argv[1], 'r') as corpusA, open(sys.argv[2]) as corpusB, open(sys.argv[3]) as ctxA, open(sys.argv[4]) as ctxB:

    model = load_model(sys.argv[6])
    
    for n, num in enumerate(nos):
        source_nos = int(num.strip().split()[0])
        target_nos = int(num.strip().split()[1])
        
        textA = []
        textB = []
        contxA = []
        contxB = []
        
        for i in range(source_nos):
            textA.append(next(corpusA))
            contxA.append(next(ctxA))
        for i in range(target_nos):
            textB.append(next(corpusB))
            contxB.append(next(ctxB))
        
        for i, tA in enumerate(textA):
            for j, tB in enumerate(textB):
                
                lA = len(tA.strip().split())
                lB = len(tB.strip().split())
                if lA == 0 or lB == 0:
                    continue
                r = lA / lB
                if r > 2.0 or r < 0.5 or lA < 4 or lB < 4 or lA > 50 or lB > 50 or re.match('\\\\', tA) or re.match('\\\\', tB):
                    continue
                else:
                    
                    ## compute cosine sim
                    cvec_1 = np.fromstring(contxA[i].strip(), sep=" ")
                    cvec_2 = np.fromstring(contxB[j].strip(), sep=" ")
                    ## compute cosine sim
                    feas_conc = np.concatenate((cvec_1, cvec_2))
                    feas_mult = np.multiply(cvec_1, cvec_2)
                    feas_subt = cvec_1 - cvec_2
                    feas = np.concatenate((feas_conc, feas_mult, feas_subt))
                        
                    if True:
                        pred = model.predict(feas.T)[1]
                        if pred > .5:
                            with open(sys.argv[5]+'.nnsim', 'a+') as target:
                                target.write('%d %d %d %f \n' % (n, i, j, pred))
                                
                        else:
                            continue
                            
                    else:
                        continue
