import time

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
    # short vibration.
    myo_device.services.vibrate(1)

    myo_device.services.emg_filt_notifications()
    myo_device.services.imu_notifications()
    myo_device.services.set_mode(
        myo.EmgMode.FILT, myo.ImuMode.DATA, myo.ClassifierMode.OFF)

    myo_device.add_emg_event_handler(processEMG)
    myo_device.add_imu_event_handler(processIMU)

    return myo_device


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
            gestures[name].append(getDotProduct(emgs[-1], imus[-1]))

    MYO.services.vibrate(1)

    if click.confirm('Gesture recorded as ' + name + ". Do another?", default=True):
        continue
    else:
        break
