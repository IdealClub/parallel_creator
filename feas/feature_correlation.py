# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:43:01 2017

args: context_sim score

@author: vurga
"""

import pandas as pd, numpy as np
import sys
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

def read_data(filename):
    # Read csv to pandas dataframe
    return pd.read_csv(filename, low_memory=False)

def read_data_sx(filename):
    # Read csv to pandas dataframe
    return pd.read_csv(filename, index_col=0, low_memory=False)

def correlation_test(data):
    
    to_excl = ['label']
    predictors = data.columns.difference(to_excl)

    corrs = []
    for predictor in predictors:
        corrs.append(pearsonr(data[predictor], data['label']))
        
    return corrs

if __name__ == '__main__':
       
    X = read_data(sys.argv[1])
    y = read_data(sys.argv[2])
    
#    features = []
#    for arg in sys.argv[3:]:
#        S = read_data_sx(arg)
#        features.append(S)
#    sx_features = pd.concat(features, ignore_index=True)
    
    training_data = pd.concat((X, y), axis=1, ignore_index=True)
    training_data.columns = ['context-500k', 'label']
    
    #training_data = pd.concat([sx_features, training_data], axis=1, ignore_index=True)
    #training_data.columns = ['2-gram-cos', '3-gram-cos', '4-gram-cos',  '5-gram-cos', 'chars-1', 'chars-2', 'cognate-cos', 'length-factor', 'tokens-1', 'tokens-2', 'context-500k', 'label']
    
    #training_data = training_data[37332+1595+1555:]
    training_data = training_data.convert_objects(convert_numeric=True)
    training_data = training_data.fillna(0)
    
    #c = correlation_test(training_data[:37332])
    ctx_corr = pearsonr(training_data['context-500k'], training_data['label'])
    
    ## plot
    N = 5
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35 
    fig, ax = plt.subplots()
    rects_ctx = ax.bar(ind, (0.9, 0.55, 0.58, 0.23, 0.47), width)
    ax.set_ylabel('Correlation')
    ax.set_xticks(ind + width / 2)
    ax.set_yticks(np.arange(0.0, 1.1, 0.1))
    ax.set_xticklabels(('BUCC', 'en-es', 'en-en', 'es-es', 'joint'))
    ax.set_ylim((0, 1))
    ax.grid(axis='y')
    fig.savefig('ctx_correl.png')