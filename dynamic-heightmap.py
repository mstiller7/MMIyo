# make a dynamic height graph of each sensor's value

import matplotlib.pyplot as plt
import numpy
import open_myo as myo

# create empty histogram
h, = plt.plot([0, 1, 2, 3, 4, 5, 6, 7],
              [0, 0, 0, 0, 0, 0, 0, 0])


def updateGraph(g, data):
	global fig
	g.set_ydata(data)
    # plt.draw()
	fig.canvas.draw()
	fig.canvas.flush_events()



def processEMG(emg):
    global h
    updateGraph(h, emg)

fig = plt.figure()
ax = fig.add_subplot(111)

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

    # plt.show()

    # main program loop. await service notifications.
    while True:
        if myo_device.services.waitForNotifications(1):
            continue
        print("Waiting...")


main()
