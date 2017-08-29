# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 14:48:04 2017

@author: vurga
"""

import matplotlib.pyplot as plt

epochs = [0, 1, 2, 3, 4, 5]
##pp_abs_test
en2de = [11.05, 10.58, 11.75, 11.77, 12.16, 11.94]
en2es = [31.6, 32.27, 33.92, 33.94, 34.39, 34.59]
en2fr = [19.01, 21.16, 16.43, 18.57, 17.51, 16.56]
de2en = [15.8, 15.86, 16.66, 16.67, 17.11, 17.01]
es2en = [31.2, 31.18, 31.67, 31.7, 31.77, 31.69]
fr2en = [24.26, 24.89, 23.59, 24.39, 24.31, 23.98]
plt.plot(epochs, en2de)
plt.plot(epochs, en2es)
plt.plot(epochs, en2fr)
plt.plot(epochs, de2en)
plt.plot(epochs, es2en)
plt.plot(epochs, fr2en)
plt.savefig('pp_abs_dev.png')

##pp_title_test
en2de = [31.23, 30.53, 32.48, 32.71, 33.28, 34.19]
en2es = [42.71, 42.18, 43.7, 43.42, 44.56, 45.27]
en2fr = [40, 38.5, 38.31, 40.53, 38.03, 39.01]
de2en = [40.79, 39.93, 41.22, 41.37, 41.71, 40.86]
es2en = [38.55, 37.33, 38.85, 38.73, 40.29, 39.97]
fr2en = [39.09, 39.98, 39.42, 40.35, 38.89, 37.79]

plt.figure()
plt.plot(epochs, en2de)
plt.plot(epochs, en2es)
plt.plot(epochs, en2fr)
plt.plot(epochs, de2en)
plt.plot(epochs, es2en)
plt.plot(epochs, fr2en)
plt.savefig('pp_title_test.png')

##pp_abs_test
en2de = [17.51, 16.93, 18.61, 18.79, 19.39, 19.26]
en2es = [26.91, 26.88, 28.07, 28.03, 28.67, 28.84]
de2en = [24.35, 25.33, 25.52, 26.08, 26.46, 26.09]
es2en = [25.98, 25.96, 25.89, 25.99, 26.35, 26.43]

plt.figure()
plt.plot(epochs, en2de)
plt.plot(epochs, en2es)
plt.plot(epochs, de2en)
plt.plot(epochs, es2en)
plt.savefig('pp_abs_test.png')

##EMEA dev
en2de = [31.29, 32.91, 30.81, 30.29, 28.58, 27.85]
en2es = [38.5, 40.02, 37.55, 37.11, 37.48, 36.54]
en2fr = [26.12, 28.05, 25.92, 25.37, 25.05, 24.24]
de2en = [36.91, 39.36, 37.71, 36.62, 35.69, 35.66]
es2en = [40.77, 43.16, 39.82, 38.9, 38.16, 38.06]
fr2en = [36.39, 37.55, 35.41, 35.34, 33.68, 33.73]
es2de = [14.44, 14.65, 14.74, 12.6, 11.33, 10.24]
de2es = [19.37, 20.23, 19.38, 18.62, 18.1, 17.96]
plt.figure()
plt.plot(epochs, en2de)
plt.plot(epochs, en2es)
plt.plot(epochs, en2fr)
plt.plot(epochs, de2en)
plt.plot(epochs, es2en)
plt.plot(epochs, fr2en)
plt.plot(epochs, es2de)
plt.plot(epochs, de2es)
plt.savefig('emea_dev.png')

## EMEA test
en2de = [31.15, 32.69, 29.7, 29.32, 27.74, 27.8]
en2es = [39.25, 41.62, 39.79, 37.83, 38.29, 37.78]
en2fr = [26.08, 28.19, 26.05, 25.35, 24.42, 23.4]
de2en = [36.1, 38.12, 35.69, 35.5, 34.39, 34.17]
es2en = [40.25, 41.75, 39.38, 38.41, 38.49, 38.19]
fr2en = [34.97, 36.18, 34.01, 33.45, 32.09, 32.7]
de2es = [15.52,  15.34, 13.57, 13.44, 12.09, 11.46]
plt.figure()
plt.plot(epochs, en2de)
plt.plot(epochs, en2es)
plt.plot(epochs, en2fr)
plt.plot(epochs, de2en)
plt.plot(epochs, es2en)
plt.plot(epochs, fr2en)
plt.plot(epochs, es2de)
plt.plot(epochs, de2es)
plt.savefig('emea_test.png')

## newstest
en2de = [14.35, 14.35, 14.46, 14.16, 14.21, 14.42]
en2es = [22.58, 23.09, 23.1, 22.77, 22.68, 22.64]
en2fr = [17.56, 18.46, 17.52, 16.97, 15.99, 15.93]
de2en = [18.89, 19.52, 19.24, 19.44, 19.09, 18.96]
es2en = [23.08, 23.43, 22.7, 22.5, 22.52, 22.16]
fr2en = [22.62, 22.74, 22.21, 21.9, 21.54, 20.97]
es2de = [6.89, 6.97, 7.17, 5.82, 3.45, 3.55]
fr2de = [6.3, 6.54, 6.62, 5.54, 3.64, 3.97]
de2es = [14.42, 14.52, 14.21, 13.06, 12.48, 12.58]
fr2es = [24.92, 25.33, 24.62, 24, 23.33, 23.23]
de2fr = [9.27, 10.4, 7.3, 7.87, 6.65, 4.87]
es2fr = [17.77, 19.11, 17.21, 16.61, 15.55, 13.46]
plt.figure()
plt.plot(epochs, en2de)
plt.plot(epochs, en2es)
plt.plot(epochs, en2fr)
plt.plot(epochs, de2en)
plt.plot(epochs, es2en)
plt.plot(epochs, fr2en)
plt.plot(epochs, es2de)
plt.plot(epochs, fr2de)
plt.plot(epochs, de2es)
plt.plot(epochs, fr2es)
plt.plot(epochs, de2fr)
plt.plot(epochs, es2fr)
plt.savefig('newstest.png')


