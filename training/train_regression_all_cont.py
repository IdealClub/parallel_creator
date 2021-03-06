# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:43:01 2017

args: context_sim score

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
    return pd.read_csv(filename, low_memory=False)

def read_data_sx(filename):
    # Read csv to pandas dataframe
    return pd.read_csv(filename, index_col=0, low_memory=False)

def train_and_xval(df, a="svm"):
    
    to_excl = ['label']
    predictors = df.columns.difference(to_excl)
    
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
    predictors = data.columns.difference(to_excl)
    
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
    predictors = data.columns.difference(to_excl)
    
    predictions = classifier.predict(data[predictors])
    class_predictions = []
    for p in predictions:
        if p > 2.5:
            class_predictions.append(1)
        else:
            class_predictions.append(0)
            
    labels = []
    for label in data['label']:
        if label > 2.5:
            labels.append(1)
        else:
            labels.append(0)
            
    print('Test scores (decision threshold 2.5)')
    print('confusion matrix')
    print(metrics.confusion_matrix(labels, class_predictions))
    print('Pr')
    print(metrics.precision_score(labels, class_predictions))
    print('Re')
    print(metrics.recall_score(labels, class_predictions))
    print('F')
    print(metrics.f1_score(labels, class_predictions))
    
    print('MSE')
    print(metrics.mean_squared_error(data['label'], predictions))
    
def test_ens(base_classifiers, ensemble, data):
    
    to_excl = ['label']
    predictors = data.columns.difference(to_excl)
    
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
       
    X = read_data(sys.argv[1])
    y = read_data(sys.argv[2])
    
    features = []
    for arg in sys.argv[3:]:
        S = read_data_sx(arg)
        features.append(S)
    sx_features = pd.concat(features, ignore_index=True)
    
    training_data = pd.concat((X, y), axis=1, ignore_index=True)
    training_data.columns = ['context-500k', 'label']
    
    training_data = pd.concat([sx_features, training_data], axis=1, ignore_index=True)
    training_data.columns = ['2-gram-cos', '3-gram-cos', '4-gram-cos',  '5-gram-cos', 'chars-1', 'chars-2', 'cognate-cos', 'length-factor', 'tokens-1', 'tokens-2', 'context-500k', 'label']
    
    training_data = training_data.dropna()
    training_data = training_data.convert_objects(convert_numeric=True)
    training_data = training_data.dropna()
    original_test = shuffle(training_data[:37332], random_state=3)[32666:33599]
    
    training_portion = int(len(training_data) * 0.875)
    test_portion = int(len(training_data) * 0.025)
    ensemble_portion = int(len(training_data) * 0.1)
    training_data = shuffle(training_data, random_state=2)
    print(training_data[training_data.isnull().any(axis=1)])
    
    #sv = train_and_xval(training_data[:training_portion], a="svm")
    gb = train_and_xval(training_data, a="gb")
    print('Original BUCC test set')
    test(gb, original_test)
    test(gb, training_data[training_portion:training_portion+test_portion])
  
    #ens = vote([sv, gb], training_data[-ensemble_portion:])
   
    #with open('all.sv_regression_cnt.pkl', 'wb') as fid:
    #    pickle.dump(sv, fid) 
    with open('all.gb_regression_cnt.pkl', 'wb') as fid:
        pickle.dump(gb, fid) 
    #with open('all.regression_ensemble_cnt.pkl', 'wb') as fid:
    #    pickle.dump(ens, fid)     
    
        
