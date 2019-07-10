#  Copyright 2018 Alvaro Villoslada (Alvipe)
#  This file is part of Open Myo.
#  Open Myo is distributed under a GPL 3.0 license

import open_myo as myo

def process_emg(emg):
    print(str(emg[0]) + ',')

def process_imu(quat, acc, gyro):
    print(quat)

def process_sync(arm, x_direction):
    print(arm, x_direction)

def process_classifier(pose):
    print(pose)

def process_battery(batt):
    print("Battery level: %d" % batt)

def led_emg(emg):
    """Sets the LED to be red over a certain threshold, otherwise it is set to purple."""
    if(emg[0] > 80):
        myo_device.services.set_leds([255, 0, 0], [128, 128, 255])
    else:
        myo_device.services.set_leds([128, 128, 255], [128, 128, 255])

# assign the device to a var. get the MAC address first!
myo_mac_addr = myo.get_myo()
myo_device = myo.Device()

# print developer information to console.
print("MAC address: %s" % myo_mac_addr)
fw = myo_device.services.firmware()
print("Firmware version: %d.%d.%d.%d" % (fw[0], fw[1], fw[2], fw[3]))
print("Battery level: %d" % myo_device.services.battery())

# never sleep.
myo_device.services.sleep_mode(1)
# set logo & bar LED color to purple.
myo_device.services.set_leds([128, 128, 255], [128, 128, 255]) 
# short vibration.
myo_device.services.vibrate(1)

# define which services we wish to subscribe to.
# myo_device.services.battery_notifications()
myo_device.services.classifier_notifications()
# myo_device.services.emg_filt_notifications()
myo_device.services.emg_raw_notifications()
myo_device.services.imu_notifications()

myo_device.services.set_mode(myo.EmgMode.RAW, myo.ImuMode.OFF, myo.ClassifierMode.OFF)

myo_device.add_emg_event_handler(process_emg)
myo_device.add_emg_event_handler(led_emg)
myo_device.add_imu_event_handler(process_imu)
myo_device.add_sync_event_handler(process_sync)
# myo_device.add_classifier_event_handler(process_classifier)

# main program loop. await service notifications.
while True:
    if myo_device.services.waitForNotifications(1):
        continue
    print("Waiting...")
