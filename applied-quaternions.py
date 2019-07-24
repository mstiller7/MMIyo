import open_myo as myo
import numpy as np
import time

emgs = list()
imus = list()

def processEMG(emg):
    del emgs[:]
    emgs.append(emg)


def processIMU(quat, acc, gyro):
    del imus[:]
    imus.append(quat)


def getDotProduct(emg, imu):
    e = np.array(emg)
    i = np.array(imu)
    i.resize(e.shape)
    dp = np.matmul(e, i)
    print dp
    return dp


gestures = dict()


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

doLoop = True
while doLoop:
    name = raw_input("Enter gesture name: ")
    gestures[name] = list()
    raw_input("Press enter to begin recording.")

    MYO.services.vibrate(1)
    # doProcessing = True

    # for 3 seconds...
    end = time.time() + 3
    while time.time() < end:
        e = emgs[-1]
        i = imus[-1]
        gestures[name].append(getDotProduct(e, i))

    # doProcessing = False
    MYO.services.vibrate(1)

    choice = raw_input("Complete. Do another? [y/n] ")
    if choice == 'y':
        continue
    else:
        doLoop = False

