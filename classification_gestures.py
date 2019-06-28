# Python 2.7.15 64-bit
# Encoding: utf-8
# © 2019 Matthew Stiller @ UTA CSE REU

# -----------------------------------------------
# Noosphere: Mathematical Playground
# -----------------------------------------------

# Store each octet separately, but in its parent class tag.
# When a new dataset of octets is received, classify it by using the 'k-nearest-neighbor' algorithm.

# We will be testing one octet against one other octet at a time.
emg_knowns = [3,-8,4,1,-1,-2,2,-1]
emg_unknowns = [-1,7,-6,-3,-1,2,6,-1]

import math
def euclidean(set_a, set_b):
    '''
    Returns the Euclidian distance between sets of the same length.
    '''
    distance = 0
    for x in range(len(set_a)):
        distance += pow((set_a[x]-set_b[x]),2)
    return math.sqrt(distance)

eu = euclidean(emg_knowns, emg_unknowns)
print("The Eu. distance is: " + str(eu))

import sys
sys.exit()

# -----------------------------------------------
# Realspace: EMG Classification
# -----------------------------------------------

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
emg_octets = list()

for k in emg_data.keys():
    emg_classes.append(k)
    for i in range(iterations):
        for c in range(channels):
            emg_octet = np.array(zip(*emg_data[k][i])[c][0:999])
            # Debug: print out each octet.
            for o in xrange(0, len(emg_octet), channels):
                print("Gesture classification: " + k)
                print(emg_octet[o:o+channels])
            emg_octets.append(emg_octet)
