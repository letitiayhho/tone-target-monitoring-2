from cgitb import reset
from re import M
from tracemalloc import stop
from psychopy import prefs
from psychopy.hardware.keyboard import Keyboard 
from psychopy.gui import DlgFromDict
from psychopy import visual, core
from functions import *

FREQS = [130, 200, 280]
SEQ_LENS = [30, 40, 50]
TONE_LEN = 0.3
SCORE_NEEDED = 18
SUB_NUM = input("Input subject number: ")
BLOCK_NUM = input("Input block number: ")
WIN = visual.Window([800,600], monitor="testMonitor", units="deg")

#marker = EventMarker()
KB = Keyboard()
KB.clearEvents()

# exp_info = {'sub_num': '', 'block_num':''}
# dlg = DlgFromDict(exp_info)
# SUB_NUM = exp_info["sub_num"]
# BLOCK_NUM = exp_info["block_num"]

# If pressed Cancel, abort!
# if not dlg.OK:
#     quit()

# set subject number and block as seed
SEED = int(SUB_NUM + "0" + BLOCK_NUM)
print("Current seed: " + str(SEED))
random.seed(SEED)

# open log file
LOG = open_log(SUB_NUM, BLOCK_NUM)
seq_num = get_seq_num(LOG)
score = get_score(LOG)

# play sequences until SCORE_NEEDED is reached
while score < SCORE_NEEDED:
    target = get_target(FREQS)
    n_tones = get_n_tones(SEQ_LENS)
    
    # Play target
    play_target(KB, WIN, TONE_LEN, target)
    ready(KB, WIN)
    WaitSecs(1)
    
    # Play tones
    fixation(WIN)
    core.wait(1)
    tone_nums, freqs, marks, is_targets, n_targets = play_sequence(FREQS, TONE_LEN, target, n_tones)
    WIN.flip()
    core.wait(1)
    
    # Get response
    response = get_response(KB, WIN)
    correct, score = update_score(WIN, N_TARGETS, RESPONSE, score, SCORE_NEEDED)
    seq_num += 1
    
    # Write log file
    write_log(LOG, n_tones, SEED, SUB_NUM, BLOCK_NUM, seq_num, target, tone_nums, 
              freqs, marks, is_targets, n_targets, response, correct, score)
    core.wait(1)

#marker.close()
# if not tidlg.OK:
#     quit()
# core.quit()