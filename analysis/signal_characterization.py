#!/usr/bin/env python
"""Signal characterization for ATLAS-invisible pMSSM models.

For each blind-spot model (ATLAS tier 0 or 1), extracts:
1. Production cross-sections from SModelS decomposition
2. Dominant decay chains from SPheno branching fractions
3. Chargino lifetime from SP_w_chi_1p (width in GeV -> ctau in meters)
4. Kinematic characteristics: mass splittings, expected lepton/jet pT ranges

Requires: results/atlas_coverage/model_atlas_coverage.csv (from atlas_coverage.py)
Outputs:  results/atlas_coverage/signal_characterization.csv
"""

import os
import sys
import csv
import numpy as np
import awkward as ak
from collections import defaultdict

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results', 'atlas_coverage')
os.makedirs(RESULTS_DIR, exist_ok=True)

sys.path.insert(0, os.path.dirname(__file__))
from final_classification import REQUIRED_FIELDS, apply_all_cuts, classify_model
from atlas_coverage import parse_smodels_file

import uproot
import glob as globmod

# Physical constants
HBAR_GEV_S = 6.582119569e-25  # hbar in GeV*s
C_M_S = 2.998e8               # speed of light in m/s

# Additional ntuple branches needed for signal characterization
SIGNAL_FIELDS = [
    'SP_w_chi_1p', 'SP_w_chi_20', 'SP_w_chi_2p', 'SP_w_chi_30',
    'SP_w_t_1', 'SP_w_b_1', 'SP_w_e_L', 'SP_w_e_R',
    'SP_BF_chi_1p_to_chi_10', 'SP_BF_chi_1p_other',
    'SP_BF_chi_20_to_chi_10', 'SP_BF_chi_20_to_chi_10_Z',
    'SP_BF_chi_20_to_chi_10_h', 'SP_BF_chi_20_to_chi_1p',
    'SP_BF_chi_20_to_chi_1p_W',
    'SP_BF_t_1_to_chi_10_t', 'SP_BF_t_1_to_chi_1p_b',
    'SP_BF_t_1_to_chi_10_c', 'SP_BF_t_1_to_chi_10_b_W',
    'SP_BF_t_1_to_chi_20', 'SP_BF_t_1_to_chi_10_b',
    'SP_BF_b_1_to_chi_10_b', 'SP_BF_b_1_to_chi_1p_t',
    'SP_BF_b_1_to_chi_1p', 'SP_BF_b_1_to_chi_10',
    'SP_BF_e_L_to_chi_10_ele', 'SP_BF_e_R_to_chi_10_ele',
    'SP_m_chi_30', 'SP_m_chi_40', 'SP_m_chi_2p',
    'SP_m_tau_1', 'SP_m_nu_eL',
    'SP_chi_10_Bino_frac', 'SP_chi_10_Wino_frac', 'SP_chi_10_Higgsino_frac',
    'SP_chi_1p_Wino_frac', 'SP_chi_1p_Higgsino_frac',
]

ALL_FIELDS = list(set(REQUIRED_FIELDS + SIGNAL_FIELDS))


def load_ntuples_extended():
    """Load all ntuples with extended fields for signal characterization."""
    ntuple_files = sorted(globmod.glob(os.path.join(PROJECT_ROOT, 'scans/phase*/*/ntuple.*.root')))
    arrays = []
    provenance = []

    for f in ntuple_files:
        scan_dir = os.path.dirname(f)
        with uproot.open(f"{f}:susy") as tree:
            available = set(tree.keys())
            fields_to_read = [fld for fld in ALL_FIELDS if fld in available]
            if 'model' not in fields_to_read and 'model' in available:
                fields_to_read.append('model')
            missing = [fld for fld in ALL_FIELDS if fld not in available]
            arr = tree.arrays(fields_to_read, library="ak")
            n = len(arr)
            for fld in missing:
                arr = ak.with_field(arr, np.full(n, -1.0), fld)
            arrays.append(arr)

            if 'model' in available:
                model_ids = ak.to_numpy(arr['model']).astype(int)
            else:
                model_ids = np.arange(n)
            for mid in model_ids:
                provenance.append((scan_dir, int(mid)))

    data = ak.concatenate(arrays)
    return data, provenance


def width_to_ctau(width_gev):
    """Convert decay width (GeV) to ctau (meters)."""
    if width_gev <= 0 or width_gev == -1:
        return -1.0
    tau = HBAR_GEV_S / width_gev  # lifetime in seconds
    return tau * C_M_S  # ctau in meters


def get_field(p, name, default=-1.0):
    """Safely get a field from a record, returning default if missing."""
    try:
        val = float(p[name])
        return val
    except (KeyError, ValueError):
        return default


def characterize_model(p, smodels_data):
    """Build signal characterization dict for one model."""
    lsp_type = int(p['SP_LSP_type'])
    m_lsp = abs(float(p['SP_m_chi_10']))
    m_chi1p = abs(float(p['SP_m_chi_1p']))
    m_chi20 = abs(float(p['SP_m_chi_20']))
    m_t1 = abs(float(p['SP_m_t_1']))
    m_b1 = abs(float(p['SP_m_b_1']))
    m_eL = abs(float(p['SP_m_e_L']))
    m_eR = abs(float(p['SP_m_e_R']))

    # Mass splittings
    dm_c1 = m_chi1p - m_lsp
    dm_n2 = m_chi20 - m_lsp
    dm_stop = m_t1 - m_lsp

    # Chargino lifetime
    w_chi1p = get_field(p, 'SP_w_chi_1p')
    ctau_chi1p = width_to_ctau(w_chi1p)

    # Key branching fractions
    bf_c1_to_n1 = get_field(p, 'SP_BF_chi_1p_to_chi_10')
    bf_n2_to_n1 = get_field(p, 'SP_BF_chi_20_to_chi_10')
    bf_n2_to_n1_Z = get_field(p, 'SP_BF_chi_20_to_chi_10_Z')
    bf_n2_to_n1_h = get_field(p, 'SP_BF_chi_20_to_chi_10_h')
    bf_n2_to_c1_W = get_field(p, 'SP_BF_chi_20_to_chi_1p_W')
    bf_t1_to_n1_t = get_field(p, 'SP_BF_t_1_to_chi_10_t')
    bf_t1_to_c1_b = get_field(p, 'SP_BF_t_1_to_chi_1p_b')
    bf_t1_to_n1_c = get_field(p, 'SP_BF_t_1_to_chi_10_c')
    bf_t1_to_n1_bW = get_field(p, 'SP_BF_t_1_to_chi_10_b_W')
    bf_eL_to_n1_e = get_field(p, 'SP_BF_e_L_to_chi_10_ele')
    bf_eR_to_n1_e = get_field(p, 'SP_BF_e_R_to_chi_10_ele')

    # Mixing fractions
    n1_bino = get_field(p, 'SP_chi_10_Bino_frac')
    n1_wino = get_field(p, 'SP_chi_10_Wino_frac')
    n1_higgsino = get_field(p, 'SP_chi_10_Higgsino_frac')
    c1_wino = get_field(p, 'SP_chi_1p_Wino_frac')
    c1_higgsino = get_field(p, 'SP_chi_1p_Higgsino_frac')

    # Determine dominant decay chain description
    dominant_chain = ''
    if lsp_type == 2 and dm_c1 < 5:
        dominant_chain = f'chi1+ -> pi+ chi10 (ctau={ctau_chi1p:.3f}m)'
    elif lsp_type == 3 and dm_c1 < 30:
        if bf_n2_to_n1_Z > 0.3:
            dominant_chain = f'chi20 -> Z* chi10, chi1+ -> W* chi10'
        else:
            dominant_chain = f'chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)'
    elif bf_t1_to_c1_b > 0.3:
        dominant_chain = f'stop -> b chi1+ (BF={bf_t1_to_c1_b:.2f})'
    elif bf_t1_to_n1_t > 0.3:
        dominant_chain = f'stop -> t chi10 (BF={bf_t1_to_n1_t:.2f})'
    elif bf_eL_to_n1_e > 0.3 or bf_eR_to_n1_e > 0.3:
        dominant_chain = f'slepton -> l chi10'

    # Production cross-sections from SModelS
    total_theory_xsec = 0.0
    atlas_xsec = 0.0
    cms_xsec = 0.0
    if smodels_data:
        for res in smodels_data['expt_results']:
            xsec = res['theory_prediction_fb']
            if xsec and xsec > 0:
                total_theory_xsec += xsec
                if 'ATLAS' in res['AnalysisID'].upper():
                    atlas_xsec += xsec
                elif 'CMS' in res['AnalysisID'].upper():
                    cms_xsec += xsec

    # Expected visible pT (rough kinematic estimate)
    if dm_c1 < 1:
        expected_vis_pt = 'sub-GeV (displaced pion)'
    elif dm_c1 < 20:
        expected_vis_pt = f'soft leptons ~{dm_c1/3:.0f} GeV'
    elif dm_stop < 200 and m_t1 < 1000:
        expected_vis_pt = f'b-jets ~{dm_stop/2:.0f} GeV'
    else:
        expected_vis_pt = 'standard'

    return {
        'dm_c1': dm_c1,
        'dm_n2': dm_n2,
        'dm_stop': dm_stop,
        'w_chi1p_gev': w_chi1p,
        'ctau_chi1p_m': ctau_chi1p,
        'bf_c1_to_n1': bf_c1_to_n1,
        'bf_n2_to_n1_Z': bf_n2_to_n1_Z,
        'bf_n2_to_n1_h': bf_n2_to_n1_h,
        'bf_n2_to_c1_W': bf_n2_to_c1_W,
        'bf_t1_to_n1_t': bf_t1_to_n1_t,
        'bf_t1_to_c1_b': bf_t1_to_c1_b,
        'bf_eL_to_n1_e': bf_eL_to_n1_e,
        'bf_eR_to_n1_e': bf_eR_to_n1_e,
        'n1_bino_frac': n1_bino,
        'n1_wino_frac': n1_wino,
        'n1_higgsino_frac': n1_higgsino,
        'c1_wino_frac': c1_wino,
        'c1_higgsino_frac': c1_higgsino,
        'dominant_chain': dominant_chain,
        'total_theory_xsec_fb': total_theory_xsec,
        'expected_vis_pt': expected_vis_pt,
    }


def main():
    print("=" * 70)
    print("SIGNAL CHARACTERIZATION")
    print("=" * 70)

    # Load coverage CSV to identify which models to characterize
    cov_path = os.path.join(RESULTS_DIR, 'model_atlas_coverage.csv')
    with open(cov_path) as f:
        cov_rows = list(csv.DictReader(f))
    print(f"Loaded {len(cov_rows)} models from coverage CSV")

    # Load full ntuples with extended fields for branching fractions and widths
    data, provenance = load_ntuples_extended()
    mask = apply_all_cuts(data)
    passing = data[mask]
    passing_mask = ak.to_numpy(mask)
    passing_provenance = [p for p, m in zip(provenance, passing_mask) if m]

    n_pass = len(passing)
    print(f"{n_pass} models pass all cuts")

    # Build lookup from (scan_dir_basename, model_id) -> index
    prov_lookup = {}
    for i, (sd, mid) in enumerate(passing_provenance):
        key = (os.path.basename(sd), int(mid))
        prov_lookup[key] = i

    # Characterize all models (focus on ATLAS tier 0-2 but do all for completeness)
    output_rows = []
    n_characterized = 0

    for cov_row in cov_rows:
        scan_dir_base = cov_row['scan_dir']
        model_id = int(cov_row['model_id'])
        atlas_tier = int(cov_row['atlas_tier'])

        key = (scan_dir_base, model_id)
        idx = prov_lookup.get(key)
        if idx is None:
            continue

        p = passing[idx]
        sd_full = passing_provenance[idx][0]

        # Parse SModelS
        smodels_path = os.path.join(sd_full, 'SModelS', f'{model_id}.slha.py')
        sm = parse_smodels_file(smodels_path)

        sig = characterize_model(p, sm)
        n_characterized += 1

        row = {
            'scan_dir': scan_dir_base,
            'model_id': model_id,
            'lsp_type': int(cov_row['lsp_type']),
            'lsp_name': cov_row['lsp_name'],
            'atlas_tier': atlas_tier,
            'm_lsp': cov_row['m_lsp'],
            'm_chi1p': cov_row['m_chi1p'],
            'm_chi20': cov_row['m_chi20'],
            'm_t1': cov_row['m_t1'],
            'm_eL': cov_row['m_eL'],
            'm_eR': cov_row['m_eR'],
        }
        row.update({k: f'{v:.6f}' if isinstance(v, float) else v for k, v in sig.items()})
        output_rows.append(row)

    # Write output CSV
    out_path = os.path.join(RESULTS_DIR, 'signal_characterization.csv')
    with open(out_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()))
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"\nSignal characterization CSV: {out_path} ({n_characterized} models)")

    # Print summary statistics for ATLAS-blind models
    blind = [r for r in output_rows if int(r['atlas_tier']) <= 1]
    print(f"\n{'='*60}")
    print(f"ATLAS-BLIND MODELS (tier 0-1): {len(blind)}")
    print(f"{'='*60}")

    # Chargino lifetime distribution
    ctau_vals = [float(r['ctau_chi1p_m']) for r in blind if float(r['ctau_chi1p_m']) > 0]
    if ctau_vals:
        print(f"\n  Chargino ctau distribution:")
        print(f"    ctau > 1 cm:  {sum(1 for c in ctau_vals if c > 0.01)}")
        print(f"    ctau > 10 cm: {sum(1 for c in ctau_vals if c > 0.1)}")
        print(f"    ctau > 1 m:   {sum(1 for c in ctau_vals if c > 1.0)}")
        print(f"    max ctau: {max(ctau_vals):.3f} m")

    # Dominant decay chains
    from collections import Counter
    chains = Counter(r['dominant_chain'] for r in blind if r['dominant_chain'])
    print(f"\n  Dominant decay chains:")
    for chain, cnt in chains.most_common(10):
        print(f"    {chain}: {cnt}")

    print("\nDone.")


if __name__ == '__main__':
    main()
