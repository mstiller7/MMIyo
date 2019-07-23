# Python 2.7.16 64-bit
# Encoding: utf-8
# © 2019 Matthew Stiller @ UTA CSE REU
# Adapted from: https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/

import numpy as np
import Tkinter
import tkFileDialog
import pickle
import time
import operator
import sys

from fastdtw import fastdtw
from scipy.spatial.distance import euclidean as eu

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
    # a = list(set_a)[:-1]
    # b = list(set_b)[:-1]
    # distance, path = fastdtw(a, b, dist=eu)
    # return distance
    distance = 0
    for x in range(length):
        try:
            distance += pow((set_a[x]-set_b[x]),2)
        except:
            pass
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


def getNeighbors(givens, unknown, k):
    '''
    Returns the 'k' most similar neighbors to an
    unknown instance from a set of given values.
    '''
    print("Now testing: ")
    print(unknown)
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
    start = time.time()
    votes = {}
    for i in range(len(neighbors)):
        response = neighbors[i][-1]
        if response in votes:
            votes[response] += 1
        else:
            votes[response] = 1
    votes_sorted = sorted(
        votes.iteritems(), key=operator.itemgetter(1), reverse=True)
    print("Voting concluded. Results: ")
    print(votes_sorted)
    winner = list(votes_sorted[0])
    end = time.time()
    try:
        # print("Highest votes: " + winner[0])
        print("Duration: " + str('%.9f' % (end-start)) + " seconds.")
    except:
        pass
    return winner[0]

# DEBUG: Test voting.
# neighbors = [[1,1,1,'a'],[2,2,2,'b'],[3,3,3,'b']]
# print(getResponse(neighbors))
# sys.exit()

# -----------------------------------------------
# Realspace: EMG Classification
# -----------------------------------------------


# Step 1: Data loading.

# Load the data via GUI.
Tkinter.Tk().withdraw()
fp = tkFileDialog.askopenfilename()
print("Opening " + fp + "...")
with open(fp, 'r') as file:
    emg_data = pickle.load(file)  # initialdir = "/home"

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

set_test = [
    [105, 73, 88, 122, 232, 445, 304, 112, 'fist'],
    [102, 78, 97, 135, 268, 477, 316, 113, 'fist'],
    [107, 75, 93, 145, 286, 452, 283, 119, 'fist'],
    [114, 78, 96, 149, 294, 425, 289, 124, 'fist'],
    [110, 76, 97, 149, 305, 455, 303, 136, 'fist'],
    [102, 89, 103, 146, 274, 383, 298, 115, 'fist'],
    [123, 97, 98, 136, 253, 355, 276, 119, 'fist'],
    [122, 99, 100, 127, 240, 351, 271, 113, 'fist'],
    [127, 97, 100, 116, 236, 363, 275, 106, 'fist'],
    [128, 100, 118, 135, 257, 356, 257, 96, 'fist']
]

# set_test = [
#     [415, 68, 37, 67, 131, 163, 61, 154, 'slap-left'],
#     [436, 67, 36, 63, 128, 157, 63, 184, 'slap-left'],
#     [498, 68, 39, 56, 109, 161, 59, 200, 'slap-left'],
#     [488, 69, 38, 48, 103, 159, 63, 195, 'slap-left'],
#     [501, 62, 41, 60, 117, 157, 56, 198, 'slap-left'],
#     [468, 63, 46, 66, 120, 145, 53, 190, 'slap-left'],
#     [417, 58, 52, 71, 120, 145, 55, 158, 'slap-left'],
#     [389, 68, 52, 72, 116, 130, 59, 156, 'slap-left'],
#     [439, 72, 53, 76, 110, 156, 54, 165, 'slap-left'],
#     [455, 76, 52, 69, 93, 167, 63, 166, 'slap-left']
# ]

k = 100
count = 0
for i in range(len(set_test)):
    neighbors = getNeighbors(emg_octets, set_test[i], k)
    classification = set_test[i][8]
    response = getResponse(neighbors)
    if (classification == response):
        count += 1
    print('')

# print("Accuracy results: " + str((count/float(k))*100.0) + '%')
# print('')
