import pandas as pd
import os.path
import random

from psychopy import prefs
prefs.hardware['audioLib'] = ['ptb']
from psychopy.sound.backend_ptb import SoundPTB as Sound
from events import EventMarker
from psychopy import visual, core, event
from psychtoolbox import GetSecs, WaitSecs

def open_log(SUB_NUM, BLOCK_NUM):
    log = "data/logs/subj_" + SUB_NUM + "_block_" + BLOCK_NUM + ".log"
    
    if not os.path.isfile(log): # create log file if it doesn't exist
        print(f"Creating {log}")
        d = {
            'seed': [],
            'sub_num': [],
            'block_num': [],
            'seq_num': [],
            'target': [],
            'tone_num' : [],
            'freq': [],
            'mark': [],
            'is_target': [],
            'n_targets': [],
            'response': [],
            'correct': [],
            'score': [],
            }
        print(d)
        df = pd.DataFrame(data = d)
        df.to_csv(log, mode='w', index = False)
    return(log)

def get_score(LOG):
    log = pd.read_csv(LOG)
    scores = log['score']
    if len(scores) == 0:
        score = 0
    else:
        score = scores.iloc[-1]
    score = int(score)
    return(score)

def get_seq_num(LOG):
    log = pd.read_csv(LOG)
    seq_nums = log['seq_num']
    if len(seq_nums) == 0:
        seq_num = 0
    else:
        seq_num = seq_nums.iloc[-1]
    seq_num = int(seq_num)
    return(seq_num)

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

def play_target(WIN, TONE_LEN, target):
    t_snd = Sound(target, secs = TONE_LEN)
    
    target_text = visual.TextStim(WIN, 
                                  text = "Press 'space' to hear the target tone. Press 'enter' to continue",
                                  pos=(0.0, 0.0),
                                  color=(1, 1, 1), 
                                  colorSpace='rgb')
    target_text.draw()
    WIN.flip()
    while True:
        keys = event.getKeys(keyList = ['space', 'return'])
        if 'space' in keys:
            t_snd.play()
        elif 'return' in keys: 
            break

def ready(WIN):
    block_begin = visual.TextStim(WIN, 
                                  text = "Please count how many times you hear the target tone. Press 'enter' to begin!",
                                  pos=(0.0, 0.0),
                                  color=(1, 1, 1), 
                                  colorSpace='rgb')
    block_begin.draw()
    WIN.flip()
    event.waitKeys(keyList = ['return'])
    WIN.flip()

def play_sequence(FREQS, TONE_LEN, target, n_tones):
    tone_nums = []
    freqs = []
    marks = []
    is_targets = []
    n_targets = 0

    for tone_num in range(1, n_tones + 1):
        print(tone_num, end = ', ', flush = True)

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
        WaitSecs(0.1)
#         marker.send(mark) CHANGE THIS
        WaitSecs(TONE_LEN - 0.1)
        
        # add jitter between TRIALS
        WaitSecs(TONE_LEN + random.uniform(-0.1, 0))

        # save tone info
        tone_nums.append(tone_num)
        freqs.append(freq)
        marks.append(mark)
        is_targets.append(is_target)
    
    print('')
    return(tone_nums, freqs, marks, is_targets, n_targets)

def broadcast(n_tones, var):
    if not isinstance(var, list):
        broadcasted_array = [var]*n_tones
    return(broadcasted_array)

def write_log(LOG, n_tones, SEED, SUB_NUM, BLOCK_NUM, seq_num, target, tone_nums, 
              freqs, marks, is_targets, n_targets, response, correct, score):
    print("Writing to log file")
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
    df.to_csv(LOG, mode='a', header = False, index = False)
            
def get_response(WIN):
    # Prompt response
    ask_response = visual.TextStim(WIN, 
                      text = "How many times did you hear the target tone?",
                      pos=(0.0, 0.0),
                      color=(1, 1, 1), 
                      colorSpace='rgb')
    ask_response.draw()
    WIN.flip()

    # Fetch response
    keylist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'return', 'backspace']
    response = []
    response_text = ''

    while True:
        keys = event.getKeys(keyList = keylist)
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
            WIN.flip()
            show_response = visual.TextStim(WIN,
                                           text = response_text,
                                           pos=(0.0, 0.0),
                                           color=(1, 1, 1), 
                                           colorSpace='rgb')
            show_response.draw()
            WIN.flip()
            
    response = int(response_text)
    return(response)

def update_score(WIN, n_targets, response, score, SCORE_NEEDED):
    if abs(n_targets - response) == 0:
        correct = 2
        score += 1
        update = visual.TextStim(WIN, 
                  text = f"You are correct! There were {n_targets} targets. Your score is now {score}/{SCORE_NEEDED}. Press 'enter' to continue.",
                  pos=(0.0, 0.0), 
                  color=(1, 1, 1), 
                  colorSpace='rgb'
                 )
    elif abs(n_targets - response) < 2:
        correct = 1
        score += 1
        update = visual.TextStim(WIN, 
                  text = f"Close enough! There were {n_targets} targets. Your score is now {score}/{SCORE_NEEDED}. Press 'enter' to continue.",
                  pos=(0.0, 0.0), 
                  color=(1, 1, 1), 
                  colorSpace='rgb'
                 )
    else:
        correct = 0 
        update = visual.TextStim(WIN, 
                  text = f"There were {n_targets} targets. \
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
    
    event.waitKeys(keyList = ['return'])

    return(correct, score)



