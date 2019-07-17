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

import numpy as np

import open_myo as myo


def euclidean(set_a, set_b):
    '''
    Returns the Euclidian distance between EMG sets, by calculating
    the mathematical distance between each value.
    We assume both the sets' lengths are 8,
    ignoring the possible 9th classification value.
    '''
    distance = 0
    for i in range(8):
        distance += pow((set_a[i]-set_b[i]), 2)
    return math.sqrt(distance)


def getNeighbors(k, unknown, givens):
    '''
    Returns the 'k' most similar neighbors to an
    unknown instance from a set of given values.
    '''
    distances = []
    # Iterate through each of our known entries,
    # computing the Euclidean distance between the current set
    # and our unknown instance.
    for g in givens:
        eu = euclidean(unknown, g)
        # nested tuple of a given octet and its distance to the unknown
        distances.append((g, eu))
    distances.sort(key=operator.itemgetter(1))

    neighbors = []
    for i in range(k):
        neighbors.append((distances[i][0], distances[i][1]))
    return neighbors


def getResponse(neighbors):
    '''
    Allow each neighbor to vote for their respective attribute,
    and take the majority vote as the resulting prediction.
    '''
    start = time.time()
    votes = {}
    for n in neighbors:
        r = n[0][-1]  # get the 'response' index
        if r in votes:
            votes[r] += 1/(n[1])  # add the response's distance-weighted vote
        else:
            votes[r] = 0

    votes_sorted = sorted(
        votes.iteritems(), key=operator.itemgetter(1), reverse=True)
    if (PRINT_DEBUG):
        print "Voting concluded. Results:", votes_sorted
    winner = list(votes_sorted[0])
    end = time.time()

    if (PRINT_DEBUG):
        print("Duration: " + str('%.3f' % (end-start)) + " seconds.")

    return winner[0]


def loadData():
    '''
    Allow the user to select a file of training data.
    '''
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
                    # honestly, just never load incomplete vectors. life is so much easier.
                    if len(emg_octet) == 9:
                        emg_octets.append(emg_octet)

    print('Loaded datasets.')
    emg_octets.sort()
    return emg_octets


def processBattery(batt):
    print("Battery level: %d" % batt)


responses = list()


def processEMG(emg):
    global responses
    global emg_octets
    neighbors = getNeighbors(k, emg, emg_octets)
    response = getResponse(neighbors)

    responses.append(response)
    if len(responses) >= 10:
		winner = Counter(responses).most_common(1)[0][0]
		print("Gesture: " + str(winner))
		print(responses)
		
		count = 0
		for i in range(len(responses)):
			if responses[i] == winner:
				count += 1
		print('Precision: ' + str((count/float(len(responses)))*100.0) + '%')
		print('')
		responses = list()


emgs = list()


def processAverageEMG(emg):
    global emg_octets
    global emgs

    emgs.append(emg)
    if len(emgs) >= 20:
        avgs = np.average(np.array(emgs), axis=0)
        neighbors = getNeighbors(k, avgs, emg_octets)
        response = getResponse(neighbors)
        print("Gesture: " + str(response))


# load our known ("sample") data.
emg_octets = loadData()
k = 5


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
    myo_device.services.set_mode(
        myo.EmgMode.FILT, myo.ImuMode.OFF, myo.ClassifierMode.OFF)
    myo_device.add_emg_event_handler(processEMG)
    # myo_device.add_emg_event_handler(processAverageEMG)

    # main program loop. await service notifications.
    while True:
        if myo_device.services.waitForNotifications(1):
            continue
        print("Waiting...")


PRINT_DEBUG = False

main()
