#!/usr/bin/env python
import re
import itertools
from typing import Tuple, Iterator
from mne_bids import BIDSPath, read_raw_bids, print_dir_tree
from bids import BIDSLayout

KeyType = Tuple[str, str, str, str]

def iter_fpaths(bids_root) -> Iterator[KeyType]:
    # Get filepaths
    layout = BIDSLayout(bids_root, derivatives = True)
    fpaths = layout.get(scope = 'preprocessing',
                        extension = 'fif.gz',
                        return_type = 'filename')
    fpaths.pop(0)

    # Get corresponding subject number
    filter_subs = re.compile('sub-(\d)_')
    subs = list(map(filter_subs.findall, fpaths))
    subs = list(itertools.chain(*subs))

    # Get corresponding run number
    filter_runs = re.compile('run-(\d)')
    runs = list(map(filter_runs.findall, fpaths))
    runs = list(itertools.chain(*runs))

    for i in range(len(fpaths)):
        key = (fpaths[i], subs[i], 'tasks', runs[i])
        yield key
