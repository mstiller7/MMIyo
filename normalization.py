import time
import timeit

import matplotlib.pyplot as plt
import numpy as np

import open_myo as myo

lst = [0, 1, 2, 3, 4, 5, 6, 7]
cur_gesture = list()


def process_emg(emg):
	# print(emg[0])
	if get_reading:
		cur_gesture.append(emg[0])
		print(cur_gesture)


def plotting(vectors, l):
	global cur_gesture
	avgs = [0, 0, 0, 0, 0, 0, 0, 0]
	for v in range(len(vectors)):

		# Construct a vector composed of the average value of all vectors - PER INDEX
		# so, for each entry, add each index to a new single vector
		# and at the end, divide each index by the length of the whole set
		for i in range(len(vectors[v])):
			avgs[i] += vectors[v][i]

	for i in range(len(avgs)):
		print(vectors)
		i = i / len(vectors)
		# attempt at normalization??
		# i = (i - min(avgs)) / (max(avgs) - min(avgs))
		plt.plot(lst, avgs, linewidth=1.0, label=l)
	cur_gesture = list()
	print(avgs)

# TODO: realtime data gathering as in save_emg_signals.py, and plotting per-gesture
# for each set of gestures, create an average plot, and label!!


def main():
	myo_device = myo.Device()
	myo_device.services.sleep_mode(1)  # never sleep
	# purple logo and bar LEDs)
	myo_device.services.set_leds([128, 128, 255], [128, 128, 255])
	myo_device.services.vibrate(1)  # short vibration
	# myo_device.services.emg_filt_notifications()
	myo_device.services.emg_raw_notifications()
	myo_device.services.set_mode(
		myo.EmgMode.RAW, myo.ImuMode.OFF, myo.ClassifierMode.OFF)
	# myo_device.services.set_mode(myo.EmgMode.OFF, myo.ImuMode.OFF, myo.ClassifierMode.OFF)
	time.sleep(1)
	myo_device.add_emg_event_handler(process_emg)

	n_gestures = int(raw_input("Number of gestures: "))
	runtime = int(raw_input("Seconds per gesture: "))
	for g in range(n_gestures):
		name = raw_input("Enter the name of gesture number {}: ".format(g+1))
		raw_input("Press enter to begin recording.")
		myo_device.services.vibrate(1)

		start_time = timeit.default_timer()
		tick = start_time
		get_reading = True
		while round(tick - start_time, 1) <= runtime:
			if myo_device.services.waitForNotifications(1):
				tick = timeit.default_timer()
			else:
				print("Waiting...")
		get_reading = False
		myo_device.services.vibrate(1)
		plotting(cur_gesture, name)


get_reading = False

main()
plt.show()
