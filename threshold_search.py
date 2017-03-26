# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 14:39:43 2017

@author: vurga
"""

import sys
from sklearn.cross_validation import KFold
import numpy as np
from sklearn.utils import shuffle
from sklearn import metrics

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
            #print(th, acc)
            th += step
            if th > maxneg:
                acc = check_acc(maxneg, feas, labels)
                accs[maxneg] = acc
                #print(maxneg, acc)
                
        return sorted(accs, key=accs.get, reverse=True)[0]
    
def train_and_xval(X):
    
    # 10-fold cross-validation
    kf = KFold(X.shape[0], n_folds=10, random_state=1)
    # train folds
    predictions = []
    ths = []
    for train, test in kf:
        train_predictors = X[train][:,0]
        train_target = X[train][:,1]
        th = find_best_threshold(train_predictors, train_target)
        test_predictions = []
        ths.append(th)
        for test_instance in X[test]:
            if test_instance[0] < th:
                test_predictions.append(0)
            else:
                test_predictions.append(1)
        predictions.append(test_predictions)
    # concatenate fold
    predictions = np.concatenate(predictions, axis=0)
    
    print('CV scores')
    print('confusion matrix')
    print(metrics.confusion_matrix(X[:,1], predictions))
    print('Pr')
    print(metrics.precision_score(X[:,1], predictions))
    print('Re')
    print(metrics.recall_score(X[:,1], predictions))
    
    ## train on whole data set
    th = find_best_threshold(X[:,0], X[:,1])
    return th

def test(X, th):
    
    test_predictions = []
    for test_instance in X:
        if test_instance[0] < th:
            test_predictions.append(0)
        else:
            test_predictions.append(1)
    
    print('Test scores')
    print('confusion matrix')
    print(metrics.confusion_matrix(X[:,1], test_predictions))
    print('Pr')
    print(metrics.precision_score(X[:,1], test_predictions))
    print('Re')
    print(metrics.recall_score(X[:,1], test_predictions))

    return test_predictions        
    

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
        
    feas = np.array(cosine_sims)
    labels = np.array(labels)
    
    X = np.column_stack((feas, labels))
    X = shuffle(X, random_state=2)
    
    th=train_and_xval(X[:32666])
    print(th)
    
    preds = test(X[32666:33599], th)