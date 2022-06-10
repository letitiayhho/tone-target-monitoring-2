#!/usr/bin/env python3

import subprocess
import sys
from util.io.iter_BIDSPaths import *

def main() -> None:
    BIDS_ROOT = '../data/bids'

    for (fpath, sub, task, run) in iter_BIDSPaths(BIDS_ROOT, False):
        subprocess.check_call("sbatch ./preprocess.py %s %s %s" % (sub, task, run), shell=True)

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print(__doc__)
        sys.exit(1)
    main()
