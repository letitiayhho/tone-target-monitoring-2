from cgitb import reset
from re import M
from tracemalloc import stop
from psychopy import prefs
prefs.hardware['audioLib'] = ['ptb']
from psychopy.sound.backend_ptb import SoundPTB as Sound
from psychopy import visual, core
from psychopy.hardware.keyboard import Keyboard 
from psychtoolbox import GetSecs, WaitSecs
from psychopy.gui import DlgFromDict

#from events import EventMarker
import numpy as np
import os.path
import csv
import random

exp_info = {'sub_num': '', 'block_num':''}
dlg = DlgFromDict(exp_info)

# If pressed Cancel, abort!
if not dlg.OK:
    quit()

#set keyboard as kb and clear
kb = Keyboard()
kb.clearEvents()


TEST_MODE = False
TRIALS = 20
FREQS = [50, 120, 170]


# init device to send TTL triggers
#marker = EventMarker()

# ask for subject and block number
#sub_num = input("Input subject number: ")
#block_num = input("Input block number: ")

# set subject number and block as seed
seed = int(exp_info["sub_num"] + "0" + exp_info["block_num"])
print("Current seed: " + str(seed))
np.random.seed(seed)

# count trial progress in log file
#log = "data/logs/subj_" + exp_info['sub_num'] + "_block_" + exp_info['block_num'] + ".log"
#if not os.path.isfile(log): # create log file if it doesn't exist
   # with open(log, 'w', newline='') as f:
   #     writer = csv.writer(f)
   #     writer.writerow(['trial', 'freq', 'marker'])
# trial_count = sum(1 for line in open(log))
# print("Current trial number: " + str(trial_count))

#create window and make fixation 
mywin = visual.Window([800,600], monitor="testMonitor", units="deg")
fixation = visual.TextStim(mywin, '*')


#set the target & target snd and print at beginning of block; set target marker to 0
t_index = np.random.randint(0, len(FREQS))
TARGET = FREQS[t_index]
t_snd = Sound(TARGET, secs = 0.3)
target_marker = 0
print(TARGET)


#have subj press 'enter' to hear the target tone
target_text = visual.TextStim(mywin, text = "Press 'enter' to hear the target tone!",pos=(0.0, 0.0),
                       color=(1, 1, 1), colorSpace='rgb')
again_text = visual.TextStim(mywin, text = "Would you like to hear the target again? [y/n]",pos=(0.0, 0.0),
                       color=(1, 1, 1), colorSpace='rgb')
target_text.draw()
mywin.flip()
while True:
    keys = kb.getKeys()
    if 'return' in keys:
        t_snd.play()
        again_text.draw()
        mywin.flip()
    elif 'y' in keys: 
         t_snd.play()
    elif 'n' in keys: 
        break
        

#have subj press 'enter' to begin block    
block_begin = visual.TextStim(mywin, text = "Press 'enter' to begin! A * will appear everytime the target tone plays. Please count how many times you hear the target tone.",pos=(0.0, 0.0),
                       color=(1, 1, 1), colorSpace='rgb')
block_begin.draw()
mywin.flip()


while True:
    keys = kb.getKeys()
    if 'return' in keys: 
        # start the experiment
        WaitSecs(5.)
        for i in range(1, TRIALS + 1):
            if TEST_MODE:
                freq = 100
            else:
                index = np.random.randint(0, len(FREQS))
                freq = FREQS[index]
                #mark = index + 1
            snd = Sound(freq, secs = 0.3)
            print(i, freq)

            # schedule sound
            now = GetSecs()
            snd.play(when = now + 0.1)
            WaitSecs(0.1)
            

            #draw fixation when target plays
            if freq == TARGET:
                fixation.draw()
                mywin.update()
                WaitSecs(0.1)
                mywin.flip()
                target_marker = target_marker + 1
           
               
            # add jitter between TRIALS
            WaitSecs(0.2+np.random.uniform(0, 0.3))

            #marker.send(mark)

            # log trial info
            # with open(log, 'a') as f:
            #     writer = csv.writer(f)
            #     writer.writerow([i, freq, mark])
 
        break

#marker.close()
print(f"Done. The target was played {target_marker} times")

#have subj report how many times TARGET was heard
target_info = {"Number of times target played:": ""}
tidlg = DlgFromDict(target_info)
n_target = target_info['Number of times target played:']

if not tidlg.OK:
    quit()
print(n_target)

core.quit()