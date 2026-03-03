#!/usr/bin/env python
"""Phase 2 analysis: evaluate MCMC scan results, classify models, compare to Phase 1."""

import uproot
import awkward as ak
import numpy as np
import os
import sys
import glob

# --- Configuration ---
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
PLOT_DIR = os.path.join(PROJECT_ROOT, 'results', 'plots')
os.makedirs(PLOT_DIR, exist_ok=True)

# Physics cut values
HIGGS_MASS_LOW = 122.0
HIGGS_MASS_HIGH = 128.0
OMEGA_UPPER = 0.132
BSG_CENTRAL = 3.32e-4
BSG_SIGMA = 0.33e-4
BSMUMU_CENTRAL = 3.09e-9
BSMUMU_SIGMA = 0.65e-9

PHASE2_SCANS = {
    'phase2a': {'label': 'Light EWKinos', 'path': 'scans/phase2a'},
    'phase2b': {'label': 'Light Stops', 'path': 'scans/phase2b'},
    'phase2c': {'label': 'Light Sleptons', 'path': 'scans/phase2c'},
    'phase2d': {'label': 'Compressed', 'path': 'scans/phase2d'},
}


def load_ntuples(scan_path):
    """Load and merge all ntuples from a scan directory (multiple seeds)."""
    ntuple_files = sorted(glob.glob(os.path.join(scan_path, '*/ntuple.*.root')))
    if not ntuple_files:
        return None
    arrays = []
    for f in ntuple_files:
        with uproot.open(f"{f}:susy") as tree:
            arrays.append(tree.arrays(library="ak"))
    return ak.concatenate(arrays)


def apply_all_cuts(data):
    """Apply quality + physics + SModelS cuts. Returns mask."""
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

    return quality & neut_lsp & higgs_ok & omega_ok & bsg_ok & bsmumu_ok & smodels_ok


def classify_model(p):
    """Classify a single passing model into physics categories. Returns list of category names."""
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

    # 1. Bino LSP with light EWKinos
    if lsp_type == 1 and m_chi20 < 1000 and m_chi1p < 1000:
        categories.append('Bino+lightEWK')

    # 2. Wino-like compressed
    if lsp_type == 2 and dm_c1 < 20:
        categories.append('Wino_compressed')

    # 3. Higgsino-like compressed
    if lsp_type == 3 and dm_n2 < 30:
        categories.append('Higgsino_compressed')

    # 4. Light stop
    if m_t1 < 1200 and (m_t1 - m_lsp) > 20:
        categories.append('Light_stop')

    # 5. Light sbottom
    if m_b1 < 1200 and (m_b1 - m_lsp) > 20:
        categories.append('Light_sbottom')

    # 6. Light sleptons
    if min(m_eL, m_eR) < 600:
        categories.append('Light_slepton')

    # 7. Compressed EWKino (general)
    if dm_c1 < 50:
        categories.append('Compressed_EWK')

    # 8. Compressed stop
    if (m_t1 - m_lsp) < 200:
        categories.append('Compressed_stop')

    # 9. Heavy Higgs accessible
    if m_H < 1000 or m_A < 1000:
        categories.append('Heavy_Higgs')

    return categories


def print_cutflow(data, label):
    """Print cutflow for a dataset."""
    n = len(data)
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

    cuts = [
        ('Total models', ak.ones_like(sp_valid, dtype=bool)),
        ('Quality (both specgen)', quality),
        ('Neutralino LSP', quality & neut_lsp),
        ('Higgs mass', quality & neut_lsp & higgs_ok),
        ('Relic density', quality & neut_lsp & higgs_ok & omega_ok),
        ('B-physics', quality & neut_lsp & higgs_ok & omega_ok & bsg_ok & bsmumu_ok),
        ('SModelS allowed', quality & neut_lsp & higgs_ok & omega_ok & bsg_ok & bsmumu_ok & smodels_ok),
    ]

    print(f"\n{'='*60}")
    print(f"CUTFLOW: {label}")
    print(f"{'='*60}")
    print(f"{'Cut':<30} {'Pass':>8} {'Rate':>8}")
    print(f"{'-'*60}")
    for name, mask in cuts:
        n_pass = int(ak.sum(mask))
        rate = n_pass / n * 100 if n > 0 else 0
        print(f"{name:<30} {n_pass:>8} {rate:>7.1f}%")
    print(f"{'='*60}")


def make_phase2_plots(all_passing, category_counts, plot_dir):
    """Generate Phase 2 analysis plots."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available, skipping plots")
        return

    if len(all_passing) == 0:
        print("No passing models, skipping plots")
        return

    # --- Plot 1: LSP mass distribution by scan type ---
    fig, ax = plt.subplots(figsize=(9, 6))
    m_lsp = np.abs(ak.to_numpy(all_passing['SP_m_chi_10']))
    ax.hist(m_lsp, bins=40, range=(0, 1000), color='steelblue', edgecolor='black')
    ax.set_xlabel('|m(LSP)| [GeV]')
    ax.set_ylabel('Models')
    ax.set_title('Phase 2: LSP Mass Distribution (all passing)')
    fig.savefig(os.path.join(plot_dir, 'phase2_lsp_mass.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)

    # --- Plot 2: Chargino-LSP mass splitting ---
    fig, ax = plt.subplots(figsize=(9, 6))
    dm = np.abs(ak.to_numpy(all_passing['SP_m_chi_1p'])) - np.abs(ak.to_numpy(all_passing['SP_m_chi_10']))
    ax.hist(dm, bins=50, range=(0, 500), color='coral', edgecolor='black')
    ax.set_xlabel('dm(chi1+, LSP) [GeV]')
    ax.set_ylabel('Models')
    ax.set_title('Phase 2: Chargino-LSP Mass Splitting')
    fig.savefig(os.path.join(plot_dir, 'phase2_dm_chargino.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)

    # --- Plot 3: Stop mass vs LSP mass ---
    fig, ax = plt.subplots(figsize=(8, 7))
    m_t1 = np.abs(ak.to_numpy(all_passing['SP_m_t_1']))
    ax.scatter(m_lsp, m_t1, c='steelblue', s=8, alpha=0.6)
    ax.plot([0, 2000], [0, 2000], 'r--', label='m(stop1) = m(LSP)')
    ax.set_xlabel('|m(LSP)| [GeV]')
    ax.set_ylabel('|m(stop1)| [GeV]')
    ax.set_title('Phase 2: Stop1 vs LSP Mass')
    ax.legend()
    ax.set_xlim(0, 1500)
    ax.set_ylim(0, 2500)
    fig.savefig(os.path.join(plot_dir, 'phase2_stop_vs_lsp.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)

    # --- Plot 4: Category populations bar chart ---
    if category_counts:
        fig, ax = plt.subplots(figsize=(10, 6))
        cats = sorted(category_counts.keys())
        counts = [category_counts[c] for c in cats]
        ax.barh(cats, counts, color='steelblue', edgecolor='black')
        ax.set_xlabel('Number of models')
        ax.set_title('Phase 2: Physics Category Populations')
        fig.savefig(os.path.join(plot_dir, 'phase2_categories.png'), dpi=150, bbox_inches='tight')
        plt.close(fig)

    # --- Plot 5: LSP composition pie chart ---
    lsp_types = ak.to_numpy(all_passing['SP_LSP_type'])
    bino_n = int(np.sum(lsp_types == 1))
    wino_n = int(np.sum(lsp_types == 2))
    higgsino_n = int(np.sum(lsp_types == 3))
    if bino_n + wino_n + higgsino_n > 0:
        fig, ax = plt.subplots(figsize=(7, 7))
        labels = [f'Bino ({bino_n})', f'Wino ({wino_n})', f'Higgsino ({higgsino_n})']
        sizes = [bino_n, wino_n, higgsino_n]
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        nonzero = [(l, s, c) for l, s, c in zip(labels, sizes, colors) if s > 0]
        if nonzero:
            labels, sizes, colors = zip(*nonzero)
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.set_title('Phase 2: LSP Composition (all passing)')
            fig.savefig(os.path.join(plot_dir, 'phase2_lsp_composition.png'), dpi=150, bbox_inches='tight')
        plt.close(fig)

    # --- Plot 6: Relic density ---
    omega = ak.to_numpy(all_passing['MO_Omega'])
    omega_pos = omega[omega > 0]
    if len(omega_pos) > 0:
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.hist(np.log10(omega_pos), bins=50, color='steelblue', edgecolor='black')
        ax.axvline(np.log10(0.120), color='red', linestyle='--', label='Planck (0.120)')
        ax.set_xlabel('log10(Omega h^2)')
        ax.set_ylabel('Models')
        ax.set_title('Phase 2: Relic Density (passing models)')
        ax.legend()
        fig.savefig(os.path.join(plot_dir, 'phase2_relic_density.png'), dpi=150, bbox_inches='tight')
        plt.close(fig)

    print(f"Plots saved to {plot_dir}/")


def main():
    print("=" * 70)
    print("PHASE 2 ANALYSIS: Targeted MCMC Scans")
    print("=" * 70)

    all_passing_arrays = []
    all_category_counts = {}

    for scan_key, scan_info in PHASE2_SCANS.items():
        scan_path = os.path.join(PROJECT_ROOT, scan_info['path'])
        data = load_ntuples(scan_path)
        if data is None:
            print(f"\n[SKIP] {scan_info['label']}: no ntuples found in {scan_path}")
            continue

        print(f"\n--- {scan_info['label']} ({scan_key}) ---")
        print(f"  Models loaded: {len(data)}")

        # Pipeline success
        sp_ok = int(ak.sum(data['SP_m_h'] != -1))
        print(f"  SPheno success: {sp_ok}/{len(data)} ({sp_ok/len(data)*100:.1f}%)")

        # Cutflow
        print_cutflow(data, scan_info['label'])

        # Apply all cuts
        mask = apply_all_cuts(data)
        passing = data[mask]
        n_pass = len(passing)
        print(f"\n  Passing all cuts: {n_pass}/{len(data)} ({n_pass/len(data)*100:.1f}%)")

        if n_pass > 0:
            all_passing_arrays.append(passing)

            # LSP composition
            lsp = ak.to_numpy(passing['SP_LSP_type'])
            print(f"  LSP types: Bino={int(np.sum(lsp==1))}, Wino={int(np.sum(lsp==2))}, Higgsino={int(np.sum(lsp==3))}")

            # Classify
            cat_counts = {}
            for i in range(n_pass):
                cats = classify_model(passing[i])
                for c in cats:
                    cat_counts[c] = cat_counts.get(c, 0) + 1
                    all_category_counts[c] = all_category_counts.get(c, 0) + 1

            print(f"  Categories:")
            for c, n in sorted(cat_counts.items(), key=lambda x: -x[1]):
                print(f"    {c}: {n}")

    # Merge all passing models
    if all_passing_arrays:
        all_passing = ak.concatenate(all_passing_arrays)
    else:
        print("\nNo models passed all cuts in any Phase 2 scan.")
        return

    print(f"\n{'='*70}")
    print(f"PHASE 2 COMBINED: {len(all_passing)} models pass all cuts")
    print(f"{'='*70}")

    # LSP composition
    lsp = ak.to_numpy(all_passing['SP_LSP_type'])
    print(f"LSP types: Bino={int(np.sum(lsp==1))}, Wino={int(np.sum(lsp==2))}, Higgsino={int(np.sum(lsp==3))}")

    # Category summary
    print(f"\nCategory populations (non-exclusive):")
    for c, n in sorted(all_category_counts.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")

    # Plots
    make_phase2_plots(all_passing, all_category_counts, PLOT_DIR)


if __name__ == '__main__':
    main()
