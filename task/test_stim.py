from psychopy import prefs
prefs.hardware['audioLib'] = ['ptb']
from psychopy.sound.backend_ptb import SoundPTB as Sound
from psychtoolbox import GetSecs, WaitSecs
from events import EventMarker
import numpy as np
import os.path
import csv
import time

TRIALS = 50 # takes about 6:40 per block
FREQS = [120, 200, 270]
TONE_LEN = 0.3 # sec

#seed = 0
print("Current seed: no seed, fully random")
#np.random.seed(seed)

# count trial progress in log file
log = "data/logs/test.log"
with open(log, 'w', newline='') as f: # always open file as 'w'
    writer = csv.writer(f)
    writer.writerow(['trial', 'freq', 'marker'])
trial_count = 0
print("Current trial number: " + str(trial_count))

# play the target tone
print("Playing target tone")
index = np.random.randint(0, len(FREQS))
target_freq = FREQS[index]
mark = 0
snd = Sound(target_freq, secs = TONE_LEN)
now = GetSecs()
snd.play(when = now + 1)

WaitSecs(2.)

print("Playing target tone again")
snd.play()
WaitSecs(5.)

sequence_start = time.time()
targets = 0
for i in range(trial_count, TRIALS + 1):
    print(i)
    start = time.time()

    else:
        index = np.random.randint(0, len(FREQS))
        freq = FREQS[index]
        mark = index + 1
        if freq == target_freq:
            targets += 1
    snd = Sound(freq, secs = TONE_LEN)

    # schedule sound
    now = GetSecs()
    snd.play(when = now + 0.01)
    WaitSecs(TONE_LEN)
    #marker.send(mark)

    # log trial info
    with open(log, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([i, freq, mark])

    # add jitter between TRIALS
    WaitSecs(0.3+np.random.uniform(-0.1, 0.09))
    end = time.time()
    print(end - start)

print(f"Number of targets: {targets}")
sequence_end = time.time()
print(f"Sequence time: {sequence_end - sequence_start}")
print("Done.")
