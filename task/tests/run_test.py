import os
from functions_test import *

# os.chdir('../..')
print(os.getcwd())

FREQS = [130, 200, 280]
SEQ_LENS = [30, 36, 42]
TONE_LEN = 0.1
SUBS = 100
BLOCKS = 5
SEQS = 18

# open log file
LOG = open_log("0", "0")

# bogus filler values
score = 0
response = 0
correct = 0

for SUB_NUM in range(SUBS):
    print(f"SUB: {SUB_NUM}")

    for BLOCK_NUM in range(BLOCKS):
        print(f"BLOCK: {BLOCK_NUM}")

        # play sequences until SCORE_NEEDED is reached
        for seq_num in range(SEQS):

            # set subject number, block and seq_num as seed
            SEED = int(str(SUB_NUM) + "0" + str(BLOCK_NUM) + str(seq_num))
            print("SEED: " + str(SEED))
            random.seed(SEED)
            
            print(f"SEQ_NUM: {seq_num}")
            print(seq_num, end = ', ', flush = True)
            target = get_target(FREQS)
            n_tones = get_n_tones(SEQ_LENS)

            # Play tones
            tone_nums, freqs, marks, is_targets, n_targets = play_sequence(FREQS, TONE_LEN, target, n_tones)

            # Write log file
            write_log(LOG, n_tones, SEED, SUB_NUM, BLOCK_NUM, seq_num, target, tone_nums,
                      freqs, marks, is_targets, n_targets, response, correct, score)
