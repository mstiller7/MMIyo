import open_myo as myo
import numpy as np

EMG = list()
IMU = list()


def processEMG(emg):
    global EMG
    # print emg
    EMG = emg
    processData()


def processIMU(quat, acc, gyro):
    global IMU
    # print quat, acc, gyro
    IMU = quat


def processData():
    global EMG, IMU
    e = np.array(EMG)
    i = np.array(IMU)
    i.resize(e.shape)
    print np.matmul(e, i)


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
    myo_device.services.imu_notifications()
    myo_device.services.set_mode(
        myo.EmgMode.FILT, myo.ImuMode.DATA, myo.ClassifierMode.OFF)

    myo_device.add_emg_event_handler(processEMG)
    myo_device.add_imu_event_handler(processIMU)

    # main program loop. await service notifications.
    while True:
        if myo_device.services.waitForNotifications(1):
            continue
        print("Waiting...")


main()
