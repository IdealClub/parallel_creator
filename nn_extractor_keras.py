# -*- coding: utf-8 -*-
"""
Created on Tue May  9 16:43:04 2017

@author: vurga
"""

import keras
import numpy as np
import sys
from sklearn.utils import shuffle
import sklearn.metrics

def read_data(file):
    
    with open(file, 'r') as source:
        lines = source.readlines()
        
    cvxs = []
    for line in lines:
        cvxs.append(np.fromstring(line.strip(), sep=" "))
       
    return np.concatenate([cvxs], axis=1)
    
if __name__ == '__main__':
    
    ## get data here
    data_X_a = read_data(sys.argv[1])
    data_X_b = read_data(sys.argv[2])
    data_y = np.concatenate((np.tile([1, 0], (int(len(data_X_a)/4), 1)), np.tile([0, 1], (int(len(data_X_a)/4), 1)), np.tile([1, 0], (int(len(data_X_b)/4), 1)), np.tile([0, 1], (int(len(data_X_b)/4), 1))))
    
    ## strategy for feature combination
    ## simple concatenation
    data_X_conc= np.concatenate((data_X_a, data_X_b), axis=1)
    ## element-wise multiplication
    data_X_mult = np.multiply(data_X_a, data_X_b)
    ## subtraction
    data_X_sub = data_X_a - data_X_b
    
    #data_X = np.concatenate((data_X_conc, data_X_mult, data_X_sub), axis=1)
    data_X = data_X_mult
    
    ## paste & shuffle
    full_data = np.concatenate((data_X, data_y), axis=1)
    full_data = shuffle(full_data, random_state=3)
    
    training_portion = int(len(full_data) * 0.875)
    test_portion = int(len(full_data) * 0.025)
    
    ## layer sizes
    n_input = data_X.shape[1] ## number of input neurons
    n_hidden = 1024 ## hidden layer size
    n_output = data_y.shape[1] ## number of labels
    
    train_X = full_data[:training_portion,:n_input]
    train_y = full_data[:training_portion,n_input:]
    
    test_X = full_data[training_portion:training_portion+test_portion,:n_input]
    test_y = full_data[training_portion:training_portion+test_portion,n_input:]
    
    learning_rate = 0.1
    
    # define the architecture of the network
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(n_hidden, input_dim=n_input, init="uniform", activation="sigmoid"))
    #model.add(keras.layers.Dense(384, init="uniform", activation="relu"))
    model.add(keras.layers.Dense(n_output))
    model.add(keras.layers.Activation("softmax"))
    
    # train the model using SGD
    print("[INFO] compiling model...")
    opt = keras.optimizers.Adagrad(lr=learning_rate)
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=['accuracy'])
    model.fit(train_X, train_y, nb_epoch=5, batch_size=32)
    
    # show the accuracy on the testing set
    test_preds = model.predict(test_X)
    print(test_preds)
    print(sklearn.metrics.precision_score(test_preds, test_y))
    print(sklearn.metrics.recall_score(test_preds, test_y))
    print(sklearn.metrics.f1_score(test_preds, test_y))