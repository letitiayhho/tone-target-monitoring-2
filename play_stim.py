from psychopy import prefs
prefs.hardware['audioLib'] = ['ptb']
from psychopy.sound.backend_ptb import SoundPTB as Sound
from psychtoolbox import GetSecs, WaitSecs
#from events import EventMarker
import numpy as np
import os.path
import csv

TEST_MODE = False

trials = 20
min_freq = 40
max_freq = 254

# init device to send TTL triggers
#marker = EventMarker()

# set the seed to the subject number so trial order can be recreated
sub_num = input("Input subject number: ")
log = "subj_" + sub_num + ".log"
sub_num = int(sub_num)
np.random.seed(sub_num)

# count trial progress in log file
if not os.path.isfile(log): # create log file if it doesn't exist
    with open(log, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['trial', 'freq', 'marker'])
trial_count = sum(1 for line in open(log))

# start the experiment
WaitSecs(5.)

for i in range(trial_count, trials + 1):

    if TEST_MODE:
        freq = 100
    else:
        freq = np.random.randint(min_freq, max_freq)
        freq = freq - (freq%2) # get only even numbered freqs for tags
    snd = Sound(freq, secs = 0.1)

    # schedule sound
    now = GetSecs()
    snd.play(when = now + 0.1)
    WaitSecs(0.1)
    marker = int(freq/2)
    #marker.send(marker)

    # log trial info
    with open(log, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([i, freq, marker])

    # add jitter between trials
    WaitSecs(0.1+np.random.uniform(0, 0.1))

#marker.close()
print("Done.")
