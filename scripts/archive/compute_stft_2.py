#SBATCH --time=00:04:00
#SBATCH --partition=broadwl
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=all
#SBATCH --mail-user=letitiayhho@uchicago.edu
#SBATCH --output=logs/stft_%j.log

import sys
import numpy as np
import mne
import pandas as pd
from scipy import signal
from scipy import signal
from util.io.bids import DataSink
from util.io.stft import *

def main(fpath, sub, task, run):
    DERIV_ROOT = '../data/bids/derivatives'
    FS = 5000
    CONDITION_FREQS = [50, 100, 150, 200, 250]
    
    # Read data
    epochs = mne.read_epochs(fpath)
    print("events read")
    events = epochs.events
    epochs = epochs.get_data()
    
    # Get metadata
    n_freqs = len(CONDITION_FREQS)
    n_epochs = np.shape(epochs)[0]
    n_chans = np.shape(epochs)[1]
    
    # Compute stft across all channels
    Zxxs = np.empty([n_epochs, n_chans, n_freqs, 19]) # n_epochs, n_chans, n_freqs, n_windows
    for chan in range(n_chans):
        x = pd.DataFrame(epochs[:, chan, :])
        f, t, Zxx = get_stft_for_one_channel(x, FS, n_epochs, CONDITION_FREQS)
        Zxxs[:, chan, :, :] = Zxx

    # Save powers and events
    sink = DataSink(DERIV_ROOT, 'decoding')
    stft_fpath = sink.get_path(
        subject = sub,
        task = task,
        run = run,
        desc = 'stft',
        suffix = 'power',
        extension = 'npy',
    )
    print('Saving scores to: ' + stft_fpath)
    np.save(stft_fpath, Zxxs)
        
    return (Zxxs, events)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)
    FPATH = sys.argv[1]
    SUB = sys.argv[2]
    TASK = sys.argv[3]
    RUN = sys.argv[4]
    main(FPATH, SUB, TASK, RUN)
