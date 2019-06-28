# Python 2.7.15 64-bit
# Encoding: utf-8
# © 2019 Matthew Stiller @ UTA CSE REU

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

emg_octets = list()
emg_classes = list()

for k in emg_data.keys():
    emg_classes.append(k)
    for i in range(iterations):
        for c in range(channels):
            emg_octet = np.array(zip(*emg_data[k][i])[c][0:999])
            # Print out each octet.
            for o in xrange(0, len(emg_octet), channels):
                print(emg_octet[o:o+channels])
            emg_octets.append(emg_octet)
