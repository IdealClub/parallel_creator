# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:43:01 2017

@author: vurga
"""

import pandas as pd, numpy as np
import sys
from sklearn.utils import shuffle
from sklearn.cross_validation import KFold
from sklearn import svm, ensemble, metrics, linear_model
import pickle


def read_data(filename):
    # Read csv to pandas dataframe
    return pd.read_csv(filename, index_col=0, low_memory=False)

def train_and_xval(df, a="svm"):
    
    to_excl = ['label']
    predictors = training_data.columns.difference(to_excl)
    
    if a == "gb":
        alg = ensemble.GradientBoostingRegressor()
    else:
        alg = svm.SVR()
        
    print('Training Model: '+a)
 
    ## train on whole data 
    alg.fit(df[predictors], df['label'])
    
    return alg
    
def vote(classifiers, data):
    
    to_excl = ['label']
    predictors = training_data.columns.difference(to_excl)
   
    predictor_features = []
    for i, classifier in enumerate(classifiers):
        y = pd.DataFrame(classifier.predict(data[predictors]))
        predictor_features.append(y)
    
    dev_data = pd.concat(predictor_features, axis=1, ignore_index=True)
    ens = linear_model.LinearRegression()
    ens.fit(dev_data, data['label'])
    
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
    

    training_portion = int(len(training_data) * 0.875)
    test_portion = int(len(training_data) * 0.025)
    ensemble_portion = int(len(training_data) * 0.1)
    training_data = shuffle(training_data, random_state=3)
    
    sv = train_and_xval(training_data[:training_portion], a="svm")
    gb = train_and_xval(training_data[:training_portion], a="gb")
    
    ens = vote([sv, gb], training_data[-ensemble_portion:])
    
    with open('sv_regression.pkl', 'wb') as fid:
        pickle.dump(sv, fid) 
    with open('gb_regression.pkl', 'wb') as fid:
        pickle.dump(gb, fid) 
    with open('regression_ensemble.pkl', 'wb') as fid:
        pickle.dump(ens, fid)     
    
        