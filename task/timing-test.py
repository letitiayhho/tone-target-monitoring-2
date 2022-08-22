from functions import *
from events import EventMarker
from psychtoolbox import GetSecs, WaitSecs
from psychopy.sound.backend_ptb import SoundPTB as Sound
import random

FREQS = [130, 200, 280]
TONES = 1000
TONE_LEN = 0.2

marker = EventMarker()

for i in range(TONES):
    print(i)

    index = random.randint(0, len(FREQS)-1)
    freq = FREQS[index]
    mark = index + 1
    snd = Sound(freq, secs = TONE_LEN)

    now = GetSecs()
    snd.play(when = now + 0.1)
    WaitSecs(0.1)
    marker.send(mark)
    WaitSecs(TONE_LEN - 0.1)

    WaitSecs(0.1)

print("Done :^)")
