import numpy
import time
import timeit

import matplotlib.pyplot as plt
import numpy as np

from open_myo import open_myo

lst = [0, 1, 2, 3, 4, 5, 6, 7]
cur_gesture = list()


def process_emg(emg):
    if get_reading:
        cur_gesture.append(emg[0])


def make_plot(vectors, l):
    global cur_gesture
    avgs = numpy.array([0, 0, 0, 0, 0, 0, 0, 0])

    for v in vectors:
        emg = numpy.array(v)
        avgs += emg

    for i in avgs:
        i = i / len(vectors)
        i = (i - min(avgs)) - (max(avgs) - min(avgs))
    plt.plot(lst, avgs, linewidth=1.0, label=l)

    cur_gesture = list()


def main():
    global get_reading
    myo = open_myo.Device()
    myo.services.sleep_mode(1)
    myo.services.vibrate(1)
    myo.services.emg_raw_notifications()
    myo.services.set_mode(
        open_myo.EmgMode.RAW, open_myo.ImuMode.OFF, open_myo.ClassifierMode.OFF)
    myo.add_emg_event_handler(process_emg)

    n_gestures = int(raw_input("Number of gestures: "))
    runtime = int(raw_input("Seconds per gesture: "))

    for g in range(n_gestures):
        name = raw_input("Enter the name of gesture number {}: ".format(g+1))
        raw_input("Press enter to begin recording.")
        myo.services.vibrate(1)

        start_time = timeit.default_timer()
        tick = start_time
        get_reading = True
        while round(tick - start_time, 1) <= runtime:
            if myo.services.waitForNotifications(1):
                tick = timeit.default_timer()
            else:
                print("Waiting...")
        get_reading = False
        myo.services.vibrate(1)

        make_plot(cur_gesture, name)


get_reading = False

main()

plt.legend(loc='upper right')
plt.show()
