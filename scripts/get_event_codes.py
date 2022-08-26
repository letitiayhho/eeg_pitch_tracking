#!/usr/bin/env python3

import glob
import subprocess

epoch_paths = glob.glob('../data/bids/derivatives/preprocessing/*/*res-hi*fif.gz')

for path in epoch_paths:
    print(f'subprocess.check_call("sbatch util/io/get_event_codes.py %s" % (path), shell=True)')
    subprocess.check_call("sbatch util/io/get_event_codes.py %s" % (path), shell=True)
