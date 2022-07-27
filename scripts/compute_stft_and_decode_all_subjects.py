#!/usr/bin/env python3

import subprocess
import argparse
import compute_stft_and_decode
from bids import BIDSLayout
from util.io.iter_BIDSPaths import *

# import mne
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd

# from scipy import signal
# from typing import Tuple, Iterator
# from mne_bids import BIDSPath, read_raw_bids, print_dir_tree
# from util.io.iter_BIDSPaths import *
# from util.io.bids import DataSink
# from mne.time_frequency import stft

# from sklearn.pipeline import make_pipeline
# from sklearn import preprocessing
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LogisticRegression
# from mne.decoding import SlidingEstimator, cross_val_multiscore

def main(subs, skips):
    BIDS_ROOT = '../data/bids'
    layout = BIDSLayout(BIDS_ROOT, derivatives = True)
    fpaths = layout.get(scope = 'preprocessing',
                    res = 'hi',
                    suffix='epo',
                    extension = 'fif.gz',
                    return_type = 'filename')
    
    for (fpath, sub, task, run) in iter_BIDSPaths(fpaths):
        # if subs were given but sub is not in subs, don't preprocess
        if bool(subs) and sub not in subs:
            continue
        # if sub in skips, don't preprocess
        if sub in skips:
            continue
        
        # Compute stft and decode
        subprocess.check_call("sbatch ./compute_stft_and_decode.py %s %s %s %s" % (fpath, sub, task, run), shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run decoder_2.py over given subjects')
    parser.add_argument('--subs', 
                        type = str, 
                        nargs = '*', 
                        help = 'subjects to decode (e.g. 3 14 8), provide no argument to run over all subjects', 
                        default = [])
    parser.add_argument('--skips', 
                        type = str, 
                        nargs = '*', 
                        help = 'subjects NOT to decode (e.g. 1 9)', 
                        default = [])
    args = parser.parse_args()
    subs = args.subs
    skips = args.skips
    print(f"subs: {subs}, skips : {skips}")
    if bool(subs) & bool(skips):
        raise ValueError('Cannot specify both subs and skips')
    main(subs, skips)
