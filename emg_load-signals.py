# Load the data via GUI.
import pickle
import tkFileDialog
import Tkinter
Tkinter.Tk().withdraw()
fp = tkFileDialog.askopenfilename()
print("Opening " + fp + "...")
with open(fp, 'r') as file:
    emg_data = pickle.load(file)  # initialdir = "/home"

for k in emg_data:
    count = 0
    gesture = emg_data[k]
    for g in gesture:
        for emg in g:
            if count >= 30:
                break
            print k, ': ', list(emg), ','
            count += 1