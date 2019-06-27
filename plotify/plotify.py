#  Copyright 2018 Alvaro Villoslada (Alvipe)
#  This file is part of Open Myo.
#  Open Myo is distributed under a GPL 3.0 license

import matplotlib.pyplot as plt
import numpy as np
import pickle
import Tkinter, tkFileDialog
from emgesture import fextraction as fex
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# Data loading - now with GUI! For some reason, we're in Python2. Whatever...
Tkinter.Tk().withdraw()
fp = tkFileDialog.askopenfilename()
print("Opening " + fp + "...")
with open(fp,'r') as file:
    emg_data = pickle.load(file) # initialdir = "/home"

n_classes = len(emg_data)
n_iterations = [len(value) for value in emg_data.values()][0]
n_channels = 8
n_signals = n_classes*n_iterations*n_channels
emg = list()
segmented_emg = list()
class_labels = list()

#for m in range(1,n_classes+1):
#    for i in range(n_iterations):
#        for c in range(1,n_channels+1):
#            emg.append(emg_data['motion'+str(m)+'_ch'+str(c)][:,i]) #motion1_ch1_i1, motion1_ch2_i1, motion1_ch1_i2, motion1_ch2_i2

for g in emg_data.keys():
    class_labels.append(g)
    for i in range(n_iterations):
        for c in range(n_channels):
            emg.append(np.array(zip(*emg_data[g][i])[c][0:999]))

#for z in range(n_signals):
#    emg[z] = emg[z]*(5/2)/2**24

# Segmentation
for n in range(n_signals):
    segmented_emg.append(fex.segmentation(emg[n],n_samples=50))

# Feature calculation
feature_list = [fex.mav, fex.rms, fex.var, fex.ssi, fex.zc, fex.wl, fex.ssc, fex.wamp]

n_segments = len(segmented_emg[0][0])
for i in range(0,n_signals,n_channels):
    n_segments = min(n_segments,len(segmented_emg[i][0]))

# n_segments = len(segmented_emg[0][0])
n_features = len(feature_list)
feature_matrix = np.zeros((n_classes*n_iterations*n_segments,n_features*n_channels))
n = 0

for i in range(0,n_signals,n_channels):
    # n_segments = len(segmented_emg[i][0])
    for j in range(n_segments):
        # print("n_segments: " + str(n_segments))
        # print('n: ' + str(n) + ', i: ' + str(i) + ', j: ' + str(j))
        feature_matrix[n] = fex.features((segmented_emg[i][:,j],
                                          segmented_emg[i+1][:,j],
                                          segmented_emg[i+2][:,j],
                                          segmented_emg[i+3][:,j],
                                          segmented_emg[i+4][:,j],
                                          segmented_emg[i+5][:,j],
                                          segmented_emg[i+6][:,j],
                                          segmented_emg[i+7][:,j]),feature_list)
        n = n + 1

# Target matrix generation
y = fex.generate_target(n_iterations*n_segments,class_labels)

# Dimensionality reduction and feature scaling
[X,reductor,scaler] = fex.feature_scaling(feature_matrix, y)
# print(X[0,0])
# print(X[0,1])

# Split dataset into training and testing datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Classifier training
classifier = SVC(kernel='rbf',C=10,gamma=10)
classifier.fit(X_train,y_train)

# Classification
predict = classifier.predict(X_test)
print("Classification accuracy = %0.5f." %(classifier.score(X_test,y_test)))

# Plotting
colors = ['red','blue','green','cyan','magenta','yellow','lime','orange']
for i in range(0, n_classes):
    if len(X[0]) < 2:
        plt.scatter(X[i*n_segments*n_iterations:(i+1)*n_segments*n_iterations,0],X[i*n_segments*n_iterations:(i+1)*n_segments*n_iterations,0],c=colors[i],label=class_labels[i])
    else:
        plt.scatter(X[i*n_segments*n_iterations:(i+1)*n_segments*n_iterations,0],X[i*n_segments*n_iterations:(i+1)*n_segments*n_iterations,1],c=colors[i],label=class_labels[i])
plt.title(fp)
plt.legend(scatterpoints=1,loc='center left', bbox_to_anchor=(1, 0.5))
# plt.show()

import os
output = '../graphs/' + os.path.split(fp)[1] + '.png'
plt.savefig(output, bbox_inches='tight')
print('Saved file to ' + output)
