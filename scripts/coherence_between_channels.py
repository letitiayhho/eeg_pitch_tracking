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

def main(FPATH, SUB, TASK, RUN, METHOD, SAVE_FP):
    BIDS_ROOT = '../data/bids'
    FIGS_ROOT = '../figs'
    DERIV_ROOT = '../data/bids/derivatives'
    FS = 5000
    TMIN = 0
    TMAX = 0.25
    N_CHANS = 62
    CONDS = ['50', '100', '150', '200', '250']
    
    # Load epoched data
    epochs = mne.read_epochs(FPATH, preload = True)
    events = epochs.events
    n_epochs = len(events)
    
    # Crop data
    epochs = epochs.crop(tmin = TMIN, tmax = TMAX)

    # Compute coherence
    indices = get_coh_indices(N_CHANS)
    fmin, fmax = get_fmin_and_fmax(CONDS)
    coh_df = pd.DataFrame()
    for cond in CONDS:
        coh = get_coh(cond, combined_epochs, indices, fmin, fmax, CONDS, FS, METHOD)
        coh = clean_coh(coh, CONDS, N_CHANS)
        cond_coh_df = create_coh_df(coh, cond, CONDS, N_CHANS, SUB)
        coh_df = pd.concat([coh_df, cond_coh_df])
    coh_df = coh_df.reset_index()

    # Write to pickle
    print(f"Writing coherence output to {SAVE_FP}")
    coh_df.to_pickle(SAVE_FP)
    
__doc__ = "Usage: ./coherence.py <fname> <sub> <task> <run> <method>, method is 'coh' or 'imcoh' etc."
    
if __name__ == "__main__":
    if len(sys.argv) != 7:
        print(__doc__)
        sys.exit(1)
    FPATH = sys.argv[1]
    SUB = sys.argv[2]
    TASK = sys.argv[3]
    RUN = sys.argv[4]
    METHOD = sys.argv[5]
    SAVE_FP = sys.argv[6]
    main(FPATH, SUB, TASK, RUN, METHOD, SAVE_FP)
