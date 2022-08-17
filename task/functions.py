import pandas as pd
import os.path
import random
import csv
import string

from psychopy import prefs
prefs.hardware['audioLib'] = ['ptb']
from psychopy.sound.backend_ptb import SoundPTB as Sound
from events import EventMarker
from psychopy import visual, core, event


def open_log(SUB_NUM, BLOCK_NUM):
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
    return(log)

def get_seq_num(LOG):
    log = pd.read_csv(LOG)
    seq_nums = log['seq_num']
    if len(seq_nums) == 0:
        seq_num = 0
    else:
        seq_num = seq_nums.iloc[-1]
    return(seq_num)

def get_score(LOG):
    log = pd.read_csv(LOG)
    scores = log['score']
    if len(scores) == 0:
        score = 0
    else:
        score = scores.iloc[-1]
    return(score)

def get_target(FREQS):
    target = random.choice(FREQS)
    return(target)

def get_n_tones(SEQ_LENS):
    n_tones = random.choice(SEQ_LENS)
    return(n_tones)

def fixation(WIN):
    fixation = visual.TextStim(WIN, '+')
    fixation.draw()
    WIN.flip()
    return(fixation)

def play_target(KB, WIN, TONE_LEN, target):
    t_snd = Sound(target, secs = TONE_LEN)
    
    # creds to jared
    target_text = visual.TextStim(WIN, 
                                  text = "Press 'space' to hear the target tone. \
                                  \
                                  Press 'enter' to continue",
                                  pos=(0.0, 0.0),
                                  color=(1, 1, 1), 
                                  colorSpace='rgb')
    target_text.draw()
    WIN.flip()
#     event.waitKeys()
    while True:
        keys = event.getKeys()
        if keys:
            print(keys)
        if 'space' in keys:
            t_snd.play()
        elif 'return' in keys: 
            break

def ready(KB, WIN):
    block_begin = visual.TextStim(WIN, 
                                  text = "Please count how many times you hear the target tone. Press 'enter' to begin!",
                                  pos=(0.0, 0.0),
                                  color=(1, 1, 1), 
                                  colorSpace='rgb')
    block_begin.draw()
    WIN.flip()
    event.waitKeys()
#     while True:
#         keys = event.getKeys()
#         if 'return' in keys: 
#             WIN.flip()
#             break

def play_sequence(FREQS, TONE_LEN, target, n_tones):
    tone_nums = []
    freqs = []
    marks = []
    is_targets = []
    n_targets = 0

    for tone_num in range(0, n_tones + 1):
        print(tone_num)

        # select next tone
        index = random.randint(0, len(FREQS)-1)
        freq = FREQS[index]
        mark = index + 1
        snd = Sound(freq, secs = TONE_LEN)
        
        # increment
        if freq == target:
            is_target = 1
            n_targets += 1
        else:
            is_target = 0

        # schedule sound
        now = GetSecs()
        snd.play(when = now + 0.1)
        WaitSecs(TONE_LEN)
#         marker.send(mark) CHANGE THIS
        
        # add jitter between TRIALS
        WaitSecs(TONE_LEN + random.uniform(-0.1, 0.09))

        # save tone info
        tone_nums.append(tone_num)
        freqs.append(freq)
        marks.append(mark)
        is_targets.append(is_target)
        
    return(tone_nums, freqs, marks, is_targets, n_targets)

def broadcast(n_tones, var):
    if not isinstance(var, list):
        broadcasted_array = [var]*n_tones
    return(broadcasted_array)

def write_log(LOG, n_tones, SEED, SUB_NUM, BLOCK_NUM, seq_num, target, tone_num, 
              freq, mark, is_target, n_targets, response, correct, score):
    d = {
        'seed': broadcast(n_tones, SEED),
        'sub_num': broadcast(n_tones, SUB_NUM),
        'block_num': broadcast(n_tones, BLOCK_NUM),
        'seq_num': broadcast(n_tones, seq_num),
        'target': broadcast(n_tones, target),
        'tone_num' : tone_nums,
        'freq': freqs,
        'mark': marks,
        'is_target': is_targets,
        'n_targets': broadcast(n_tones, n_targets),
        'response': broadcast(n_tones, response),
        'correct': broadcast(n_tones, correct),
        'score': broadcast(n_tones, score),
        }
    df = pd.DataFrame(data = d)
    df.to_csv(LOG, mode='a', header=False)
            
def get_response(KB, WIN):
    # Prompt response
    WaitSecs(1)
    ask_response = visual.TextStim(WIN, 
                      text = "How many times did you hear the target tone?",
                      pos=(0.0, 0.0),
                      color=(1, 1, 1), 
                      colorSpace='rgb')
    ask_response.draw()
    WIN.flip()

    # Fetch response
    keyList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'return', 'backspace']
    response = []
    response_text = ''

    while True:
        keys = event.getKeys(keyList = keyList)
        if response_text and 'return' in keys: # empty response not accepted
            break
        elif keys:
            if 'return' in keys:
                None
            elif 'backspace' in keys:
                response = response[:-1]
            else:
                response.append(keys)
            response_text = ''.join([item for sublist in response for item in sublist])
            win.flip()
            print(f'Response: {response_text}')
            show_response = visual.TextStim(win,
                                           text = response_text,
                                           pos=(0.0, 0.0),
                                           color=(1, 1, 1), 
                                           colorSpace='rgb')
            show_response.draw()
            win.flip()
            
    response = int(response_text)
    return(response)

def update_score(WIN, N_TARGETS, RESPONSE, score, SCORE_NEEDED):
    if abs(N_TARGETS - RESPONSE) == 0:
        correct = 2
        score += 1
        update = visual.TextStim(WIN, 
                  text = f"You are correct! There were {N_TARGETS} targets. \
                  \
                  Your score is now {score}/{SCORE_NEEDED}. \
                  \
                  Press 'enter' to continue.",
                  pos=(0.0, 0.0), 
                  color=(1, 1, 1), 
                  colorSpace='rgb'
                 )
    elif abs(N_TARGETS - RESPONSE) < 2:
        correct = 1
        score += 1
        update = visual.TextStim(WIN, 
                  text = f"Close enough! There were {N_TARGETS} targets. \
                  \
                  Your score is now {score}/{SCORE_NEEDED}. \
                  \
                  Press 'enter' to continue.",
                  pos=(0.0, 0.0), 
                  color=(1, 1, 1), 
                  colorSpace='rgb'
                 )
    else:
        correct = 0 
        update = visual.TextStim(WIN, 
                  text = f"There were {N_TARGETS} targets. \
                  \
                  Your score remains {score}/{SCORE_NEEDED}. \
                  \
                  Press 'enter' to continue.",
                  pos=(0.0, 0.0), 
                  color=(1, 1, 1), 
                  colorSpace='rgb'
                 )

    update.draw()
    WIN.flip()
    
    event.waitKeys()
#     while True:
#         keys = KB.getKeys()
#         if 'return' in keys: 
#             WIN.flip()
#             break

    return(correct, score)



