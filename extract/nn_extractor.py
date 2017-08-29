# -*- coding: utf-8 -*-
"""
Created on Fri May  5 08:35:53 2017

@author: vurga
"""

import tensorflow as tf
import numpy as np
import sys
from sklearn.utils import shuffle
import pandas as pd

RANDOM_SEED = 52
tf.set_random_seed(RANDOM_SEED)

def init_weights(shape):
    
    """Weight initialization."""
    
    weights = tf.random_normal(shape, stddev=0.1)
    return tf.Variable(weights)

def forwardprop(X, weights, biases):
    
    """Forward propagation."""
    
    h = tf.add(tf.matmul(X, weights['h']), biases['h']) ## hidden layer
    yhat = tf.matmul(h, weights['o']) + biases['o']
    
    return yhat

def get_batch(data, batch_no, batch_size):
    
    try:
        return data[batch_no*batch_size:(batch_no+1)*batch_size]
    except IndexError:
        return data[batch_no*batch_size:]
    
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
    data_y = np.concatenate((np.tile([1, 0], (int(len(data_X_a)/2), 1)), np.tile([0, 1], (int(len(data_X_a)/2), 1)), np.tile([1, 0], (int(len(data_X_b)/2), 1)), np.tile([0, 1], (int(len(data_X_b)/2), 1))))
 
    ## paste & shuffle
    full_data = np.concatenate((data_X_a, data_X_b, data_y), axis=1)
    full_data = shuffle(full_data, random_state=3)
    
    ## join a & b: first, simple concatenation
    training_portion = int(len(full_data) * 0.875)
    test_portion = int(len(full_data) * 0.025)
    
    train_X = full_data[:training_portion,[0,1]]
    train_y = full_data[:training_portion,2]
    
    test_X = full_data[training_portion:training_portion+test_portion,[0,1]]
    test_y = full_data[training_portion:training_portion+test_portion,2]
  
    ## layer sizes
    n_input = train_X.shape[1] ## number of input neurons
    n_hidden = 256 ## hidden layer size
    n_output = train_y.shape[1] ## number of labels
    
    learning_rate = 0.01
    
    ## placholders
    X = tf.placeholder("float", shape=[None, n_input])
    y = tf.placeholder("float", shape=[None, n_output])
    
    ## weight initalization
    weights = {
            'h' : init_weights([n_input, n_hidden]),
            'o' : init_weights([n_hidden, n_output])}
    biases = {
            'h' : init_weights([n_hidden]),
            'o' : init_weights([n_output])}
    
    ## forward propagation
    yhat = forwardprop(X, weights, biases)
    pred = tf.argmax(yhat, axis=1)
    
    ## backward propagation
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=yhat))
    updates = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
    
    ## run SGD
    with tf.Session() as sess:
        #sess = tf.Session()
        init = tf.global_variables_initializer()
        sess.run(init)
        
        training_epochs = 15
        batch_size = 100
        display_step = 1
        for epoch in range(training_epochs):
            avg_cost = 0.
            total_batch = int(train_X.shape[0]/batch_size) + 1
            
            for i in range(total_batch):
                batch_x = get_batch(train_X, i, batch_size)
                batch_y = get_batch(train_y, i, batch_size)
                _, c = sess.run([updates, cost], feed_dict={X: batch_x,
                                                            y: batch_y})
                
                avg_cost += c / total_batch
            if epoch % display_step == 0:
                print("Epoch:", '%04d' % (epoch+1), "cost=", \
                    "{:.9f}".format(avg_cost))
        print("Optimization Finished!")
        
        # Test model
        correct_prediction = tf.equal(pred, tf.argmax(y, 1))
        # Calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        print("Accuracy:", accuracy.eval({X: test_X, y: test_y}))
        
    