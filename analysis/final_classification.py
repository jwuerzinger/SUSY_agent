#!/usr/bin/env python
"""Final classification: merge Phase 1 + Phase 2, classify all models, extract benchmarks."""

import uproot
import awkward as ak
import numpy as np
import os
import sys
import glob

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
PLOT_DIR = os.path.join(PROJECT_ROOT, 'results', 'plots')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')
os.makedirs(PLOT_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Physics cut values
HIGGS_MASS_LOW = 122.0
HIGGS_MASS_HIGH = 128.0
OMEGA_UPPER = 0.132
BSG_CENTRAL = 3.32e-4
BSG_SIGMA = 0.33e-4
BSMUMU_CENTRAL = 3.09e-9
BSMUMU_SIGMA = 0.65e-9
LEP_CHARGINO_MIN = 103.0  # LEP2 lower limit on chargino mass [GeV]


REQUIRED_FIELDS = [
    'SP_m_h', 'SS_m_h', 'SP_LSP_type', 'FH_m_h', 'MO_Omega',
    'SI_BR_b_to_sgamma', 'SI_BR_Bs_to_mumu',
    'SModelS_bestExpUL_TheoryPrediction', 'SModelS_bestExpUL_UpperLimit',
    'SP_m_chi_10', 'SP_m_chi_1p', 'SP_m_chi_20',
    'SP_m_t_1', 'SP_m_b_1', 'SP_m_gl',
    'SP_m_e_L', 'SP_m_e_R', 'SP_m_H', 'SP_m_A',
]


def load_all_ntuples():
    """Load ntuples from all phases, reading only required fields."""
    import re
    ntuple_files = sorted(glob.glob(os.path.join(PROJECT_ROOT, 'scans/phase*/*/ntuple.*.root')))
    if not ntuple_files:
        print("No ntuple files found")
        sys.exit(1)

    print(f"Found {len(ntuple_files)} ntuple files:")
    arrays = []
    sources = []
    for f in ntuple_files:
        with uproot.open(f"{f}:susy") as tree:
            available = set(tree.keys())
            fields_to_read = [fld for fld in REQUIRED_FIELDS if fld in available]
            missing = [fld for fld in REQUIRED_FIELDS if fld not in available]
            arr = tree.arrays(fields_to_read, library="ak")
            n = len(arr)
            # Fill missing fields with -1
            for fld in missing:
                arr = ak.with_field(arr, np.full(n, -1.0), fld)
            arrays.append(arr)
            m = re.search(r'(phase\d[a-d]?)', f)
            tag = m.group(1) if m else 'unknown'
            sources.extend([tag] * n)
            print(f"  {f}: {n} entries ({len(missing)} fields filled)")

    data = ak.concatenate(arrays)
    print(f"Total models: {len(data)}")
    return data, sources


def apply_all_cuts(data):
    """Apply all physics cuts."""
    sp_valid = data['SP_m_h'] != -1
    ss_valid = data['SS_m_h'] != -1
    quality = sp_valid & ss_valid
    neut_lsp = (data['SP_LSP_type'] >= 1) & (data['SP_LSP_type'] <= 3)
    has_fh = data['FH_m_h'] != -1
    m_h = ak.where(has_fh, data['FH_m_h'], data['SP_m_h'])
    higgs_ok = (m_h > HIGGS_MASS_LOW) & (m_h < HIGGS_MASS_HIGH)
    omega_ok = (data['MO_Omega'] != -1) & (data['MO_Omega'] <= OMEGA_UPPER)
    bsg_ok = (data['SI_BR_b_to_sgamma'] != -1) & \
             (data['SI_BR_b_to_sgamma'] > BSG_CENTRAL - 2 * BSG_SIGMA) & \
             (data['SI_BR_b_to_sgamma'] < BSG_CENTRAL + 2 * BSG_SIGMA)
    bsmumu_ok = (data['SI_BR_Bs_to_mumu'] != -1) & \
                (data['SI_BR_Bs_to_mumu'] > BSMUMU_CENTRAL - 2 * BSMUMU_SIGMA) & \
                (data['SI_BR_Bs_to_mumu'] < BSMUMU_CENTRAL + 2 * BSMUMU_SIGMA)
    has_sm = data['SModelS_bestExpUL_TheoryPrediction'] != -1
    has_ul = data['SModelS_bestExpUL_UpperLimit'] != -1
    smodels_ok = ~has_sm | ~has_ul | \
                 (data['SModelS_bestExpUL_TheoryPrediction'] < data['SModelS_bestExpUL_UpperLimit'])
    lep_ok = np.abs(ak.to_numpy(data['SP_m_chi_1p'])) > LEP_CHARGINO_MIN
    return quality & neut_lsp & higgs_ok & omega_ok & bsg_ok & bsmumu_ok & smodels_ok & lep_ok


def classify_model(p):
    """Classify a single model. Returns list of category names."""
    categories = []
    lsp_type = int(p['SP_LSP_type'])
    m_lsp = abs(float(p['SP_m_chi_10']))
    m_chi1p = abs(float(p['SP_m_chi_1p']))
    m_chi20 = abs(float(p['SP_m_chi_20']))
    m_t1 = abs(float(p['SP_m_t_1']))
    m_b1 = abs(float(p['SP_m_b_1']))
    m_eL = abs(float(p['SP_m_e_L']))
    m_eR = abs(float(p['SP_m_e_R']))
    m_H = abs(float(p['SP_m_H']))
    m_A = abs(float(p['SP_m_A']))
    dm_c1 = m_chi1p - m_lsp
    dm_n2 = m_chi20 - m_lsp

    if lsp_type == 1 and m_chi20 < 1000 and m_chi1p < 1000:
        categories.append('Bino+lightEWK')
    if lsp_type == 2 and dm_c1 < 20:
        categories.append('Wino_compressed')
    if lsp_type == 3 and dm_n2 < 30:
        categories.append('Higgsino_compressed')
    if m_t1 < 1200 and (m_t1 - m_lsp) > 20:
        categories.append('Light_stop')
    if m_b1 < 1200 and (m_b1 - m_lsp) > 20:
        categories.append('Light_sbottom')
    if min(m_eL, m_eR) < 600:
        categories.append('Light_slepton')
    if dm_c1 < 50:
        categories.append('Compressed_EWK')
    if (m_t1 - m_lsp) < 200:
        categories.append('Compressed_stop')
    if m_H < 1000 or m_A < 1000:
        categories.append('Heavy_Higgs')
    return categories


def find_benchmarks(passing, all_categories):
    """Find the most interesting benchmark model per category."""
    benchmarks = {}

    for i in range(len(passing)):
        p = passing[i]
        cats = all_categories[i]
        m_lsp = abs(float(p['SP_m_chi_10']))
        m_t1 = abs(float(p['SP_m_t_1']))
        m_b1 = abs(float(p['SP_m_b_1']))
        m_eL = abs(float(p['SP_m_e_L']))
        m_eR = abs(float(p['SP_m_e_R']))
        dm_c1 = abs(float(p['SP_m_chi_1p'])) - m_lsp

        for cat in cats:
            score = None
            if cat == 'Light_stop':
                score = m_t1  # lightest stop wins
            elif cat == 'Light_sbottom':
                score = m_b1
            elif cat == 'Light_slepton':
                score = min(m_eL, m_eR)
            elif cat in ('Wino_compressed', 'Higgsino_compressed', 'Compressed_EWK'):
                score = dm_c1  # smallest splitting wins
            elif cat == 'Compressed_stop':
                score = m_t1 - m_lsp
            elif cat == 'Heavy_Higgs':
                score = min(abs(float(p['SP_m_H'])), abs(float(p['SP_m_A'])))
            elif cat == 'Bino+lightEWK':
                score = abs(float(p['SP_m_chi_20']))
            else:
                score = m_lsp

            if cat not in benchmarks or score < benchmarks[cat][1]:
                benchmarks[cat] = (i, score)

    return benchmarks


def print_model_summary(p, idx, source=''):
    """Print a compact summary of a model."""
    lsp_names = {1: 'Bino', 2: 'Wino', 3: 'Higgsino'}
    lsp_type = int(p['SP_LSP_type'])
    m_lsp = abs(float(p['SP_m_chi_10']))
    print(f"  Model #{idx} ({source}) — LSP: {lsp_names.get(lsp_type, '?')}")
    print(f"    m(LSP)={m_lsp:.0f}, m(chi1+)={abs(float(p['SP_m_chi_1p'])):.0f}, "
          f"m(chi20)={abs(float(p['SP_m_chi_20'])):.0f} GeV")
    print(f"    m(t1)={abs(float(p['SP_m_t_1'])):.0f}, m(b1)={abs(float(p['SP_m_b_1'])):.0f}, "
          f"m(gl)={abs(float(p['SP_m_gl'])):.0f} GeV")
    print(f"    m(eL)={abs(float(p['SP_m_e_L'])):.0f}, m(eR)={abs(float(p['SP_m_e_R'])):.0f} GeV")
    print(f"    Omega={float(p['MO_Omega']):.4f}, m_h(FH)={float(p['FH_m_h']):.1f} GeV")
    sm_tp = float(p['SModelS_bestExpUL_TheoryPrediction'])
    sm_ul = float(p['SModelS_bestExpUL_UpperLimit'])
    if sm_tp > 0 and sm_ul > 0:
        print(f"    SModelS r={sm_tp/sm_ul:.3f}")


def make_summary_plots(passing, all_categories, category_counts, plot_dir):
    """Publication-quality summary plots."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available")
        return

    if len(passing) == 0:
        return

    m_lsp = np.abs(ak.to_numpy(passing['SP_m_chi_10']))
    m_chi1p = np.abs(ak.to_numpy(passing['SP_m_chi_1p']))
    m_t1 = np.abs(ak.to_numpy(passing['SP_m_t_1']))
    m_b1 = np.abs(ak.to_numpy(passing['SP_m_b_1']))
    lsp_type = ak.to_numpy(passing['SP_LSP_type'])

    # --- Summary: m(chi1+) vs m(LSP) colored by LSP type ---
    fig, ax = plt.subplots(figsize=(9, 8))
    colors_map = {1: '#ff6666', 2: '#6699ff', 3: '#66cc66'}
    labels_map = {1: 'Bino', 2: 'Wino', 3: 'Higgsino'}
    for lt in [1, 2, 3]:
        mask = lsp_type == lt
        if np.sum(mask) > 0:
            ax.scatter(m_lsp[mask], m_chi1p[mask], c=colors_map[lt], s=15, alpha=0.7,
                       label=f'{labels_map[lt]} ({np.sum(mask)})', edgecolors='black', linewidths=0.3)
    ax.plot([0, 2000], [0, 2000], 'k--', alpha=0.3, label='m(chi1+) = m(LSP)')
    ax.set_xlabel('|m(LSP)| [GeV]', fontsize=12)
    ax.set_ylabel('|m(chi1+)| [GeV]', fontsize=12)
    ax.set_title('All Surviving Models: Chargino vs LSP Mass', fontsize=13)
    ax.legend(fontsize=10)
    ax.set_xlim(0, max(m_lsp) * 1.1)
    ax.set_ylim(0, max(m_chi1p) * 1.1)
    fig.savefig(os.path.join(plot_dir, 'final_chargino_vs_lsp.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)

    # --- Summary: stop mass vs LSP mass ---
    fig, ax = plt.subplots(figsize=(9, 8))
    for lt in [1, 2, 3]:
        mask = lsp_type == lt
        if np.sum(mask) > 0:
            ax.scatter(m_lsp[mask], m_t1[mask], c=colors_map[lt], s=15, alpha=0.7,
                       label=f'{labels_map[lt]} ({np.sum(mask)})', edgecolors='black', linewidths=0.3)
    ax.plot([0, 3000], [0, 3000], 'k--', alpha=0.3, label='m(stop1) = m(LSP)')
    ax.set_xlabel('|m(LSP)| [GeV]', fontsize=12)
    ax.set_ylabel('|m(stop1)| [GeV]', fontsize=12)
    ax.set_title('All Surviving Models: Stop vs LSP Mass', fontsize=13)
    ax.legend(fontsize=10)
    fig.savefig(os.path.join(plot_dir, 'final_stop_vs_lsp.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)

    # --- Category bar chart ---
    if category_counts:
        fig, ax = plt.subplots(figsize=(10, 6))
        cats = sorted(category_counts.keys(), key=lambda c: category_counts[c])
        counts = [category_counts[c] for c in cats]
        bars = ax.barh(cats, counts, color='steelblue', edgecolor='black')
        ax.set_xlabel('Number of models', fontsize=12)
        ax.set_title('Physics Category Populations (all phases combined)', fontsize=13)
        for bar, count in zip(bars, counts):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                    str(count), va='center', fontsize=10)
        fig.tight_layout()
        fig.savefig(os.path.join(plot_dir, 'final_categories.png'), dpi=150, bbox_inches='tight')
        plt.close(fig)

    print(f"Summary plots saved to {plot_dir}/")


def main():
    print("=" * 70)
    print("FINAL CLASSIFICATION: All Phases Combined")
    print("=" * 70)

    data, sources = load_all_ntuples()
    mask = apply_all_cuts(data)
    passing = data[mask]
    passing_sources = [s for s, m in zip(sources, ak.to_numpy(mask)) if m]

    print(f"\n{len(passing)} / {len(data)} models pass all cuts ({len(passing)/len(data)*100:.1f}%)")

    # Source breakdown
    from collections import Counter
    source_counts = Counter(passing_sources)
    print(f"\nBy source:")
    for src, cnt in sorted(source_counts.items()):
        print(f"  {src}: {cnt}")

    # LSP composition
    lsp = ak.to_numpy(passing['SP_LSP_type'])
    print(f"\nLSP composition:")
    print(f"  Bino: {int(np.sum(lsp==1))}")
    print(f"  Wino: {int(np.sum(lsp==2))}")
    print(f"  Higgsino: {int(np.sum(lsp==3))}")

    # Classify all models
    all_categories = []
    category_counts = {}
    for i in range(len(passing)):
        cats = classify_model(passing[i])
        all_categories.append(cats)
        for c in cats:
            category_counts[c] = category_counts.get(c, 0) + 1

    print(f"\nCategory populations (non-exclusive):")
    for c, n in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")

    # Find benchmarks
    benchmarks = find_benchmarks(passing, all_categories)
    print(f"\nBenchmark models (best per category):")
    for cat, (idx, score) in sorted(benchmarks.items()):
        print(f"\n  [{cat}] (score={score:.1f}):")
        print_model_summary(passing[idx], idx, passing_sources[idx])

    # Plots
    make_summary_plots(passing, all_categories, category_counts, PLOT_DIR)

    # Save passing model indices for extraction
    print(f"\nTotal unique passing models: {len(passing)}")
    print(f"Total categories populated: {len(category_counts)}")


if __name__ == '__main__':
    main()
