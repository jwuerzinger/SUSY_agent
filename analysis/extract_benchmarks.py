#!/usr/bin/env python
"""Extract benchmark SLHA files for each physics category.

Identifies the best benchmark model per category from the final classification,
then copies the SPheno SLHA file to results/benchmarks/.
"""

import uproot
import awkward as ak
import numpy as np
import os
import sys
import glob
import shutil
import re

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results', 'benchmarks')
os.makedirs(RESULTS_DIR, exist_ok=True)

# Import classification logic
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from final_classification import (
    REQUIRED_FIELDS, apply_all_cuts, classify_model, find_benchmarks
)

# Physics cut values (duplicated for completeness)
HIGGS_MASS_LOW = 122.0
HIGGS_MASS_HIGH = 128.0
OMEGA_UPPER = 0.132
BSG_CENTRAL = 3.32e-4
BSG_SIGMA = 0.33e-4
BSMUMU_CENTRAL = 3.09e-9
BSMUMU_SIGMA = 0.65e-9
LEP_CHARGINO_MIN = 103.0


def load_ntuples_with_provenance():
    """Load all ntuples, tracking which scan directory each model came from."""
    ntuple_files = sorted(glob.glob(os.path.join(PROJECT_ROOT, 'scans/phase*/*/ntuple.*.root')))
    arrays = []
    provenance = []  # (scan_dir, model_id) for each model

    for f in ntuple_files:
        scan_dir = os.path.dirname(f)
        with uproot.open(f"{f}:susy") as tree:
            available = set(tree.keys())
            fields_to_read = [fld for fld in REQUIRED_FIELDS if fld in available]
            if 'model' not in fields_to_read and 'model' in available:
                fields_to_read.append('model')
            missing = [fld for fld in REQUIRED_FIELDS if fld not in available]
            arr = tree.arrays(fields_to_read, library="ak")
            n = len(arr)
            for fld in missing:
                arr = ak.with_field(arr, np.full(n, -1.0), fld)
            arrays.append(arr)

            # Track provenance
            if 'model' in available:
                model_ids = ak.to_numpy(arr['model']).astype(int)
            else:
                model_ids = np.arange(n)
            for mid in model_ids:
                provenance.append((scan_dir, int(mid)))

    data = ak.concatenate(arrays)
    return data, provenance


def main():
    print("=" * 60)
    print("BENCHMARK EXTRACTION")
    print("=" * 60)

    data, provenance = load_ntuples_with_provenance()
    mask = apply_all_cuts(data)
    passing = data[mask]
    passing_mask = ak.to_numpy(mask)
    passing_provenance = [p for p, m in zip(provenance, passing_mask) if m]

    print(f"{len(passing)} models pass all cuts")

    # Classify and find benchmarks
    all_categories = []
    for i in range(len(passing)):
        cats = classify_model(passing[i])
        all_categories.append(cats)

    benchmarks = find_benchmarks(passing, all_categories)

    print(f"\nExtracting {len(benchmarks)} benchmark SLHA files:\n")

    extracted = 0
    for cat, (idx, score) in sorted(benchmarks.items()):
        scan_dir, model_id = passing_provenance[idx]
        slha_path = os.path.join(scan_dir, 'SPheno', f'{model_id}.slha')

        # Also check for input SLHA
        input_slha = os.path.join(scan_dir, 'input', f'{model_id}.slha')

        p = passing[idx]
        lsp_names = {1: 'Bino', 2: 'Wino', 3: 'Higgsino'}
        lsp_type = int(p['SP_LSP_type'])
        m_lsp = abs(float(p['SP_m_chi_10']))

        # Sanitize category name for filename
        safe_cat = cat.replace('+', '_plus_').replace(' ', '_')
        out_name = f"benchmark_{safe_cat}.slha"
        out_path = os.path.join(RESULTS_DIR, out_name)

        source_file = None
        if os.path.exists(slha_path):
            source_file = slha_path
        elif os.path.exists(input_slha):
            source_file = input_slha

        if source_file:
            shutil.copy2(source_file, out_path)
            print(f"  [{cat}] m(LSP)={m_lsp:.0f} GeV ({lsp_names.get(lsp_type, '?')})")
            print(f"    Source: {source_file}")
            print(f"    → {out_path}")
            extracted += 1
        else:
            print(f"  [{cat}] SLHA not found: tried {slha_path}")

    # Also write a summary CSV
    summary_path = os.path.join(RESULTS_DIR, 'benchmark_summary.csv')
    with open(summary_path, 'w') as f:
        f.write("category,scan_dir,model_id,lsp_type,m_lsp,m_chi1p,m_chi20,m_t1,m_b1,m_eL,m_eR,omega,mh_fh,smodels_r\n")
        for cat, (idx, score) in sorted(benchmarks.items()):
            scan_dir, model_id = passing_provenance[idx]
            p = passing[idx]
            lsp_type = int(p['SP_LSP_type'])
            m_lsp = abs(float(p['SP_m_chi_10']))
            m_chi1p = abs(float(p['SP_m_chi_1p']))
            m_chi20 = abs(float(p['SP_m_chi_20']))
            m_t1 = abs(float(p['SP_m_t_1']))
            m_b1 = abs(float(p['SP_m_b_1']))
            m_eL = abs(float(p['SP_m_e_L']))
            m_eR = abs(float(p['SP_m_e_R']))
            omega = float(p['MO_Omega'])
            mh = float(p['FH_m_h'])
            sm_tp = float(p['SModelS_bestExpUL_TheoryPrediction'])
            sm_ul = float(p['SModelS_bestExpUL_UpperLimit'])
            r = sm_tp / sm_ul if sm_tp > 0 and sm_ul > 0 else 0.0
            f.write(f"{cat},{os.path.basename(scan_dir)},{model_id},{lsp_type},{m_lsp:.1f},{m_chi1p:.1f},{m_chi20:.1f},{m_t1:.1f},{m_b1:.1f},{m_eL:.1f},{m_eR:.1f},{omega:.4f},{mh:.1f},{r:.3f}\n")

    print(f"\n{extracted}/{len(benchmarks)} SLHA files extracted to {RESULTS_DIR}/")
    print(f"Summary CSV: {summary_path}")


if __name__ == '__main__':
    main()
