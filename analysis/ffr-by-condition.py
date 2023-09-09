#!/usr/bin/env python3

#SBATCH --time=00:30:00
#SBATCH --partition=bigmem2
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=96 
#SBATCH --mail-type=all
#SBATCH --mail-user=letitiayhho@uchicago.edu
#SBATCH --output=logs/plot-grand-average-ffr_%j.log


from matplotlib import pyplot as plt
from itertools import product
import numpy as np
import pandas as pd
import os.path as op
import argparse
import re
import matplotlib.pyplot as plt
import mne
from scipy import signal
from scipy.fft import fftshift
from bids import BIDSLayout

def read_epochs(sub, desc):
    '''
    reads and concatenates epochs across runs
    '''
    layout = BIDSLayout(BIDS_ROOT, derivatives = True)
    run = lambda f: int(re.findall('run-(\w+)_', f)[0])
    fnames = layout.get(
        return_type = 'filename',
        subject = sub, 
        desc = desc
        )
    print(fnames)
    fnames.sort(key = run)
    epochs_all = [mne.read_epochs(f) for f in fnames]
    epochs = mne.concatenate_epochs(epochs_all)
    epochs = epochs.pick('eeg')
    return epochs

def compute_spectrum_dB(epo):
    '''
    Computes power spectrum of frequency following response
    '''
    poststim = epo.average().compute_psd(tmin = 0., tmax = 0.25)
    baseline = epo.average().compute_psd(tmin = -0.25, tmax = 0.)
    power = 10 * np.log10(poststim.get_data() / baseline.get_data())
    power = np.squeeze(power)
    return poststim.freqs, power

def plot_spectrum_by_condition(sub, evokeds, cond, event_ids):
    # Plot
    x = evokeds[event_ids[0]].get_data()
    x = x.flatten()
    time_step = 1 / fs
    freqs = np.fft.fftfreq(x.size, time_step)
    idx = np.argsort(freqs)
    ps = np.abs(np.fft.fft(x))**2
    plt.plot(freqs[idx], ps[idx], label = "130")

    x = evokeds[event_ids[1]].get_data()
    x = x.flatten()
    ps = np.abs(np.fft.fft(x))**2
    plt.plot(freqs[idx], ps[idx], label = "200")

    x = evokeds[event_ids[2]].get_data()
    x = x.flatten()
    ps = np.abs(np.fft.fft(x))**2
    plt.plot(freqs[idx], ps[idx], label = "280")

    plt.title(f'Target tone: {cond}')
    plt.legend(title = 'Target frequency (Hz)')
    plt.xlabel("Hz")
    plt.ylabel("PSD (V^2/Hz)")
    plt.xlim(0, 300)
    plt.savefig(f'../figs/sub-{sub}_ffr.jpg', dpi = 300, bbox_inches = 'tight')

# Load data
BIDS_ROOT = '../data/bids'
layout = BIDSLayout(BIDS_ROOT, derivatives = True)
subs = layout.get_subjects(scope = 'preprocessing')
subs.sort(key = int)
epochs = []

for sub in subs:
    epochs = read_epochs(sub, 'clean')
    epochs = epochs.pick(['Cz'])
    
    # Average over time domain by condition
    conditions = list(epochs.event_id.keys())
    evokeds = {c:epochs[c].average() for c in conditions}
    
    # Plot
    conditions = {'130': ['11', '21', '31'],
                  '200': ['12', '22', '32'],
                  '280': ['13', '23', '33']}
    for cond, event_ids in condition.items():
        plot_spectrum_by_condition(sub, evokeds, cond, event_ids)
    
    
    
