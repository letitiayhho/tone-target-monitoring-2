#!/usr/bin/env python3

import subprocess
import argparse
from bids import BIDSLayout
from util.io.iter_BIDSPaths import *

def main(subs, skips) -> None:
    BIDS_ROOT = '../data/bids'
    layout = BIDSLayout(BIDS_ROOT, derivatives = True)
    fpaths = layout.get(scope = 'preprocessing',
                    res = 'hi',
                    suffix='epo',
                    extension = 'fif.gz',
                    return_type = 'filename')
    
    for (fpath, sub, task, run) in iter_BIDSPaths(fpaths):
        # if subs were given but sub is not in subs, don't preprocess
        if bool(subs) and sub not in subs:
            continue
        # if sub in skips, don't preprocess
        if sub in skips:
            continue
        
        # Get stft
        subprocess.check_call("sbatch ./compute_stft.py %s %s %s %s" % (fpath, sub, task, run), shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run compute_stft.py over given subjects')
    parser.add_argument('--subs', 
                        type = str, 
                        nargs = '*', 
                        help = 'subjects to compute stft for (e.g. 3 14 8), provide no argument to run over all subjects', 
                        default = [])
    parser.add_argument('--skips', 
                        type = str, 
                        nargs = '*', 
                        help = 'subjects NOT to stft for (e.g. 1 9)', 
                        default = [])
    args = parser.parse_args()
    subs = args.subs
    skips = args.skips
    print(f"subs: {subs}, skips : {skips}")
    if bool(subs) & bool(skips):
        raise ValueError('Cannot specify both subs and skips')
    main(subs, skips)
