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
    gesture = emg_data[k]
    for g in gesture:
        for emg in g:
            print k, emg