#!/usr/bin/env python3

#SBATCH --time=00:05:00
#SBATCH --partition=broadwl
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=all
#SBATCH --mail-user=letitiayhho@uchicago.edu
#SBATCH --output=logs/coherence_%j.log

import sys
from mne_bids import BIDSPath, read_raw_bids
from bids import BIDSLayout
from util.io.coherence import *
from util.io.iter_BIDSPaths import *

def main(FPATH, SUB, TASK, RUN, METHOD):
    BIDS_ROOT = '../data/bids'
    FIGS_ROOT = '../figs'
    DERIV_ROOT = '../data/bids/derivatives'
    FS = 5000
    RAW_TMIN = -0.2
    RAW_TMAX = 0.5
    TMIN = 0
    TMAX = 0.25
    N_CHANS = 62
    CONDS = ['50', '100', '150', '200', '250']
    
    # Load epoched data
    epochs = mne.read_epochs(FPATH, preload = True)
    events = epochs.events
    n_epochs = len(events)
    
    # Use a different sub for generating stim channels if sub has bad Aux channel
    STIM_SUB, STIM_RUN = get_stim_sub(SUB, RUN)
    
    # Create epochs from raw data to create simulated stim channels
    raw_epochs = get_raw_epochs(BIDS_ROOT, STIM_SUB, TASK, STIM_RUN)
    stim_epochs_array = create_stim_epochs_array(raw_epochs, n_epochs, CONDS)
    plot_stim_chans(FIGS_ROOT, SUB, RUN, RAW_TMIN, RAW_TMAX, stim_epochs_array)
    simulated_epochs = create_stim_epochs_object(stim_epochs_array, events, CONDS, FS, RAW_TMIN)

    # Crop data so both epoch objects have same windowing
    simulated_epochs = simulated_epochs.crop(tmin = TMIN, tmax = TMAX)
    epochs = epochs.crop(tmin = TMIN)

    # Add simulated channels to data
    combined_epochs = mne.epochs.add_channels_epochs([epochs, simulated_epochs])
    
    # Compute coherence
    indices = get_coh_indices(N_CHANS)
    fmin, fmax = get_fmin_and_fmax(CONDS)
    coh_df = pd.DataFrame()
    for cond in CONDS:
        coh = get_coh(cond, combined_epochs, indices, fmin, fmax, CONDS, FS, METHOD)
        coh = clean_coh(coh, N_CHANS)
        cond_coh_df = create_coh_df(coh, cond, CONDS, N_CHANS, SUB)
        coh_df = pd.concat([coh_df, cond_coh_df])
    coh_df = coh_df.reset_index()

    # Write to pickle
    pickle_fp = f"{DERIV_ROOT}/coherence/subj-{SUB}_task-{TASK}_run-{RUN}_{METHOD}-by-condition.pkl"
    print(f"Writing coherence output to {pickle_fp}")
    coh_df.to_pickle(pickle_fp)
    
__doc__ = "Usage: ./coherence.py <fname> <sub> <task> <run> <method>, method is 'coh' or 'imcoh' etc."
    
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(__doc__)
        sys.exit(1)
    FPATH = sys.argv[1]
    SUB = sys.argv[2]
    TASK = sys.argv[3]
    RUN = sys.argv[4]
    METHOD = sys.argv[5]
    main(FPATH, SUB, TASK, RUN, METHOD)