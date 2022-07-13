#!/usr/bin/env python3

#SBATCH --time=00:05:00
#SBATCH --partition=broadwl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=all
#SBATCH --mail-user=letitiayhho@uchicago.edu
#SBATCH --output=logs/compute_stft_%j.log

import sys
import mne
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from scipy import signal
from mne_bids import BIDSPath, read_raw_bids, print_dir_tree
from bids import BIDSLayout
from util.io.iter_BIDSPaths import *
from util.io.bids import DataSink
from util.io.compute_stft import *

def main(fpath, sub, task, run):
    DERIV_ROOT = '../data/bids/derivatives'
    FS = 5000
    CONDITION_FREQS = [50, 100, 150, 200, 250]
    
    # Read data
    epochs = mne.read_epochs(fpath)
    events = epochs.events
    epochs = epochs.get_data()
    
    # Get metadata
    n_freqs = len(CONDITION_FREQS)
    n_epochs = np.shape(epochs)[0]
    n_chans = np.shape(epochs)[1]
    
    # Compute stft across all channels
    Zxxs = np.empty([n_epochs, n_chans, n_freqs, 19]) # n_epochs, n_chans, n_freqs, n_windows
    for chan in range(n_chans):
        x = pd.DataFrame(epochs[:, chan, :])
        f, t, Zxx = get_stft_for_one_channel(x, FS, n_epochs, CONDITION_FREQS)
        Zxxs[:, chan, :, :] = Zxx
        
    # Reshape for decoder
    Zxxs = Zxxs.reshape((n_epochs, n_freqs*n_chans, 19)) # n_epochs, n_freqs*n_chans, n_windows

    # Save powers and events
    sink = DataSink(DERIV_ROOT, 'decoding')
    stft_fpath = sink.get_path(
        subject = sub,
        task = task,
        run = run,
        desc = 'stft',
        suffix = 'power',
        extension = 'npy',
    )
    print('Saving scores to: ' + stft_fpath)
    np.save(stft_fpath, Zxxs)
        
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