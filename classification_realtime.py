# Python 2.7.15+ 64-bit
# Encoding: utf-8
# © 2019 Matthew Stiller @ UTA CSE REU

# ------------------------------------------------------------------
# imports
# ------------------------------------------------------------------

try:
    import cpickle as pickle
except:
    print "Falling back to normal Pickle..."
    import pickle
import math
import operator
import time
import tkFileDialog
import Tkinter
from collections import Counter

import click
import numpy as np

import open_myo as myo

# ------------------------------------------------------------------
# global variables
# ------------------------------------------------------------------

emgs = list()
k = 50

PRINT_DEBUG = False

# ------------------------------------------------------------------
# myo functions
# ------------------------------------------------------------------

def processBattery(batt):
    print("Battery level: %d" % batt)

def processEMG(emg):
    if PRINT_DEBUG: print emg
    emgs.append(emg)

def connectBT():
    '''
    Order of operations is seriously important here.
    Don't ask me why.
    Data-streaming broke when I moved the vibration
    a few lines down...
    '''
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
    # set logo & bar LED color to purple.
    myo_device.services.set_leds([128, 128, 255], [128, 128, 255]) 
    # short vibration.
    myo_device.services.vibrate(1)

    # define which services we wish to subscribe to.
    myo_device.services.battery_notifications()
    myo_device.services.emg_filt_notifications()
    myo_device.services.set_mode(myo.EmgMode.FILT, myo.ImuMode.OFF, myo.ClassifierMode.OFF)
    myo_device.add_emg_event_handler(processEMG)

    print "Myo armband connected."

    return myo_device

# ------------------------------------------------------------------
# mathematic functions
# ------------------------------------------------------------------

def euclidean(set_a, set_b):
    '''
    Returns the Euclidian distance between EMG sets,
    by calculating the mathematical distance between each value.
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
    unknown instance from a dictionary of given values.
    '''
    neighbors = []
    for c, l in givens.iteritems():
        for emg in l:
            neighbors.append((c, euclidean(unknown, emg), emg))
    neighbors.sort(key=operator.itemgetter(1))
    return neighbors[:k]

# TODO return a weight: how many percentage are correct?
# votes[r] divided by the sum over all r of the votes of r
# check consistency and strength of EMG values - e.g. stdev etc.
# possible do overlapping windows of reading EMG data
# e.g 1 2 3, 2 3 4, 3 4 5...
# make a threshold that allows filtering unsure data,
# but also doesn't do nothing too often

def getResponse(neighbors):
    '''
    Allow each neighbor to vote for their respective attribute,
    and take the majority vote as the resulting prediction.
    '''
    start = time.time()
    votes = {}
    for n in neighbors:
        r = n[0]  # get the 'response' index
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

# ------------------------------------------------------------------
# data functions
# ------------------------------------------------------------------

def recordData():
    global emgs
    gestures = dict()
    MYO = connectBT()
    while True:
        name = raw_input("Enter gesture name: ")
        gestures[name] = list()
        raw_input("Press enter to begin recording.")

        MYO.services.vibrate(1)

        # for 3 seconds...
        end = time.time() + 3
        while time.time() < end:
            # YOU'RE THE BUGGER
            if MYO.services.waitForNotifications(1):
                gestures[name].append(emgs[-1])
                continue
            print "Waiting..."

        MYO.services.vibrate(1)

        print gestures
        if click.confirm('Gesture recorded as "' + name + '". Do another?', default=True):
            del emgs[:]
            continue
        else:
            print gestures
            saveData(gestures)
            break

def saveData(data):
    # timestr = time.strftime("%Y%m%d-%H%M%S")
    name = raw_input('Save file as: ')
    filename = "emg_" + name
    with open("emg-data/" + filename + ".pkl", 'wb') as fp:
        pickle.dump(data, fp)
    print 'File saved as:', filename

def loadData():
    Tkinter.Tk().withdraw()
    fp = tkFileDialog.askopenfilename()
    print("Opening " + fp + "...")
    with open(fp, 'r') as file:
        emgs = pickle.load(file)

    print "Loaded data file."

    return emgs

def classifyRealtime():
    global emgs
    MYO = connectBT()
    data = loadData()
    responses = list()
    while True:
        if MYO.services.waitForNotifications(1):
            # main processing loop. alternately, this could go in the event handler, but meh.
            responses.append(getResponse(getNeighbors(k, emgs[-1], data)))

            if len(responses) >= 10:
                emgs = list()
                winner = Counter(responses).most_common(1)[0][0]
                print("Gesture: " + str(winner))
                print(responses)
                
                count = 0
                for r in responses:
                    if r == winner: count += 1
                print('Precision: ' + str((count/float(len(responses)))*100.0) + '%')
                print('')
                responses = list()
        else:
            print "Waiting..."

# recordData()
# loadData()
classifyRealtime()
