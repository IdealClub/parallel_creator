# -*- coding: utf-8 -*-
"""
Created on Tue May  2 15:27:27 2017

@author: vurga
"""

import sys
from sklearn.cross_validation import KFold
import numpy as np
from sklearn.utils import shuffle
from sklearn import metrics
import pickle
import pandas as pd
import matplotlib.pyplot as plt

def read_data(filename):
    # Read csv to pandas dataframe
    return pd.read_csv(filename, index_col=0, low_memory=False)


with open('sx_ensemble.pkl', 'rb') as fid:
        s_ens = pickle.load(fid)
with open('all_ensemble.pkl', 'rb') as fid:
        a_ens = pickle.load(fid)
 
## Reading stuff
       
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
        
## Meaningful part
test_data = training_data[32666:33599]
to_excl = ['label']
predictors = test_data.columns.difference(to_excl)
pr_cs = []
re_cs = []
f1_cs = []
pr_as = []
re_as = []
f1_as = []
pr_ss = []
re_ss = []
f1_ss = []
for threshold in np.arange(0.0, 1.05, .05):
    ## ctx
    preds = test_data['context-500k'] >= threshold
    pr_cs.append(metrics.precision_score(preds, test_data['label']))
    re_cs.append(metrics.recall_score(preds, test_data['label']))
    f1_cs.append(metrics.f1_score(preds, test_data['label']))
    
    ## sx
    to_excl = ['label', 'context-500k']
    predictors = test_data.columns.difference(to_excl)
    probs = s_ens.predict_proba(test_data[predictors])
    preds = probs[:,1] >= threshold
    pr_ss.append(metrics.precision_score(preds, test_data['label']))
    re_ss.append(metrics.recall_score(preds, test_data['label']))
    f1_ss.append(metrics.f1_score(preds, test_data['label']))
    ## all
    to_excl = ['label']
    predictors = test_data.columns.difference(to_excl)
    probs = a_ens.predict_proba(test_data[predictors])
    preds = probs[:,1] >= threshold
    pr_as.append(metrics.precision_score(preds, test_data['label']))
    re_as.append(metrics.recall_score(preds, test_data['label']))
    f1_as.append(metrics.f1_score(preds, test_data['label']))
    
print(pr_cs, re_cs)
    
plt.figure()
plt.plot(np.arange(0.0, 1.05, .05), pr_cs, label="Pr")
plt.plot(np.arange(0.0, 1.05, .05), re_cs, label="Re")
plt.plot(np.arange(0.0, 1.05, .05), f1_cs, label="F1")
x1,x2,y1,y2 = plt.axis()
plt.axis((x1,x2,0.0,1.05))
plt.legend()

plt.figure()
plt.plot(np.arange(0.0, 1.05, .05), pr_as, label="Pr")
plt.plot(np.arange(0.0, 1.05, .05), re_as, label="Re")
plt.plot(np.arange(0.0, 1.05, .05), f1_as, label="F1")
x1,x2,y1,y2 = plt.axis()
plt.axis((x1,x2,0.0,1.05))
plt.legend()

plt.figure()
plt.plot(np.arange(0.0, 1.05, .05), pr_ss, label="Pr")
plt.plot(np.arange(0.0, 1.05, .05), re_ss, label="Re")
plt.plot(np.arange(0.0, 1.05, .05), f1_ss, label="F1")
x1,x2,y1,y2 = plt.axis()
plt.axis((x1,x2,0.0,1.05))
plt.legend()
    

