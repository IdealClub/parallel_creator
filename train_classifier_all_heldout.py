# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:43:01 2017

@author: vurga
"""

import pandas as pd, numpy as np
import sys
from sklearn.utils import shuffle
from sklearn.cross_validation import KFold
from sklearn import svm, ensemble, metrics
import pickle


def read_data(filename):
    # Read csv to pandas dataframe
    return pd.read_csv(filename, index_col=0, low_memory=False)

def train_full(df, a="svm"):
    
    to_excl = ['label']
    predictors = df.columns.difference(to_excl)
    
    if a == "gb":
        alg = ensemble.GradientBoostingClassifier()
    else:
        alg = svm.SVC(probability=True)
        
    print('Model: '+a)
    

    ## train on whole data 
    alg.fit(df[predictors], df['label'])

    return alg

def test(alg, test_set):
    
    to_excl = ['label']
    predictors = test_set.columns.difference(to_excl)
    
    test_predictions = alg.predict(test_set[predictors])
    
    print('test scores')
    print('confusion matrix')
    print(metrics.confusion_matrix(test_set['label'], test_predictions))
    print('Pr')
    print(metrics.precision_score(test_set['label'], test_predictions))
    print('Re')
    print(metrics.recall_score(test_set['label'], test_predictions))
    

def vote(classifiers, data):
    
    to_excl = ['label']
    predictors = data.columns.difference(to_excl)
    
    ens = ensemble.VotingClassifier(estimators=classifiers, voting='soft')
    ens = ens.fit(data[predictors], data['label'])
    
    test_predictions = ens.predict(data[predictors])
    
    print('ensemble scores')
    print('confusion matrix')
    print(metrics.confusion_matrix(data['label'], test_predictions))
    print('Pr')
    print(metrics.precision_score(data['label'], test_predictions))
    print('Re')
    print(metrics.recall_score(data['label'], test_predictions))
    
    return ens

if __name__ == '__main__':
    
    features = []
    labels = []
    for arg in sys.argv[1:3]:
        X = read_data(arg)
        pos = np.repeat(1, len(X)/2)
        neg = np.repeat(0, len(X)/2)
        y = pd.DataFrame(np.concatenate((pos, neg)))
        features.append(X)
        labels.append(y)
        
    train_instances = pd.concat(features, ignore_index=True)
    train_labels = pd.concat(labels, ignore_index=True)
    train_labels.columns = ['label']
    training_data = pd.concat((train_instances, train_labels), axis=1)
    
    ## read context vector similarities
    cs = []
    for arg in sys.argv[3:]:
        C = pd.read_csv(arg, header=None)
        cs.append(C)
        
    cosine_sims = pd.concat(cs, ignore_index=True)
    cosine_sims.columns = ['context-500k']
    training_data = pd.concat((training_data, cosine_sims), axis=1)
    
    training_data = shuffle(training_data, random_state=3)
    sv = train_full(training_data[:32666], a="svm")
    #test(sv, training_data[32666:33599])
    gb = train_full(training_data[:32666], a="gb")
    #test(gb, training_data[32666:33599])
    
    ens = vote([('svm',sv),('gradboost',gb)], training_data[33599:])
    #test(ens, training_data[32666:33599])
    
    # save the classifier
    with open('all_ensemble.pkl', 'wb') as fid:
        pickle.dump(ens, fid)     
        
        