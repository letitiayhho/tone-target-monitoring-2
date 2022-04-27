#!/usr/bin/env python3

import numpy as np
import os.path as op
from pprint import pformat
from typing import Tuple, Iterator
import time

# EEG utilities
import mne
from mne.preprocessing import ICA, create_eog_epochs
from pyprep.prep_pipeline import PrepPipeline
from autoreject import get_rejection_threshold, validation_curve

# BIDS utilities
from mne_bids import BIDSPath, read_raw_bids
from util.io.bids import DataSink
from bids import BIDSLayout
import util.io.preprocessing

def main(sub, task, runs) -> None:
    # Constants
    BIDS_ROOT = '../data/bids'
    DERIV_ROOT = '../data/bids/derivatives'
    LOWPASS = 300
    FS = 2000

    # Import data
    print("---------- Import data ----------")
    bids_path = get_bids_path(BIDS_ROOT, sub, task, run)
    print(bids_path)
    if not bids_path.fpath.is_file(): # skip if file doesn't exist
        continue
    raw = import_bids_data(bids_path)
    events, event_ids = read_events(raw)

    # Create virtual EOGs
    raw.load_data()
    raw = create_eogs(raw)

    if sub == '4':
        raw = raw.drop_channels(['Ch64']) # drop channel with no coordinates for sub 4

    # Resampling and PREP
    print("---------- Resampling and PREP ----------")
    raw, events = resample(raw, FS, events)
    raw, bads = run_PREP(raw, sub, run, LOWPASS)

    # Run ICA on one copy of the data
    print("---------- Run ICA on one copy of the data ----------")
    raw_for_ica = bandpass(raw, None, 1)
    raw = bandpass(raw, 270, 30)

    epochs_for_ica = epoch(raw_for_ica)
    epochs = epoch(raw)

    ica = compute_ICA(epochs_for_ica) # run ICA on less aggressively filtered data
    epochs, ica = apply_ICA(epochs_for_ica, epochs) # apply ICA on more aggressively filtered data

    # Baseline correct and reject trials
    print("---------- Baseline correct and reject trials ----------")
    epochs = baseline_correct(epochs)
    epochs, thres = reject_trials(epochs)

    # Save results and generate report
    print("---------- Save results and generate report ----------")
    fpath, sink = get_save_path(DERIV_ROOT, sub, task, run)
    save_preprocessed_data(fpath, epochs)
    generate_report(fpath, sink, epochs, ica, bads, thres)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    sub = sys.argv[1]
    task = sys.argv[2]
    runs = sys.argv[3]
    main(sub, task, runs)