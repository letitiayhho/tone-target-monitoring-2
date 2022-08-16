from psychopy import prefs
prefs.hardware['audioLib'] = ['ptb']
from psychopy.sound.backend_ptb import SoundPTB as Sound
from psychtoolbox import GetSecs, WaitSecs
from events import EventMarker
import numpy as np
import os.path
import random
import csv

open_log(SUB_NUM, BLOCK_NUM):
    log = "data/logs/subj_" + SUB_NUM + "_block_" + BLOCK_NUM + ".log"
    if not os.path.isfile(log): # create log file if it doesn't exist
        with open(log, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['seed', 
                             'sub_num', 
                             'block_num', 
                             'seq_num', 
                             'tone_num',
                             'freq', 
                             'mark', 
                             'is_target',
                             'n_targets', 
                             'target', 
                             'score'])
    sequence_count = sum(1 for line in open(log))
    print("Current sequence number: " + str(sequence_count))
    return(log)

get_target(FREQS):
    target = random.choice(FREQS)
    return(target)

get_n_tones(SEQ_LENS):
    n_tones = random.choice(SEQ_LENS)
    return(n_tones)

play_target(TONE_LEN, target):
    t_snd = Sound(target, secs = TONE_LEN)
    
    # creds to jared
    target_text = visual.TextStim(mywin, 
                                  text = "Press 'enter' to hear the target tone!",
                                  pos=(0.0, 0.0),
                                  color=(1, 1, 1), 
                                  colorSpace='rgb')
    again_text = visual.TextStim(mywin, 
                                 text = "Would you like to hear the target again? [y/n]",
                                 pos=(0.0, 0.0),
                                 color=(1, 1, 1), 
                                 colorSpace='rgb')
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

play_sequence(FREQS, TONE_LEN, target, n_tones):
    tone_nums = []
    freqs = []
    marks = []
    is_targets = []
    
    n_targets = 0
    for tone_num in range(0, n_tones + 1):
        print(tone_num)

        # select next tone
        index = np.random.randint(0, len(FREQS))
        freq = FREQS[index]
        mark = index + 1
        snd = Sound(freq, secs = TONE_LEN)
        
        # increment
        if freq == target:
            is_target = 1
            n_targets += 1

        # schedule sound
        now = GetSecs()
        snd.play(when = now + 0.1)
        WaitSecs(TONE_LEN)
        marker.send(mark)
        
        # add jitter between TRIALS
        WaitSecs(TONE_LEN + np.random.uniform(-0.1, 0.09))

        # save tone info
        tone_nums.append(tone_num)
        freqs.append(freq)
        marks.append(mark)
        is_targets.append(is_target)
        
    return(tone_nums, freqs, marks, is_targets, n_targets)

broadcast(N_TONES, var):
    if not isinstance(var, list)
        broadcasted_array = [var]*N_TONES
    return(broadcasted_array)

write_log(LOG, N_TONES, SEED, SUB_NUM, BLOCK_NUM, seq_num, tone_num, freq, mark, is_target, n_targets, target, score):
    d = {
        'seed': broadcast(N_TONES, SEED),
        'sub_num': broadcast(N_TONES, SUB_NUM),
        'block_num': broadcast(N_TONES, BLOCK_NUM),
        'seq_num': broadcast(N_TONES, seq_num),
        'tone_num' : tone_nums,
        'freq': freqs,
        'mark': marks,
        'is_target': is_targets,
        'n_targets': broadcast(N_TONES, n_targets),
        'target': broadcast(N_TONES, target),
        'score': broadcast(N_TONES, score),
        }
    df = pd.DataFrame(data = d)
    df.to_csv(LOG, mode='a')

ready():
    block_begin = visual.TextStim(mywin, 
                                  text = "Press 'enter' to begin! Please count \
                                  how many times you hear the target tone.",
                                  pos=(0.0, 0.0),
                                  color=(1, 1, 1), 
                                  colorSpace='rgb')
    block_begin.draw()
    mywin.flip()
            
get_response():
    # have subj report how many times TARGET was heard
    keys = kb.getKeys()
    target_info = {"Number of times target played:": ""}
    tidlg = DlgFromDict(target_info)
    response = target_info['Number of times target played:']
    return(response)

is_correct(N_TARGETS, RESPONSE):
    if abs(N_TARGETS - RESPONSE) <= 2:
        correct = 1
    else:
        correct = 0 
    return(correct)

get_score(SCORE_NEEDED, current_score, correct):
    if correct:
        current_score += 1
        correct = visual.TextStim(mywin, 
                                  text = f"Your score is now {current_score}/{SCORE_NEEDED}",
                                  pos=(0.0, 0.0), 
                                  color=(1, 1, 1), 
                                  colorSpace='rgb'
                                 )
    return(current_score)

