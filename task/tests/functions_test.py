import pandas as pd
import os.path
import random

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

def get_target(FREQS):
    target = random.choice(FREQS)
    return(target)

def get_n_tones(SEQ_LENS):
    n_tones = random.choice(SEQ_LENS)
    return(n_tones)

def play_sequence(FREQS, TONE_LEN, target, n_tones):
    tone_nums = []
    freqs = []
    marks = []
    is_targets = []
    n_targets = 0

    for tone_num in range(1, n_tones + 1):

        # select next tone
        index = random.randint(0, len(FREQS)-1)
        freq = FREQS[index]
        mark = index + 1

        # increment
        if freq == target:
            is_target = 1
            n_targets += 1
        else:
            is_target = 0

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
