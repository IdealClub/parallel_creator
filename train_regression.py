# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:43:01 2017

Args: set_feas1 set_feas2 ctx_sim1 ctx_sim2 features(all/set/ctx)

@author: vurga
"""

import pandas as pd, numpy as np
import sys
from sklearn.utils import shuffle
from sklearn import svm, ensemble, metrics, linear_model
import pickle


def read_data(filename):
    # Read csv to pandas dataframe
    return pd.read_csv(filename, index_col=0, low_memory=False)

def train_and_xval(df, a="svm"):
    
    to_excl = ['label']
    if sys.argv[5] == 'all':
        predictors = df.columns.difference(to_excl)
    elif sys.argv[5] == 'set':
        to_excl.append('context-500k')
        predictors = df.columns.difference(to_excl)
    else:
        predictors = ['context-500k']
    
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
    if sys.argv[5] == 'all':
        predictors = data.columns.difference(to_excl)
    elif sys.argv[5] == 'set':
        to_excl.append('context-500k')
        predictors = data.columns.difference(to_excl)
    else:
        predictors = ['context-500k']
    
    print('Training Model: ensemble')
   
    predictor_features = []
    for i, classifier in enumerate(classifiers):
        y = pd.DataFrame(classifier.predict(data[predictors]))
        predictor_features.append(y)
    
    dev_data = pd.concat(predictor_features, axis=1, ignore_index=True)
    ens = linear_model.LinearRegression()
    ens.fit(dev_data, data['label'])
    
    return ens

def test(classifier, data):
    
    to_excl = ['label']
    if sys.argv[5] == 'all':
        predictors = data.columns.difference(to_excl)
    elif sys.argv[5] == 'set':
        to_excl.append('context-500k')
        predictors = data.columns.difference(to_excl)
    else:
        predictors = ['context-500k']
    
    predictions = classifier.predict(data[predictors])
    class_predictions = []
    for p in predictions:
        if p > .5:
            class_predictions.append(1)
        else:
            class_predictions.append(0)
            
    print('Test scores')
    print('confusion matrix')
    print(metrics.confusion_matrix(data['label'], class_predictions))
    print('Pr')
    print(metrics.precision_score(data['label'], class_predictions))
    print('Re')
    print(metrics.recall_score(data['label'], class_predictions))
    print('F')
    print(metrics.f1_score(data['label'], class_predictions))
    
def test_ens(base_classifiers, ensemble, data):
    
    to_excl = ['label']
    if sys.argv[5] == 'all':
        predictors = data.columns.difference(to_excl)
    elif sys.argv[5] == 'set':
        to_excl.append('context-500k')
        predictors = data.columns.difference(to_excl)
    else:
        predictors = ['context-500k']
    
    predictor_features = []
    for i, classifier in enumerate(base_classifiers):
        y = pd.DataFrame(classifier.predict(data[predictors]))
        predictor_features.append(y)
    
    dev_data = pd.concat(predictor_features, axis=1, ignore_index=True)
    predictions = ensemble.predict(dev_data)
    class_predictions = []
    for p in predictions:
        if p > .5:
            class_predictions.append(1)
        else:
            class_predictions.append(0)
            
    print('Test scores')
    print('confusion matrix')
    print(metrics.confusion_matrix(data['label'], class_predictions))
    print('Pr')
    print(metrics.precision_score(data['label'], class_predictions))
    print('Re')
    print(metrics.recall_score(data['label'], class_predictions))
    print('F')
    print(metrics.f1_score(data['label'], class_predictions))
    
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
    for arg in sys.argv[3:-1]:
        C = pd.read_csv(arg, header=None)
        cs.append(C)
        
    cosine_sims = pd.concat(cs, ignore_index=True)
    cosine_sims.columns = ['context-500k']
    training_data = pd.concat((training_data, cosine_sims), axis=1)
    

    #training_portion = int(len(training_data) * 0.875)
    training_portion = int(len(training_data) * 0.875)
    test_portion = int(len(training_data) * 0.025)
    ensemble_portion = int(len(training_data) * 0.1)
    training_data = shuffle(training_data, random_state=3)
    
    sv = train_and_xval(training_data[:training_portion], a="svm")
    test(sv, training_data[training_portion:training_portion+test_portion])
    gb = train_and_xval(training_data[:training_portion], a="gb")
    test(gb, training_data[training_portion:training_portion+test_portion])
    
    ens = vote([sv, gb], training_data[-ensemble_portion:])
    test_ens([sv, gb], ens, training_data[training_portion:training_portion+test_portion])
    
    
    
    
    
    with open(sys.argv[-1]+'.sv_regression.pkl', 'wb') as fid:
        pickle.dump(sv, fid) 
    with open(sys.argv[-1]+'.gb_regression.pkl', 'wb') as fid:
        pickle.dump(gb, fid) 
    with open(sys.argv[-1]+'.regression_ensemble.pkl', 'wb') as fid:
        pickle.dump(ens, fid)     
    
        