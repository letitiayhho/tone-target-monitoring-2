#!/usr/bin/env python3

from mne_bids import BIDSPath, write_raw_bids, get_anonymization_daysback
import pandas as pd
import numpy as np
import itertools
import mne
import os
import re
from util.io.get_chan_mapping import get_chan_mapping
from util.io.iter_raw_paths import iter_raw_paths

# Constants

DATA_DIR = '../data/raw/' # where our data currently lives
BIDS_DIR = '../data/bids/' # where we want it to live
MAPS_DIR = '../data/captrak/' # where the mapping and electrode location files live

# Run conversion on all files

for (fname, sub, task, run) in iter_raw_paths(DATA_DIR):

    # create output file name
    bids_path = BIDSPath(
        run = run,
        subject = sub,
        task = task,
        datatype = 'eeg',
        root = BIDS_DIR
    )
    if os.path.isfile(bids_path):
        print(f'File {bids_path} exists, skipping {fname}')
        continue
    
    # load data with MNE function for your file format
    fpath = os.path.join(DATA_DIR, fname)
    print(fpath)
    raw = mne.io.read_raw_brainvision(fpath)
    raw.load_data()
    raw.set_channel_types({'Aux1': 'stim'})

    # add some info BIDS will want
    raw.info['line_freq'] = 60 # the power line frequency in the building we collected in

    # map channel numbers to channel names
    mapping = get_chan_mapping(MAPS_DIR, sub)
    raw.rename_channels(mapping)
    raw.add_reference_channels(ref_channels = ['Cz'])

    # map channels to their coordinates
    dig = mne.channels.read_dig_captrak(MAPS_DIR + 'subj-' + sub + '.bvct')
    raw.set_montage(dig, on_missing = 'warn')

    # drop meaningless event name
    events, event_ids = mne.events_from_annotations(raw)
    events = events[events[:,2] != event_ids['New Segment/'], :]

    # rename events to their stimulus pitch
    event_codes = events[:,2]
    baseline_code = np.argmax(np.bincount(event_codes)) # the one with more trials
    event_names = {1: '50', 2: '100', 3: '150', 4: '200', 5: '250'}
    annot = mne.annotations_from_events(events, sfreq = raw.info['sfreq'], event_desc = event_names)
    raw.set_annotations(annot)


    # get range of dates the BIDS specification will accept
    daysback_min, daysback_max = get_anonymization_daysback(raw)

    # write data into BIDS directory, while anonymizing
    write_raw_bids(
        raw,
        bids_path = bids_path,
        allow_preload = True, # whether to load full dataset into memory when copying
        format = 'BrainVision', # format to save to
        anonymize = dict(daysback = daysback_min), # shift dates by daysback
        overwrite = True,
    )

# Check output files

from mne_bids import print_dir_tree
print_dir_tree(BIDS_DIR)
