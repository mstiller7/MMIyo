# Python 2.7.16 64-bit
# Encoding: utf-8
# © 2019 Matthew Stiller @ UTA CSE REU
# Adapted from: https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/

import sys

# -----------------------------------------------
# Noosphere: Mathematical Playground
# -----------------------------------------------

# For our purposes throughout, we will assume to be given data sets
# of an 9-length tuple, with the 9th entry being a 
# gesture classification string.
# Example: [1,2,3,4,5,6,7,8,'index-extended']

# Step 2: Similarity.
import math
def euclidean(set_a, set_b, length):
    '''
    Returns the Euclidian distance between sets, by calculating
    the mathematical distance between each values up to the
    given 'length' of values.
    '''
    distance = 0
    for x in range(length):
        distance += pow((set_a[x]-set_b[x]),2)
    return math.sqrt(distance)

# DEBUG: Euclidean distance tests.
# emg_givens = [3,-8,4,1,-1,-2,2,-1,'a']
# emg_ungivens_1 = [-1,7,-6,-3,-1,2,6,-1,'b']
# emg_ungivens_2 = [1,2,3,-4,100,12,3,5,'c']
# eu1 = euclidean(emg_givens, emg_ungivens_1,8)
# eu2 = euclidean(emg_givens, emg_ungivens_2,8)
# print("The Eu. distance (0:1) is: " + str(eu1))
# print("The Eu. distance (0:2) is: " + str(eu2))
# sys.exit()
# From the above tests, we can see that the larger variance in numbers, the greater Euclidean distance.

# Step 3: Neighbors.
import operator
def getNeighbors(givens, unknown, k):
    '''
    Returns the 'k' most similar neighbors to an
    unknown instance from a set of given values.
    '''
    distances = []
    # Iterate through each of our known entries,
    # computing the Euclidean distance between the current set
    # and our unknown instance.
    for i in range(len(givens)):
        eu = euclidean(givens[i], unknown, len(unknown)-1)
        # Nested tuple:
        distances.append((givens[i], eu))
    distances.sort(key=operator.itemgetter(1))

    neighbors = []
    for i in range(k):
        neighbors.append(distances[i][0])
    return neighbors

# DEBUG: Test k-nearest-neighbors.
# set_a = [[2,2,2,'c'],[4,4,4,'a'],[3,3,3,'b']]
# set_b = [1,1,1]
# k = 1
# print(getNeighbors(set_a,set_b,1))
# sys.exit()

# Step 4: Response.
def getResponse(neighbors):
    '''
    Allow each neighbor to vote for their respective attribute,
    and take the majority vote as the resulting prediction.
    '''
    votes = {}
    for i in range(len(neighbors)):
        response = neighbors[i][-1]
        if response in votes:
            votes[response] += 1
        else:
            votes[response] = 1
    votes_sorted = sorted(votes.iteritems(), key=operator.itemgetter(1), reverse=True)
    print("Voting concluded. Results: ")
    print(votes_sorted)
    votes_sorted = list(votes_sorted[0])
    try:
        print("Highest votes: " + votes_sorted[0])
    except:
        pass
    # return list(votes_sorted[0])[0]

# DEBUG: Test voting.
# neighbors = [[1,1,1,'a'],[2,2,2,'b'],[3,3,3,'b']]
# print(getResponse(neighbors))
# sys.exit()

# Step 5: Accuracy.
import random
def getAccuracy(givens, k):
    '''
    Tests 'k' random values in a set by comparing their given
    classifications to their calculated predictions.
    '''
    correct = 0
    for i in range(k):
        # take a random value out
        octet = givens.pop()
        print("Iteration " + str(i) + ". Selected octet: ")
        print(octet)
        c = octet[8]

        # from the main set, take a subset:
        # everything that getResponse supplies based on the 
        # given's classification
        classification = getResponse(givens)
        g = [octet for octet in givens if c == classification]

        for j in range(len(g)):
            if g[j][-1] is c[j]:
                correct += 1
        # stick it back in & sort?
        givens.append(octet)
        givens.sort()
    return (correct/float(len(givens))) * 100.0

# -----------------------------------------------
# Realspace: EMG Classification
# -----------------------------------------------

# Step 1: Data loading.
import pickle
import tkFileDialog
import Tkinter

import numpy as np

# Load the data via GUI.
Tkinter.Tk().withdraw()
fp = tkFileDialog.askopenfilename()
print("Opening " + fp + "...")
with open(fp,'r') as file:
    emg_data = pickle.load(file) # initialdir = "/home"

iterations = [len(value) for value in emg_data.values()][0]
# The Myo armband sends data from its 8 sensors.
channels = 8

emg_classes = list()
emg_octet_groups = list()
emg_octets = list()

# We now load the data from the .pkl file into the lists.
for k in emg_data.keys():
    emg_classes.append(k)
    for i in range(iterations):
        for c in range(channels):
            emg_octet_group = np.array(zip(*emg_data[k][i])[c][0:999])
            emg_octet_groups.append(emg_octet_group)
            for o in xrange(0, len(emg_octet_group), channels):
                emg_octet = emg_octet_group[o:o+channels].tolist()
                emg_octet.append(k)
                emg_octets.append(emg_octet)
                # DEBUG
                # print(emg_octet)

print("Testing accuracy...")
print("Accuracy results: " + str(getAccuracy(emg_octets,10)))

# TODO
# When a new dataset of octets is received, classify it by using the 'k-nearest-neighbor' algorithm.
# We will be testing one octet against one other octet at a time.