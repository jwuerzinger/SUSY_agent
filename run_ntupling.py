#!/usr/bin/env python
"""Standalone ntupling script for scan directories that have model files but no ntuple."""

import os
import sys
import glob
import yaml

# Need Run3ModelGen on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Run3ModelGen', 'source'))
from Run3ModelGen.ntupling import mkntuple


# Map scan type to config file
SCAN_CONFIGS = {
    'phase1': 'configs/phase1_flat_config.yaml',
    'phase2a': 'configs/phase2a_ewkino_config.yaml',
    'phase2b': 'configs/phase2b_stop_config.yaml',
    'phase2c': 'configs/phase2c_slepton_config.yaml',
    'phase2d': 'configs/phase2d_compressed_config.yaml',
    'phase3a': 'configs/phase3a_bino_coannihilation_config.yaml',
    'phase3b': 'configs/phase3b_afunnel_config.yaml',
    'phase3c': 'configs/phase3c_compressed_stop_config.yaml',
}

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def get_num_models(scan_dir):
    """Determine num_models from the actual files in the input directory."""
    input_dir = os.path.join(scan_dir, 'input')
    if not os.path.isdir(input_dir):
        return 0
    model_ids = []
    for f in os.listdir(input_dir):
        if f.endswith('.slha'):
            try:
                model_ids.append(int(f.replace('.slha', '')))
            except ValueError:
                pass
    if not model_ids:
        return 0
    return max(model_ids) + 1


def main():
    scan_dirs = sorted(glob.glob(os.path.join(PROJECT_ROOT, 'scans/phase*/scan_seed*')))

    for scan_dir in scan_dirs:
        # Check if ntuple already exists
        existing = glob.glob(os.path.join(scan_dir, 'ntuple.*.root'))
        if existing:
            print(f"SKIP {scan_dir} — ntuple already exists: {existing[0]}")
            continue

        num_models = get_num_models(scan_dir)
        if num_models == 0:
            print(f"SKIP {scan_dir} — no models found")
            continue

        # Determine scan type from path
        phase = None
        for key in SCAN_CONFIGS:
            if key in scan_dir:
                phase = key
                break
        if phase is None:
            print(f"SKIP {scan_dir} — unknown scan type")
            continue

        config_path = os.path.join(PROJECT_ROOT, SCAN_CONFIGS[phase])
        with open(config_path) as f:
            config = yaml.safe_load(f)

        steps = config['steps']
        isGMSB = config.get('isGMSB', False)

        actual_count = len(os.listdir(os.path.join(scan_dir, 'input')))
        print(f"NTUPLE {scan_dir} — {actual_count} model files, max ID → num_models={num_models}")

        try:
            mkntuple(steps, scan_dir, num_models, isGMSB)
            print(f"  OK — ntuple created")
        except Exception as e:
            print(f"  FAILED — {e}")


if __name__ == '__main__':
    main()
