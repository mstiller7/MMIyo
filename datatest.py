import random
import numpy as np

doLoop = True
doProcessing = False

gestures = dict()
# gestures [ 
#   gesture_name [ $val, $val, $val ],
#   gesture_name [ ],
#   gesture_name [ ]
# ]
while doLoop:
    name = raw_input("Enter gesture name: ")
    gestures[name] = list()
    raw_input("Press enter to begin recording.")

    print '*vibration*'
    doProcessing = True
    
    # at the time of recording, dot the IMU quaternion with the current EMG data...
    for i in range(20):
        emg = list()
        imu = random.randint(0,100)
        for v in range(8):
            e = random.randint(0,200)
            emg.append(e)
        emg = np.array(emg)
        imu = np.array(imu)
        imu.resize(emg.shape)
        gestures[name].append(np.matmul(emg, imu))

    doProcessing = False
    print '*vibration*'

    print gestures

    choice = raw_input("Complete. Do another? [y/n] ")
    if choice == 'y':
        continue
    else:
        doLoop = False

print 'Procedure complete; file saved.'
