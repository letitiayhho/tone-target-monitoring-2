from psychopy import prefs
prefs.hardware['audioLib'] = ['ptb']
from psychopy.sound.backend_ptb import SoundPTB as Sound
from psychtoolbox import GetSecs, WaitSecs
from events import EventMarker
import numpy as np

TEST_MODE = True

trials = 1000
min_freq = 40
max_freq = 250

# init device to send TTL triggers
marker = EventMarker()

# set the seed to the subject number so trial order can be recreated
sub_num = input("Input subject number: ")
sub_num = int(sub_num)
np.random.seed(sub_num)

# start the experiment
WaitSecs(5.)

for i in range(trials):

    if TEST_MODE:
        freq = 100
    else:
        freq = np.random.randint(50, 125)
    snd = Sound(freq, secs = 0.1)

    # schedule sound
    now = GetSecs()
    snd.play(when = now + 0.1)
    WaitSecs(0.1)
    marker.send(freq)

    # add jitter between trials
    WaitSecs(0.1+np.random.uniform(0, 0.1))

marker.close()
print("Done.")
