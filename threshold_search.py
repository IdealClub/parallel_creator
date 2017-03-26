# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 14:39:43 2017

@author: vurga
"""

import sys

def check_acc(th, feas, labels):
    
    guesses = []
    for i, fea in enumerate(feas):
        if fea < th and labels[i] == 0:
            guesses.append(1)
        elif fea >= th and labels[i] == 1:
            guesses.append(1)
        else:
            guesses.append(0)
            
    return sum(guesses) / len(guesses)
def find_best_threshold(feas, labels, step=0.005):
    
    positive = []
    negative = []
    for i, fea in enumerate(feas):
        if labels[i] == 1:
            positive.append(fea)
        else:
            negative.append(fea)
    
    minpos = min(positive)
    maxneg = max(negative)
    
    if minpos > maxneg:
        return (minpos + maxneg) / 2
    else:
        th = minpos
        accs = {}
        while th <= maxneg:
            acc = check_acc(th, feas, labels)
            accs[th] = acc
            print(th, acc)
            th += step
            if th > maxneg:
                acc = check_acc(maxneg, feas, labels)
                accs[maxneg] = acc
                print(maxneg, acc)
                
        return sorted(accs, key=accs.get, reverse=True)[0]

if __name__ == '__main__':

    alllines = []
    labels = []
    for f in sys.argv[1:]:
        with open(f, 'r') as source:
            lines = source.readlines()
            alllines += lines
            for i in range(int(len(lines)/2)):
                labels.append(1)
            for i in range(int(len(lines)/2)):
                labels.append(0)
                
    cosine_sims = []
    for line in alllines:
        cosine_sims.append(float(line.strip()))
    
    th=find_best_threshold(cosine_sims, labels)
    print(th)