import open_myo as myo
import numpy as np
import timeit
import time
import pickle

EMG = list()
IMU = list()

get_reading = False


def processEMG(emg):
    global EMG
    # print emg
    EMG = emg
    if get_reading:
        processData()


def processIMU(quat, acc, gyro):
    global IMU
    # print quat, acc, gyro
    IMU = quat


def processData():
    global EMG, IMU, gestures, NAME
    e = np.array(EMG)
    i = np.array(IMU)
    i.resize(e.shape)
    dot_product = np.matmul(e, i)
    print(dot_product)
    gestures[name][i].append[dot_product]


gestures = dict()
NAME = ''

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


n_gestures = int(
    raw_input("How many gestures do you want to perform? (2<x<11): "))
n_iterations = int(raw_input(
    "How many times do you want to repeat each gesture? (x>1, default:3): "))
runtime = int(
    raw_input("How many seconds do you want each gesture to last (default: 2): "))


for g in range(n_gestures):
    name = raw_input("Enter the name of gesture number {}: ".format(g+1))
    # NAME = name
    gestures[name] = list()
    for i in range(n_iterations):
        gestures[name].append(list())
        raw_input("Iteration {}. Press enter to begin recording.".format(i+1))
        myo_device.services.vibrate(1)  # short vibration
        time.sleep(2)
    #        myo_device.services.set_mode(myo.EmgMode.RAW, myo.ImuMode.OFF, myo.ClassifierMode.OFF)
        start_time = timeit.default_timer()
        tick = start_time
        get_reading = True
        while round(tick - start_time, 1) <= runtime:
            if myo_device.services.waitForNotifications(1):
                tick = timeit.default_timer()
    #                continue
            else:
                print("Waiting...")
    #        myo_device.services.set_mode(myo.EmgMode.OFF, myo.ImuMode.OFF, myo.ClassifierMode.OFF)
        get_reading = False
        myo_device.services.vibrate(1)  # short vibration


# main()
