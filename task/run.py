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
from functions import *

FREQS = [130, 200, 280]
SEQ_LENS = [30, 40, 50]
TONE_LEN = 0.3
SCORE_NEEDED = 18
SUB_NUM = input("Input subject number: ")
BLOCK_NUM = input("Input block number: ")

#marker = EventMarker()
kb = Keyboard()
kb.clearEvents()

# exp_info = {'sub_num': '', 'block_num':''}
# dlg = DlgFromDict(exp_info)
SUB_NUM = exp_info["sub_num"]
BLOCK_NUM = exp_info["block_num"]

# # If pressed Cancel, abort!
# if not dlg.OK:
#     quit()

# #set keyboard as kb and clear
# kb = Keyboard()
# kb.clearEvents()

# set subject number and block as seed
SEED = int(SUB_NUM + "0" + BLOCK_NUM)
print("Current seed: " + str(seed))
np.random.seed(seed)

# open log file
LOG = open_log(SUB_NUM, BLOCK_NUM)
seq_num = get_seq_num(log) ##### FIX THIS?? do I want to count sequence number at all?
# current_score = 0
current_score = get_current_score(log)

while current_score < SCORE_NEEDED:
    target = get_target(FREQS)
    n_tones = get_n_tones(SEQ_LENS)
    
    play_target(TONE_LEN, target)
    ready()
    (tone_nums, freqs, marks, is_targets, n_targets) = play_sequence(FREQS, TONE_LEN, target, n_tones)
    write_log(LOG, N_TONES, SEED, SUB_NUM, BLOCK_NUM, seq_num, tone_nums, freqs, marks, is_targets, n_targets, target, score)
    
    response = get_response()
    correct = is_correct(response)
    current_score = get_score(SCORE_NEEDED, current_score, correct)
    seq_num += 1

#marker.close()
if not tidlg.OK:
    quit()
core.quit()