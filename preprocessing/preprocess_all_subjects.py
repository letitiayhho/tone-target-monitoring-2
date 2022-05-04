#!/usr/bin/env python3

import subprocess
import sys
from bids import BIDSLayout
from typing import Tuple, Iterator
from util.io.preprocessing import *

def main() -> None:
    # CONSTANTS
    BIDS_ROOT = '../data/bids'

    # Parse BIDS directory
    layout = BIDSLayout(BIDS_ROOT)
    subjects = layout.get_subjects()
    tasks = layout.get_tasks()
    runs = layout.get_runs()
    print(subjects, tasks, runs)

    KeyType = Tuple[str, str, str]

    def fpaths() -> Iterator[KeyType]:
        for sub in subjects:
            for task in tasks:
                for run in runs:
                    run = str(run) # layout.get_runs() doesn't return strings
                    key = (sub, task, run)
                    yield key

    for (sub, task, run) in fpaths():
	bids_path = get_bids_path(BIDS_ROOT, sub, task, run)
	if bids_path.fpath.is_file():
		subprocess.check_call("sbatch ./preprocess.py %s %s %s" % (sub, task, run), shell=True)

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print(__doc__)
        sys.exit(1)
    main()
