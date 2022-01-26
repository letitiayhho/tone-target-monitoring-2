from psychopy.sound.backend_ptb import SoundPTB as Sound
from psychtoolbox import GetSecs, WaitSecs
#from RTBox import RTBox
import numpy as np

trials = 10
min_freq = 40
max_freq = 250

# init device to send TTL triggers
#box = RTBox()

# set the seed to the subject number so trial order can be recreated
np.random.seed(0)

# start the experiment
WaitSecs(5.)

for i in range(trials):
    freq = np.random.randint(40, 250)
    snd = Sound(freq, secs = 0.1)

    # schedule sound
    now = GetSecs()
    snd.play(when = now + 0.1)

    # try to send TTL trigger at same time as sound
    WaitSecs(0.099)
    #box.TTL(trigger)

    # add jitter between trials
    WaitSecs(0.1+np.random.uniform(0, 0.1))

#box.close()
print("Done.")
