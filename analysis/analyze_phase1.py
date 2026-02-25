#!/usr/bin/env python
"""Phase 1 analysis: evaluate flat scan results and document findings."""

import uproot
import awkward as ak
import numpy as np
import os
import sys
import glob

# --- Configuration ---
SCAN_BASE = os.path.join(os.path.dirname(__file__), '..', 'scans', 'phase1')
PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', 'results', 'plots')
os.makedirs(PLOT_DIR, exist_ok=True)

# Physics cut values
HIGGS_MASS_LOW = 122.0
HIGGS_MASS_HIGH = 128.0
OMEGA_UPPER = 0.132  # Planck 1-sigma upper
BSG_CENTRAL = 3.32e-4
BSG_SIGMA = 0.33e-4
BSMUMU_CENTRAL = 3.09e-9
BSMUMU_SIGMA = 0.65e-9


def load_ntuples(scan_base):
    """Load and merge all ntuples from scan directories."""
    ntuple_files = sorted(glob.glob(os.path.join(scan_base, '*/ntuple.*.root')))
    if not ntuple_files:
        print(f"No ntuple files found in {scan_base}")
        sys.exit(1)

    print(f"Found {len(ntuple_files)} ntuple files:")
    arrays = []
    for f in ntuple_files:
        print(f"  {f}")
        with uproot.open(f"{f}:susy") as tree:
            arrays.append(tree.arrays(library="ak"))

    data = ak.concatenate(arrays)
    print(f"Total models loaded: {len(data)}")
    return data


def compute_pipeline_success(data):
    """Compute success rates for each pipeline step."""
    n = len(data)
    results = {}

    # SPheno: check if m_h was computed (not -1)
    sp_ok = ak.sum(data['SP_m_h'] != -1)
    results['SPheno'] = (int(sp_ok), n)

    # Softsusy
    ss_ok = ak.sum(data['SS_m_h'] != -1)
    results['Softsusy'] = (int(ss_ok), n)

    # micrOMEGAs: check if Omega was computed
    if 'MO_Omega' in data.fields:
        mo_ok = ak.sum(data['MO_Omega'] != -1)
        results['micrOMEGAs'] = (int(mo_ok), n)

    # SuperISO
    if 'SI_BR_b_to_sgamma' in data.fields:
        si_ok = ak.sum(data['SI_BR_b_to_sgamma'] != -1)
        results['SuperISO'] = (int(si_ok), n)

    # GM2Calc
    if 'GM2_gmuon' in data.fields:
        gm2_ok = ak.sum(data['GM2_gmuon'] != -1)
        results['GM2Calc'] = (int(gm2_ok), n)

    # FeynHiggs
    if 'FH_m_h' in data.fields:
        fh_ok = ak.sum(data['FH_m_h'] != -1)
        results['FeynHiggs'] = (int(fh_ok), n)

    # SModelS
    if 'SModelS_bestExpUL_TheoryPrediction' in data.fields:
        sm_ok = ak.sum(data['SModelS_bestExpUL_TheoryPrediction'] != -1)
        results['SModelS'] = (int(sm_ok), n)

    return results


def compute_physics_cuts(data):
    """Apply physics cuts and return masks + statistics."""
    n = len(data)
    cuts = {}

    # Quality: both spectrum generators converged
    sp_valid = data['SP_m_h'] != -1
    ss_valid = data['SS_m_h'] != -1
    quality = sp_valid & ss_valid

    # Neutralino LSP
    has_lsp_type = 'SP_LSP_type' in data.fields
    if has_lsp_type:
        neutralino_lsp = (data['SP_LSP_type'] >= 1) & (data['SP_LSP_type'] <= 3)
    else:
        neutralino_lsp = sp_valid  # fallback

    cuts['Quality (both specgen OK)'] = quality
    cuts['Neutralino LSP'] = quality & neutralino_lsp

    # Higgs mass (use FH when available, fall back to SP)
    if 'FH_m_h' in data.fields:
        has_fh = data['FH_m_h'] != -1
        m_h = ak.where(has_fh, data['FH_m_h'], data['SP_m_h'])
    else:
        m_h = data['SP_m_h']
    higgs_ok = (m_h > HIGGS_MASS_LOW) & (m_h < HIGGS_MASS_HIGH)
    cuts['Higgs mass'] = quality & neutralino_lsp & higgs_ok

    # Relic density
    if 'MO_Omega' in data.fields:
        omega_valid = data['MO_Omega'] != -1
        omega_ok = omega_valid & (data['MO_Omega'] <= OMEGA_UPPER)
        cuts['Relic density'] = quality & neutralino_lsp & higgs_ok & omega_ok
    else:
        omega_ok = ak.ones_like(sp_valid, dtype=bool)

    # B-physics
    if 'SI_BR_b_to_sgamma' in data.fields:
        si_valid = data['SI_BR_b_to_sgamma'] != -1
        bsg_ok = si_valid & (data['SI_BR_b_to_sgamma'] > BSG_CENTRAL - 2 * BSG_SIGMA) & \
                 (data['SI_BR_b_to_sgamma'] < BSG_CENTRAL + 2 * BSG_SIGMA)
    else:
        bsg_ok = ak.ones_like(sp_valid, dtype=bool)

    if 'SI_BR_Bs_to_mumu' in data.fields:
        si_mumu_valid = data['SI_BR_Bs_to_mumu'] != -1
        bsmumu_ok = si_mumu_valid & (data['SI_BR_Bs_to_mumu'] > BSMUMU_CENTRAL - 2 * BSMUMU_SIGMA) & \
                    (data['SI_BR_Bs_to_mumu'] < BSMUMU_CENTRAL + 2 * BSMUMU_SIGMA)
    else:
        bsmumu_ok = ak.ones_like(sp_valid, dtype=bool)

    bphys_ok = bsg_ok & bsmumu_ok
    cuts['B-physics'] = quality & neutralino_lsp & higgs_ok & omega_ok & bphys_ok

    # SModelS
    if 'SModelS_bestExpUL_TheoryPrediction' in data.fields and 'SModelS_bestExpUL_UpperLimit' in data.fields:
        has_smodels = data['SModelS_bestExpUL_TheoryPrediction'] != -1
        has_ul = data['SModelS_bestExpUL_UpperLimit'] != -1
        smodels_ok = ~has_smodels | ~has_ul | \
                     (data['SModelS_bestExpUL_TheoryPrediction'] < data['SModelS_bestExpUL_UpperLimit'])
    else:
        smodels_ok = ak.ones_like(sp_valid, dtype=bool)

    cuts['SModelS allowed'] = quality & neutralino_lsp & higgs_ok & omega_ok & bphys_ok & smodels_ok

    # All cuts combined
    all_cuts = quality & neutralino_lsp & higgs_ok & omega_ok & bphys_ok & smodels_ok
    cuts['All cuts'] = all_cuts

    return cuts, all_cuts


def print_cutflow(cuts, n_total):
    """Print a cutflow table."""
    print("\n" + "=" * 60)
    print("CUTFLOW TABLE")
    print("=" * 60)
    print(f"{'Cut':<35} {'Pass':>8} {'/ Total':>10} {'Rate':>8}")
    print("-" * 60)
    for name, mask in cuts.items():
        n_pass = int(ak.sum(mask))
        rate = n_pass / n_total * 100 if n_total > 0 else 0
        print(f"{name:<35} {n_pass:>8} {'/ ' + str(n_total):>10} {rate:>7.1f}%")
    print("=" * 60)


def make_plots(data, all_cuts_mask, plot_dir):
    """Generate Phase 1 analysis plots."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available, skipping plots")
        return

    passing = data[all_cuts_mask]
    failing = data[~all_cuts_mask]

    # --- Plot 1: M_1 vs M_2 colored by pass/fail ---
    fig, ax = plt.subplots(figsize=(8, 7))
    if len(failing) > 0:
        ax.scatter(ak.to_numpy(failing['IN_M_1']), ak.to_numpy(failing['IN_M_2']),
                   c='lightgray', s=5, alpha=0.5, label=f'Fail ({len(failing)})')
    if len(passing) > 0:
        ax.scatter(ak.to_numpy(passing['IN_M_1']), ak.to_numpy(passing['IN_M_2']),
                   c='blue', s=10, alpha=0.7, label=f'Pass ({len(passing)})')
    ax.set_xlabel('M_1 [GeV]')
    ax.set_ylabel('M_2 [GeV]')
    ax.set_title('Phase 1: M_1 vs M_2')
    ax.legend()
    fig.savefig(os.path.join(plot_dir, 'phase1_M1_vs_M2.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)

    # --- Plot 2: mu vs M_1 ---
    fig, ax = plt.subplots(figsize=(8, 7))
    if len(failing) > 0:
        ax.scatter(ak.to_numpy(failing['IN_M_1']), ak.to_numpy(failing['IN_mu']),
                   c='lightgray', s=5, alpha=0.5, label=f'Fail ({len(failing)})')
    if len(passing) > 0:
        ax.scatter(ak.to_numpy(passing['IN_M_1']), ak.to_numpy(passing['IN_mu']),
                   c='blue', s=10, alpha=0.7, label=f'Pass ({len(passing)})')
    ax.set_xlabel('M_1 [GeV]')
    ax.set_ylabel('mu [GeV]')
    ax.set_title('Phase 1: M_1 vs mu')
    ax.legend()
    fig.savefig(os.path.join(plot_dir, 'phase1_M1_vs_mu.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)

    # --- Plot 3: Higgs mass distribution ---
    sp_valid = data['SP_m_h'] != -1
    m_h_all = ak.to_numpy(data['SP_m_h'][sp_valid])
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(m_h_all, bins=50, range=(80, 140), color='lightblue', edgecolor='black', label='All valid')
    if len(passing) > 0 and 'SP_m_h' in passing.fields:
        m_h_pass = ak.to_numpy(passing['SP_m_h'])
        ax.hist(m_h_pass[m_h_pass != -1], bins=50, range=(80, 140), color='blue', edgecolor='black',
                alpha=0.7, label='Passing all cuts')
    ax.axvline(122, color='red', linestyle='--', label='Cut window')
    ax.axvline(128, color='red', linestyle='--')
    ax.axvline(125.09, color='green', linestyle='-', linewidth=2, label='Measured (125.09)')
    ax.set_xlabel('m_h [GeV]')
    ax.set_ylabel('Models')
    ax.set_title('Phase 1: Higgs Mass Distribution')
    ax.legend()
    fig.savefig(os.path.join(plot_dir, 'phase1_higgs_mass.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)

    # --- Plot 4: Relic density distribution ---
    if 'MO_Omega' in data.fields:
        mo_valid = data['MO_Omega'] != -1
        omega_all = ak.to_numpy(data['MO_Omega'][mo_valid & (data['MO_Omega'] > 0)])
        if len(omega_all) > 0:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.hist(np.log10(omega_all), bins=50, color='lightblue', edgecolor='black')
            ax.axvline(np.log10(0.120), color='red', linestyle='--', label='Planck central (0.120)')
            ax.axvline(np.log10(0.132), color='red', linestyle='-', label='Upper bound (0.132)')
            ax.set_xlabel('log10(Omega h^2)')
            ax.set_ylabel('Models')
            ax.set_title('Phase 1: Dark Matter Relic Density')
            ax.legend()
            fig.savefig(os.path.join(plot_dir, 'phase1_relic_density.png'), dpi=150, bbox_inches='tight')
            plt.close(fig)

    # --- Plot 5: LSP type pie chart ---
    if 'SP_LSP_type' in data.fields and len(passing) > 0:
        lsp_types = ak.to_numpy(passing['SP_LSP_type'])
        bino_n = np.sum(lsp_types == 1)
        wino_n = np.sum(lsp_types == 2)
        higgsino_n = np.sum(lsp_types == 3)
        if bino_n + wino_n + higgsino_n > 0:
            fig, ax = plt.subplots(figsize=(7, 7))
            labels = [f'Bino ({bino_n})', f'Wino ({wino_n})', f'Higgsino ({higgsino_n})']
            sizes = [bino_n, wino_n, higgsino_n]
            colors = ['#ff9999', '#66b3ff', '#99ff99']
            # Filter out zero entries
            nonzero = [(l, s, c) for l, s, c in zip(labels, sizes, colors) if s > 0]
            if nonzero:
                labels, sizes, colors = zip(*nonzero)
                ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                ax.set_title('Phase 1: LSP Composition (passing models)')
                fig.savefig(os.path.join(plot_dir, 'phase1_lsp_composition.png'), dpi=150, bbox_inches='tight')
            plt.close(fig)

    # --- Plot 6: tanb vs mA ---
    fig, ax = plt.subplots(figsize=(8, 7))
    if len(failing) > 0:
        ax.scatter(ak.to_numpy(failing['IN_mA']), ak.to_numpy(failing['IN_tanb']),
                   c='lightgray', s=5, alpha=0.5, label=f'Fail ({len(failing)})')
    if len(passing) > 0:
        ax.scatter(ak.to_numpy(passing['IN_mA']), ak.to_numpy(passing['IN_tanb']),
                   c='blue', s=10, alpha=0.7, label=f'Pass ({len(passing)})')
    ax.set_xlabel('mA [GeV]')
    ax.set_ylabel('tan(beta)')
    ax.set_title('Phase 1: mA vs tan(beta)')
    ax.legend()
    fig.savefig(os.path.join(plot_dir, 'phase1_mA_vs_tanb.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)

    print(f"\nPlots saved to {plot_dir}/")


def main():
    scan_base = sys.argv[1] if len(sys.argv) > 1 else SCAN_BASE
    print(f"Analyzing scans in: {scan_base}")

    # Load data
    data = load_ntuples(scan_base)

    # Pipeline success rates
    pipeline = compute_pipeline_success(data)
    print("\n" + "=" * 50)
    print("PIPELINE SUCCESS RATES")
    print("=" * 50)
    for step, (ok, total) in pipeline.items():
        print(f"  {step:<15} {ok:>5} / {total:<5}  ({ok / total * 100:.1f}%)")

    # Physics cuts
    cuts, all_cuts_mask = compute_physics_cuts(data)
    print_cutflow(cuts, len(data))

    # Summary stats
    n_pass = int(ak.sum(all_cuts_mask))
    print(f"\nSummary: {n_pass} / {len(data)} models ({n_pass / len(data) * 100:.1f}%) pass all cuts")

    # Make plots
    make_plots(data, all_cuts_mask, PLOT_DIR)

    return data, cuts, all_cuts_mask


if __name__ == '__main__':
    main()
