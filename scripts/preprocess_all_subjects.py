#!/usr/bin/env python3

import subprocess
import sys
import argparse
from util.io.iter_BIDSPaths import *

def main(subs, skips) -> None:
    BIDS_ROOT = '../data/bids'

    for (fpath, sub, task, run) in iter_BIDSPaths(BIDS_ROOT, False):
        # if subs were given but sub is not in subs, don't preprocess
        if bool(subs) and sub not in subs:
            continue
        if sub in skips:
            continue
        #print("sbatch ./preprocess.py {sub} {task} {run}")
        subprocess.check_call("sbatch ./preprocess.py %s %s %s" % (sub, task, run), shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run preprocess.py over given subjects')
    parser.add_argument('--subs', type = str, nargs = '*', help = 'subjects to preprocess (e.g. 3 14 8), provide no argument to run over all subjects', default = [])
    parser.add_argument('--skips', type = str, nargs = '*', help = 'subjects NOT to preprocess (e.g. 1 9)', default = [])
    args = parser.parse_args()
    subs = args.subs
    skips = args.skips
    print(f"subs: {subs}, skips : {skips}")
    if bool(set(subs) & set(skips)):
        overlap = list(set(subs) & set(skips))
        raise ValueError(f'Subs {overlap} in subs and skips')
    main(subs, skips)
