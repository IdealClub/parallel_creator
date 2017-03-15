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


def read_data(filename):
    # Read csv to pandas dataframe
    return pd.read_csv(filename, index_col=0, low_memory=False)

def train_and_xval(df, a="svm"):
    
    to_excl = ['label']
    predictors = df.columns.difference(to_excl)
    
    if a == "gb":
        alg = ensemble.GradientBoostingClassifier()
    else:
        alg = svm.SVC()
        
    print('Model: '+a)
    
    # 10-fold cross-validation
    kf = KFold(df.shape[0], n_folds=10, random_state=1)
    # train folds
    predictions = []
    for train, test in kf:
        train_predictors = (df[predictors].iloc[train,:])
        train_target = df['label'].iloc[train]
        alg.fit(train_predictors, train_target)
        test_predictions = alg.predict(df[predictors].iloc[test,:])
        predictions.append(test_predictions)
    # concatenate fold
    predictions = np.concatenate(predictions, axis=0) 
    
    print('CV scores')
    print('confusion matrix')
    print(metrics.confusion_matrix(df['label'], predictions))
    print('Pr')
    print(metrics.precision_score(df['label'], predictions))
    print('Re')
    print(metrics.recall_score(df['label'], predictions))
    
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
    

if __name__ == '__main__':
    
    features = []
    labels = []
    for arg in sys.argv[1:]:
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
    
    training_data = shuffle(training_data, random_state=3)
    p = train_and_xval(training_data[:35000], a="gb")
    test(p, training_data[35000:36000])
        
        