from psychopy import prefs
prefs.hardware['audioLib'] = ['ptb']
from psychopy.sound.backend_ptb import SoundPTB as Sound
from psychtoolbox import GetSecs, WaitSecs
from events import EventMarker
import numpy as np
import os.path
import csv

TEST_MODE = False
TRIALS = 2000
FREQS = [40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260]

# init device to send TTL triggers
marker = EventMarker()

# ask for subject and block number
sub_num = input("Input subject number: ")
block_num = input("Input block number: ")

# set subject number and block as seed
seed = int(sub_num + "0" + block_num)
print("Current seed: " + str(seed))
np.random.seed(seed)

# count trial progress in log file
log = "logs/subj_" + sub_num + "_block_" + block_num + ".log"
if not os.path.isfile(log): # create log file if it doesn't exist
    with open(log, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['trial', 'freq', 'marker'])
trial_count = sum(1 for line in open(log))
print("Current trial number: " + str(trial_count))

# start the experiment
WaitSecs(5.)

for i in range(trial_count, TRIALS + 1):
    print(i)

    if TEST_MODE:
        freq = 100
    else:
        mark = np.random.randint(0, len(FREQS))
        freq = FREQS[mark]
    snd = Sound(freq, secs = 0.2)

    # schedule sound
    now = GetSecs()
    snd.play(when = now + 0.1)
    WaitSecs(0.1)
    marker.send(mark)

    # log trial info
    with open(log, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([i, freq, mark])

    # add jitter between TRIALS
    WaitSecs(0.2+np.random.uniform(0, 0.1))

marker.close()
print("Done.")
