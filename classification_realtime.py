# Python 2.7.15+ 64-bit
# Encoding: utf-8
# © 2019 Matthew Stiller @ UTA CSE REU

import math
import operator
import pickle
import sys
import time
import tkFileDialog
import Tkinter
from collections import Counter
import itertools

import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean as eu

import open_myo as myo


def euclidean(set_a, set_b, length):
    '''
    Returns the Euclidian distance between sets, by calculating
    the mathematical distance between each values up to the
    given 'length' of values.
    '''
    distance = 0
    for x in range(length):
        try:
            distance += pow((set_a[x]-set_b[x]),2)
        except:
            pass
    return math.sqrt(distance)

def getNeighbors(givens, unknown, k):
    '''
    Returns the 'k' most similar neighbors to an
    unknown instance from a set of given values.
    '''
    if (PRINT_DEBUG):
        print("Now testing: ")
        print(unknown)
    distances = []
    # Iterate through each of our known entries,
    # computing the Euclidean distance between the current set
    # and our unknown instance.
    for i in range(len(givens)):
        if len(givens[i]) >= 8 or len(unknown) >= 8:
            eu = euclidean(givens[i], unknown, len(unknown)-1)
            # print eu
            # Nested tuple of a given octet and its distance to the unknown:
            distances.append((givens[i], eu))
        else:
            break
    distances.sort(key=operator.itemgetter(1))
    
    # print(distances)

    neighbors = []
    for i in range(k):
        try:
            neighbors.append((distances[i][0], distances[i][1]))
        except:
            pass

    return neighbors

def getResponse(neighbors):
    '''
    Allow each neighbor to vote for their respective attribute,
    and take the majority vote as the resulting prediction.
    '''
    start = time.time()
    votes = {}
    # print(neighbors)
    for i in range(len(neighbors)):
        response = neighbors[i][0][-1]
        if response in votes:
            try:
                votes[response] += 1/(neighbors[i][1]) # the "weight" of a vote?
            except:
                votes[response] += 0
        else:
            try:
                votes[response] = 1/(neighbors[i][1])
            except:
                votes[response] = 0

    votes_sorted = sorted(votes.iteritems(), key=operator.itemgetter(1), reverse=True)
    if (PRINT_DEBUG):
        print("Voting concluded. Results: ")
        print(votes_sorted)
    winner = list(votes_sorted[0])
    end = time.time()
    try:
        if (PRINT_DEBUG): print("Duration: " + str('%.3f'%(end-start)) + " seconds.")
    except:
        pass
    return winner[0]

def loadData():
    '''
    Allow the user to select a file of training data.
    '''
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
    
    print('Loaded datasets.')
    return emg_octets

def processBattery(batt):
    print("Battery level: %d" % batt)

responses = list()

def processEMG(emg):
    global responses
    neighbors = getNeighbors(emg_octets, emg, k)
    # print neighbors
    response = getResponse(neighbors)

    responses.append(response)
    if len(responses) >= 10:
        print("Gesture: " + str(response))
        print(responses)

        winner = Counter(responses).most_common(1)[0][0]
        count = 0
        for i in range(len(responses)):
            if responses[i] == winner:
                count += 1
        print('Precision: ' + str((count/float(len(responses)))*100.0) + '%')
        print('')
        responses = list()

# load our known ("sample") data.
emg_octets = loadData()
k = 100

def main():
    print('Connecting to Myo armband...')
    # assign the device to a var. get the MAC address first!
    myo_mac_addr = myo.get_myo()
    myo_device = myo.Device()

    # print developer information to console.
    print("MAC: %s" % myo_mac_addr)
    fw = myo_device.services.firmware()
    print("Firmware: %d.%d.%d.%d" % (fw[0], fw[1], fw[2], fw[3]))
    print("Battery: %d" % myo_device.services.battery())

    # never sleep.
    myo_device.services.sleep_mode(1)
    # short vibration.
    myo_device.services.vibrate(1)

    myo_device.services.emg_filt_notifications()
    myo_device.services.set_mode(myo.EmgMode.FILT, myo.ImuMode.OFF, myo.ClassifierMode.OFF)
    myo_device.add_emg_event_handler(processEMG)

    # main program loop. await service notifications.
    while True:
        if myo_device.services.waitForNotifications(1):
            continue
        print("Waiting...")

PRINT_DEBUG = False

main()
