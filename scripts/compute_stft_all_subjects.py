#!/usr/bin/env python3

import subprocess
import sys
from bids import BIDSLayout
from util.io.iter_BIDSPaths import *

def main() -> None:
    BIDS_ROOT = '../data/bids'
    
    layout = BIDSLayout(BIDS_ROOT, derivatives = True)
    fpaths = layout.get(scope = 'preprocessing',
                    res = 'hi',
                    suffix='epo',
                    extension = 'fif.gz',
                    return_type = 'filename')

    for (fpath, sub, task, run) in iter_BIDSPaths(fpaths):
        subprocess.check_call("sbatch ./compute_stft.py %s %s %s %s" % (fpath, sub, task, run), shell=True)

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print(__doc__)
        sys.exit(1)
    main()
