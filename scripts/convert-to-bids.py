#!/usr/bin/env python3

from mne_bids import BIDSPath, write_raw_bids, get_anonymization_daysback
import pandas as pd
import numpy as np
import itertools
import mne
import os
import re

# Constants
DATA_DIR = '../data/raw/' # where our data currently lives
BIDS_DIR = '../data/bids/' # where we want it to live
MAPS_DIR = '../data/captrak/' # where the mapping and electrode location files live



# Parse filenames

# Get filenames and digest them
fnames = os.listdir(DATA_DIR)
fnames = [f for f in fnames if '.vhdr' in f] # filter for .vhdr files

# Get subject list from file order
filt = re.compile('(([0-9]|[1-9][0-9]|[1-9][0-9][0-9]){1,2})')
subs = list(map(lambda x: (re.search(filt, x)).group(0), fnames))
#subs = []
#for strings in fnames:
#    match = re.search('(([0-9]|[1-9][0-9]|[1-9][0-9][0-9]){1,2})', string)
#    subs.append(match.group(0))
#filter_subs = re.compile('letty_subj_(\w?).*') # create regex filter
#subs = list(map(filter_subs.findall, fnames)) # extract subject numbers with filter
#subs = list(itertools.chain(*subs)) # flatten then nested list

# Get a task list
tasks = ['pitch']*len(subs) # broadcast the only task name

# Get a run list
filter_runs = re.compile('\w+[0-9]_([0-9]).*')
runs = list(map(filter_runs.findall, fnames))
runs = ['1' if x == [] else x for x in runs]
runs = list(itertools.chain(*runs))



# Retrieve mappings between channel numbers and channel names

# For subj 2, 3, 5, 6
mapping_table = pd.read_csv(MAPS_DIR + 'pitch_tracking_64_at_IZ.csv')
mapping_64_at_IZ = {mapping_table.number[i]: mapping_table.name[i] for i in range(len(mapping_table))}

# For subj 4 IZ is excluded but channel 64 is not moved to FCZ
mapping_table = pd.read_csv(MAPS_DIR + 'pitch_tracking_no_IZ.csv')
mapping_no_IZ = {mapping_table.number[i]: mapping_table.name[i] for i in range(len(mapping_table))}

# For subj 7, and onwards
mapping_table = pd.read_csv(MAPS_DIR + 'pitch_tracking_64_at_FCZ.csv')
mapping_64_at_FCZ = {mapping_table.number[i]: mapping_table.name[i] for i in range(len(mapping_table))}

# Create dict for subjects and their mappings
special_mappings = {'2': mapping_64_at_IZ,
           '3': mapping_64_at_IZ,
           '4': mapping_no_IZ,
           '5': mapping_64_at_IZ,
           '6': mapping_64_at_IZ,
           }

# Create function to fetch correct mapping
def get_mapping(sub, special_mappings):
    if sub in special_mappings.keys():
        mapping = special_mappings[sub]
    else:
        mapping = mapping_64_at_FCZ
    return mapping



# Run conversion on all files

for i in range(len(fnames)):
    sub = subs[i]
    task = tasks[i]
    run = runs[i]
    fpath = os.path.join(DATA_DIR, fnames[i])
    print(fpath)

    # load data with MNE function for your file format
    raw = mne.io.read_raw_brainvision(fpath)
    raw.load_data()
    raw.set_channel_types({'Aux1': 'stim'})

    # add some info BIDS will want
    raw.info['line_freq'] = 60 # the power line frequency in the building we collected in

    # map channel numbers to channel names
    mapping = get_mapping(sub, special_mappings)
    raw.rename_channels(mapping)
    raw.add_reference_channels(ref_channels = ['Cz'])

    # map channels to their coordinates
    dig = mne.channels.read_dig_captrak(MAPS_DIR + 'subj_' + sub + '.bvct')
    raw.set_montage(dig, on_missing = 'warn')

    # # drop meaningless event name
    events, event_ids = mne.events_from_annotations(raw)
    events = events[events[:,2] != event_ids['New Segment/'], :]

    # # rename events to their stimulus pitch
    event_codes = events[:,2]
    baseline_code = np.argmax(np.bincount(event_codes)) # the one with more trials
    event_names = {1: '50', 2: '100', 3: '150', 4: '200', 5: '250'}
    annot = mne.annotations_from_events(events, sfreq = raw.info['sfreq'], event_desc = event_names)
    raw.set_annotations(annot)

    # build appropriate BIDS directory structure
    bids_path = BIDSPath(
        run = run,
        subject = sub,
        task = task,
        datatype = 'eeg',
        root = BIDS_DIR
    )

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
