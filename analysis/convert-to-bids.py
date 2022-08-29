#!/usr/bin/env python3

#SBATCH --time=00:02:00
#SBATCH --partition=broadwl
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=48G
#SBATCH --mail-type=all
#SBATCH --mail-user=letitiayhho@uchicago.edu
#SBATCH --output=logs/convert-to-bids_%j.log

from mne_bids import BIDSPath, write_raw_bids, get_anonymization_daysback
import pandas as pd
import numpy as np
import itertools
import mne
import os
import sys
import re
from util.io.get_chan_mapping import get_chan_mapping

def main(fpath, sub, task, run) -> None:
    print(fpath, sub, task, run)

    RAW_DIR = '../data/raw/' # where our data currently lives
    BIDS_DIR = '../data/bids/' # where we want it to live
    MAPS_DIR = '../data/captrak/' # where the mapping and electrode location files live

    # create output file name
    bids_path = BIDSPath(
        run = run,
        subject = sub,
        task = task,
        datatype = 'eeg',
        root = BIDS_DIR
    )
#     if os.path.isfile(bids_path):
#         sys.exit(f'File {bids_path} exists, skipping {fname}')

    # load data with MNE function for your file format
    fpath = os.path.join(RAW_DIR, fpath)
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

    # drop extra 32 channels for subs 23, 24, 25
    if sub in ['23', '24', '25']:
        print(f"Dropping extra channels for sub {sub}!")
        matches = [x for x in raw.ch_names if re.search('Ch', x)]
        raw = raw.drop_channels(matches)
    print(raw.ch_names)
    n_chans = len(raw.ch_names)
    if n_chans != 65:
        sys.exit(f"Incorrect number of channels, there should be 65 (stim incl) channels, instead there are {n_chans} channels")

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

__doc__ = "Usage: ./convert-to-bids.py <fpath> <sub> <task> <run>"

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)
    fpath = sys.argv[1]
    sub = sys.argv[2]
    task = sys.argv[3]
    run = sys.argv[4]
    main(fpath, sub, task, run)

