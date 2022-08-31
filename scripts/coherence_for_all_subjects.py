#!/usr/bin/env python3

import os
import argparse
import subprocess
from util.io.iter_BIDSPaths import *

def main(subs, skips, method) -> None:
    BIDS_ROOT = '../data/bids'
    DERIV_ROOT = '../data/bids/derivatives'

    layout = BIDSLayout(BIDS_ROOT, derivatives = True)
    fpaths = layout.get(scope = 'preprocessing',
                        res = 'hi',
                        suffix='epo',
                        extension = 'fif.gz',
                        return_type = 'filename')

    for (fpath, sub, task, run) in iter_BIDSPaths(fpaths):
        # skip if subs were given but sub is not in subs
        if bool(subs) and sub not in subs:
            continue

        # skip if sub in skips, don't convert
        if sub in skips:
            continue

        # skip if coherence is already computed
        save_fp = f"{DERIV_ROOT}/coherence/subj-{sub}_task-{task}_run-{run}_{method}-by-condition.pkl"
        if os.path.isfile(save_fp) and sub not in subs:
            print(f"Coherence already computed for {sub} run {run}.")
            continue

        print("subprocess.check_call(\"sbatch ./coherence.py %s %s %s %s %s %s\" % (fpath, sub, task, run, method, save_fp), shell=True)")
        subprocess.check_call("sbatch ./coherence.py %s %s %s %s %s %s" % (fpath, sub, task, run, method, save_fp), shell=True)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run coherence.py over given subjects')
    parser.add_argument('method',
                        type = str,
                        nargs = 1,
                        help = 'method for computing coherence (e.g. \'coh\', \'imcoh\' etc.)')
    parser.add_argument('--subs',
                        type = str,
                        nargs = '*',
                        help = 'subjects to convert (e.g. 3 14 8), provide no argument to run over all subjects',
                        default = [])
    parser.add_argument('--skips',
                        type = str,
                        nargs = '*',
                        help = 'subjects NOT to convert (e.g. 1 9)',
                        default = [])
    args = parser.parse_args()
    method = args.method[0]
    subs = args.subs
    skips = args.skips
    print(f"method: {method}, subs: {subs}, skips : {skips}")
    if bool(subs) & bool(skips):
        raise ValueError('Cannot specify both subs and skips')
    main(subs, skips, method)