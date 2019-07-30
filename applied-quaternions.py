try:
    import cpickle as pickle
except:
    print "Falling back to normal pickle crop..."
    import pickle
import math
import operator
import time
import tkFileDialog
import Tkinter

import click
import numpy as np

import open_myo as myo

emgs = list()
imus = list()
gestures = dict()


def processEMG(emg):
    emgs.append(emg)


def processIMU(quat, acc, gyro):
    imus.append(quat)


def getDotProduct(emg, imu):
    e = np.array(emg)
    i = np.array(imu)
    i = np.resize(i, e.shape)
    dp = np.matmul(e, i)
    print dp
    return dp


def saveData(data):
    # timestr = time.strftime("%Y%m%d-%H%M%S")
    name = raw_input('Save file as: ')
    filename = "emg_" + name
    with open("emg-data/" + filename + ".pkl", 'wb') as fp:
        pickle.dump(data, fp)
    print 'File saved as:', filename


def connectBT():
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

    myo_device.services.emg_filt_notifications()
    myo_device.services.imu_notifications()
    myo_device.services.set_mode(
        myo.EmgMode.FILT, myo.ImuMode.DATA, myo.ClassifierMode.OFF)
    myo_device.add_emg_event_handler(processEMG)
    myo_device.add_imu_event_handler(processIMU)

    myo_device.services.vibrate(1)
    print "Myo armband connected."

    return myo_device


def recordRealTime():
    MYO = connectBT()
    training_data = loadData()
    while True:
        if MYO.services.waitForNotifications(1):
            # curEntry = (emgs[-1], imus[-1])
            # collect all the emgs & imus separately
            # and analyze them neighborly
            # can we just call them "emus" by now?
            # no?
            data = list()
            for k, v in training_data.iteritems():
                for t in v:
                    # (classification, emg, imu)
                    data.append((k, t[0], t[1]))

def recordData():
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
                curEntry = (emgs[-1], imus[-1])
                gestures[name].append(curEntry)
                # gestures[name].append(getDotProduct(emgs[-1], imus[-1]))

        MYO.services.vibrate(1)

        if click.confirm('Gesture recorded as "' + name + '". Do another?', default=True):
            del emgs[:]
            del imus[:]
            continue
        else:
            print gestures
            saveData(gestures)
            break


def loadData():
    Tkinter.Tk().withdraw()
    fp = tkFileDialog.askopenfilename()
    print("Opening " + fp + "...")
    with open(fp, 'r') as file:
        emg_data = pickle.load(file)

    for k, v in emg_data.iteritems():
        for t in v:
            print k, t[0], t[1]

    print "Loaded data file."

    return emg_data

def euclidean(setA, setB):
    dist = 0
    if len(setA) == len(setB):
        for i in range(len(setA)):
            dist += pow((setA[i] - setB[i]), 2)
    return math.sqrt(dist)

def getNeighbors(k, unknown, givens):
    neighbors = []
    for g in givens:
        eu = euclidean(unknown, g)
        neighbors.append((g, eu))
    neighbors.sort(key=operator.itemgetter(1))
    del neighbors[k:]
    return neighbors

def getResponse(neighbors):
    votes = {}
    for n in neighbors:
        r = n[0][-1]  # get the 'response' index
        if r in votes:
            votes[r] += 1/(n[1])  # add the response's distance-weighted vote
        else:
            votes[r] = 0
    
    votes_sorted = sorted(
        votes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return list(votes_sorted[0])[0]

# recordData()
loadData()
