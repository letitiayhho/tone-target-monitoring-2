#!/usr/bin/env python3

#SBATCH --time=00:10:00
#SBATCH --partition=broadwl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=24G
#SBATCH --mail-type=all
#SBATCH --mail-user=letitiayhho@uchicago.edu
#SBATCH --output=logs/compute_stft_and_decode_%j.log

import sys
# import mne
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd

# from scipy import signal
# from mne_bids import BIDSPath, read_raw_bids, print_dir_tree
# from bids import BIDSLayout
# from util.io.iter_BIDSPaths import *
# from util.io.bids import DataSink
from util.io.compute_stft import *
from decoder_2 import * 

def main(fpath, sub, task, run):
    Zxxs, events = compute_stft(fpath, sub, task, run)
    decoder_2(sub, task, run, Zxxs, events)
    
    return (Zxxs, events)
    
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)
    fpath = sys.argv[1]
    sub = sys.argv[2]
    task = sys.argv[3]
    run = sys.argv[4]
    main(fpath, sub, task, run)
