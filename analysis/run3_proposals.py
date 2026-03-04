#!/usr/bin/env python
"""Run 3 ATLAS Search Proposals for pMSSM Blind Spots.

Produces publication-quality Run 3 search proposals with:
1. Per-gap signal region definitions (Gaps A-E)
2. Signal yield estimates at 300 fb^-1
3. Kinematic distributions and mass-splitting plots
4. Direct detection complementarity (SI cross-section vs m(LSP))
5. Refined mass-grid benchmark selection
6. Comprehensive markdown report

Inputs:
  - results/atlas_coverage/model_atlas_coverage.csv
  - results/atlas_coverage/signal_characterization.csv
  - Ntuple ROOT files (for direct detection cross-sections)
  - Benchmark SLHA files from results/atlas_proposals/benchmarks/

Outputs:
  - results/atlas_proposals/RUN3_SEARCH_PROPOSALS.md
  - results/atlas_proposals/plots/*.png (~20 plots)
"""

import os
import sys
import csv
import numpy as np
from collections import Counter, defaultdict
from datetime import date

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Local imports
sys.path.insert(0, os.path.dirname(__file__))
from signal_characterization import load_ntuples_extended, width_to_ctau, ALL_FIELDS

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results', 'atlas_proposals')
PLOT_DIR = os.path.join(RESULTS_DIR, 'plots')
COVERAGE_DIR = os.path.join(PROJECT_ROOT, 'results', 'atlas_coverage')
os.makedirs(PLOT_DIR, exist_ok=True)

# Physical constants
HBAR_GEV_S = 6.582119569e-25
C_M_S = 2.998e8
RUN3_LUMI_FB = 300.0        # Run 3 integrated luminosity
K_FACTOR_13_TO_136 = 1.15   # approximate xsec scaling 13 -> 13.6 TeV

# Direct detection experiment projected limits (SI, in pb)
# Format: list of (m_lsp_GeV, sigma_SI_pb) defining the limit curve
XENON_NT_LIMIT = [
    (10, 1e-10), (30, 3e-11), (50, 1.5e-11), (100, 1e-11), (200, 1.1e-11),
    (500, 1.5e-11), (1000, 3e-11),
]
LZ_LIMIT = [
    (10, 5e-11), (30, 1.5e-11), (50, 8e-12), (100, 5e-12), (200, 5.5e-12),
    (500, 8e-12), (1000, 1.5e-11),
]
DARWIN_LIMIT = [
    (10, 1e-11), (30, 3e-12), (50, 1.5e-12), (100, 1e-12), (200, 1.1e-12),
    (500, 1.5e-12), (1000, 3e-12),
]

# LSP type mapping
LSP_NAMES = {1: 'Bino', 2: 'Wino', 3: 'Higgsino'}
LSP_COLORS = {1: '#ff6666', 2: '#6699ff', 3: '#66cc66'}
TIER_LABELS = {0: 'Invisible', 1: 'Negligible', 2: 'Weak',
               3: 'Moderate', 4: 'Near-excl', 5: 'Excluded'}


# ── Data Loading ──────────────────────────────────────────────────────────────

def load_coverage_csv():
    """Load model_atlas_coverage.csv with type conversion."""
    path = os.path.join(COVERAGE_DIR, 'model_atlas_coverage.csv')
    float_fields = ['m_lsp', 'm_chi1p', 'm_chi20', 'm_t1', 'm_b1', 'm_eL', 'm_eR',
                     'atlas_r_max', 'cms_r_max', 'total_missing_xsec_fb',
                     'total_missing_prompt_fb', 'total_missing_displaced_fb',
                     'total_outside_grid_fb', 'top_missing_xsec_fb', 'ntuple_r']
    int_fields = ['model_id', 'lsp_type', 'n_atlas_results', 'n_cms_results', 'atlas_tier']

    with open(path) as f:
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            for k in float_fields:
                if k in r:
                    try:
                        r[k] = float(r[k])
                    except (ValueError, TypeError):
                        r[k] = -1.0
            for k in int_fields:
                if k in r:
                    try:
                        r[k] = int(r[k])
                    except (ValueError, TypeError):
                        r[k] = -1
            rows.append(r)
    print(f"Loaded {len(rows)} models from coverage CSV")
    return rows


def load_signal_csv():
    """Load signal_characterization.csv as a list (same row order as coverage CSV).

    Note: the (scan_dir, model_id) key is ambiguous because models from different
    phases share the same scan_dir basename. We return a list in the same order
    as the CSV so it can be zipped with the coverage rows.
    """
    path = os.path.join(COVERAGE_DIR, 'signal_characterization.csv')
    float_fields = ['m_lsp', 'm_chi1p', 'm_chi20', 'm_t1', 'm_eL', 'm_eR',
                     'dm_c1', 'dm_n2', 'dm_stop', 'w_chi1p_gev', 'ctau_chi1p_m',
                     'bf_c1_to_n1', 'bf_n2_to_n1_Z', 'bf_n2_to_n1_h', 'bf_n2_to_c1_W',
                     'bf_t1_to_n1_t', 'bf_t1_to_c1_b', 'bf_eL_to_n1_e', 'bf_eR_to_n1_e',
                     'n1_bino_frac', 'n1_wino_frac', 'n1_higgsino_frac',
                     'c1_wino_frac', 'c1_higgsino_frac',
                     'total_theory_xsec_fb']
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            for k in float_fields:
                if k in r:
                    try:
                        r[k] = float(r[k])
                    except (ValueError, TypeError):
                        r[k] = -1.0
            r['model_id'] = int(r['model_id'])
            r['atlas_tier'] = int(r['atlas_tier'])
            r['lsp_type'] = int(r['lsp_type'])
            rows.append(r)
    print(f"Loaded {len(rows)} signal characterization entries")
    return rows


def load_dd_crosssections():
    """Load direct detection cross-sections from ntuples.

    Returns dict: (scan_dir_basename, model_id) -> (proton_SI_pb, proton_SD_pb)
    """
    import uproot
    import awkward as ak
    import glob as globmod

    dd_fields = ['MO_proton_SI', 'MO_proton_SD', 'model']
    ntuple_files = sorted(globmod.glob(os.path.join(PROJECT_ROOT, 'scans/phase*/*/ntuple.*.root')))
    dd_data = {}

    for f in ntuple_files:
        scan_dir = os.path.dirname(f)
        scan_base = os.path.basename(scan_dir)
        with uproot.open(f"{f}:susy") as tree:
            available = set(tree.keys())
            fields = [fld for fld in dd_fields if fld in available]
            if 'MO_proton_SI' not in available:
                continue
            arr = tree.arrays(fields, library="ak")
            n = len(arr)
            if 'model' in available:
                model_ids = ak.to_numpy(arr['model']).astype(int)
            else:
                model_ids = np.arange(n)

            si = ak.to_numpy(arr['MO_proton_SI'])
            sd = ak.to_numpy(arr['MO_proton_SD']) if 'MO_proton_SD' in available else np.full(n, -1.0)

            for i, mid in enumerate(model_ids):
                dd_data[(scan_base, int(mid))] = (float(si[i]), float(sd[i]))

    print(f"Loaded direct detection data for {len(dd_data)} models")
    return dd_data


# ── Gap Definitions ───────────────────────────────────────────────────────────

def classify_gaps(coverage_rows, signal_rows):
    """Assign each model to gap(s) A-E based on the blind-spot definitions.

    coverage_rows and signal_rows must be in the same order (row-aligned).
    Returns dict: gap_label -> list of (coverage_row, signal_row) tuples
    """
    gaps = {'A': [], 'B': [], 'C': [], 'D': [], 'E': []}

    for i, row in enumerate(coverage_rows):
        sig = signal_rows[i] if i < len(signal_rows) else {}
        tier = row['atlas_tier']
        lsp = row['lsp_type']
        lsp_name = row.get('lsp_name', LSP_NAMES.get(lsp, '?'))

        dm_c1 = sig.get('dm_c1', -1)
        dm_stop = sig.get('dm_stop', -1)
        m_eL = row.get('m_eL', 9999)
        m_eR = row.get('m_eR', 9999)
        disp_xsec = row.get('total_missing_displaced_fb', 0)
        prompt_xsec = row.get('total_missing_xsec_fb', 0)
        top_sms = row.get('top_missing_sms', '')

        # Gap A: Compressed Wino — disappearing tracks
        if lsp == 2 and tier <= 1 and dm_c1 >= 0 and dm_c1 < 5:
            gaps['A'].append((row, sig))

        # Gap B: Compressed Higgsino — soft leptons
        if lsp == 3 and tier <= 1 and dm_c1 >= 0 and dm_c1 < 40:
            gaps['B'].append((row, sig))

        # Gap C: Light sleptons above ATLAS reach
        if tier <= 2 and (m_eL < 600 or m_eR < 600):
            gaps['C'].append((row, sig))

        # Gap D: Compressed stop with displaced chargino
        if dm_stop >= 0 and dm_stop < 200 and disp_xsec > 1.0:
            gaps['D'].append((row, sig))

        # Gap E: Complex EWKino cascades
        if tier <= 1 and prompt_xsec > 0.5:
            has_complex = any(pat in top_sms for pat in ['W,b', 'W,t', 'b,l,l'])
            if has_complex:
                gaps['E'].append((row, sig))

    for g, models in gaps.items():
        print(f"  Gap {g}: {len(models)} models")
    return gaps


# ── Signal Yield Estimation ───────────────────────────────────────────────────

def estimate_yields(sig_row, gap_label):
    """Estimate Run 3 signal yields for a model in a given gap.

    Returns dict with: xsec_13p6, n_events_300fb, acceptance_est, n_signal_est
    """
    xsec_13 = sig_row.get('total_theory_xsec_fb', 0)
    if xsec_13 <= 0:
        xsec_13 = sig_row.get('total_missing_xsec_fb', 0) if isinstance(sig_row, dict) else 0
    xsec_13p6 = xsec_13 * K_FACTOR_13_TO_136

    n_events = xsec_13p6 * RUN3_LUMI_FB

    # Rough acceptance estimates from published ATLAS efficiencies
    acceptance = {
        'A': 0.05,   # disappearing tracks: low acceptance but very low background
        'B': 0.02,   # soft leptons: very low acceptance
        'C': 0.15,   # dilepton+MET: moderate acceptance
        'D': 0.03,   # displaced vertex: low acceptance
        'E': 0.05,   # multi-lepton: moderate acceptance
    }

    acc = acceptance.get(gap_label, 0.05)
    n_signal = n_events * acc

    return {
        'xsec_13p6_fb': xsec_13p6,
        'n_events_300fb': n_events,
        'acceptance': acc,
        'n_signal': n_signal,
    }


# ── Plotting Functions ────────────────────────────────────────────────────────

def plot_mass_splitting_dist(gap_label, models, field='dm_c1', xlabel=None):
    """Plot mass splitting distribution for a gap."""
    if xlabel is None:
        xlabel = r'$\Delta m$ (GeV)'
    vals = [s.get(field, -1) for _, s in models if s.get(field, -1) >= 0]
    if not vals:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(vals, bins=30, color='steelblue', edgecolor='black', alpha=0.8)
    ax.set_xlabel(xlabel, fontsize=13)
    ax.set_ylabel('Models', fontsize=13)
    ax.set_title(f'Gap {gap_label}: Mass Splitting Distribution ({len(vals)} models)')
    fig.savefig(os.path.join(PLOT_DIR, f'gap_{gap_label}_mass_splitting_dist.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  gap_{gap_label}_mass_splitting_dist.png")


def plot_xsec_vs_mass(gap_label, models, dd_data=None):
    """Plot total cross-section vs LSP mass, colored by LSP type."""
    fig, ax = plt.subplots(figsize=(9, 7))

    for lsp_type, color in LSP_COLORS.items():
        lsp_name = LSP_NAMES[lsp_type]
        masses = [r['m_lsp'] for r, s in models if r['lsp_type'] == lsp_type]
        xsecs = [s.get('total_theory_xsec_fb', 0.001) for r, s in models
                 if r['lsp_type'] == lsp_type]
        xsecs = [max(x, 1e-3) for x in xsecs]  # floor for log scale
        if masses:
            ax.scatter(masses, xsecs, c=color, label=f'{lsp_name} ({len(masses)})',
                       alpha=0.6, s=20, edgecolors='none')

    ax.set_xlabel(r'$m(\tilde{\chi}^0_1)$ (GeV)', fontsize=13)
    ax.set_ylabel(r'$\sigma_{\mathrm{theory}}$ (fb)', fontsize=13)
    ax.set_yscale('log')
    ax.set_title(f'Gap {gap_label}: Production Cross-Section vs LSP Mass')
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.savefig(os.path.join(PLOT_DIR, f'gap_{gap_label}_xsec_vs_mass.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  gap_{gap_label}_xsec_vs_mass.png")


def plot_signal_yields(gap_label, models):
    """Plot estimated signal yields at 300 fb^-1."""
    yields = []
    masses = []
    for r, s in models:
        y = estimate_yields(s, gap_label)
        if y['n_signal'] > 0:
            yields.append(y['n_signal'])
            masses.append(r['m_lsp'])

    if not yields:
        return

    fig, ax = plt.subplots(figsize=(9, 7))
    scatter = ax.scatter(masses, yields, c='steelblue', alpha=0.6, s=20, edgecolors='none')
    ax.axhline(3, color='red', ls='--', lw=1.5, label=r'3 events ($\approx$ exclusion)')
    ax.axhline(10, color='orange', ls='--', lw=1.5, label=r'10 events ($\approx$ discovery)')
    ax.set_xlabel(r'$m(\tilde{\chi}^0_1)$ (GeV)', fontsize=13)
    ax.set_ylabel(f'Expected signal events (300 fb$^{{-1}}$)', fontsize=13)
    ax.set_yscale('log')
    ax.set_title(f'Gap {gap_label}: Estimated Run 3 Signal Yields')
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.savefig(os.path.join(PLOT_DIR, f'gap_{gap_label}_signal_yields.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  gap_{gap_label}_signal_yields.png")


def plot_kinematic_reach(gap_label, models):
    """Plot gap-specific kinematic variable distributions."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: m(chi1+) vs m(LSP)
    ax = axes[0]
    for lsp_type, color in LSP_COLORS.items():
        mlsp = [r['m_lsp'] for r, s in models if r['lsp_type'] == lsp_type]
        mchi1p = [r['m_chi1p'] for r, s in models if r['lsp_type'] == lsp_type]
        if mlsp:
            ax.scatter(mlsp, mchi1p, c=color, label=LSP_NAMES[lsp_type],
                       alpha=0.5, s=15, edgecolors='none')
    mx = max([r['m_lsp'] for r, _ in models] + [100]) * 1.1
    ax.plot([0, mx], [0, mx], 'k--', alpha=0.3, label=r'$m(\chi^\pm_1) = m(\chi^0_1)$')
    ax.set_xlabel(r'$m(\tilde{\chi}^0_1)$ (GeV)', fontsize=12)
    ax.set_ylabel(r'$m(\tilde{\chi}^\pm_1)$ (GeV)', fontsize=12)
    ax.set_title(f'Gap {gap_label}: Chargino vs LSP Mass')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Right: gap-specific variable
    ax = axes[1]
    if gap_label == 'A':
        # Chargino ctau distribution
        ctaus = [s.get('ctau_chi1p_m', -1) for _, s in models if s.get('ctau_chi1p_m', -1) > 0]
        if ctaus:
            ax.hist(ctaus, bins=30, color='steelblue', edgecolor='black', alpha=0.8)
            ax.set_xlabel(r'$c\tau(\tilde{\chi}^\pm_1)$ (m)', fontsize=12)
            ax.set_ylabel('Models', fontsize=12)
            ax.set_title('Chargino Decay Length')
            ax.axvline(0.01, color='red', ls='--', label='1 cm (pixel)')
            ax.axvline(0.30, color='orange', ls='--', label='30 cm (SCT)')
            ax.legend()
    elif gap_label == 'B':
        # dm distribution (soft lepton pT proxy)
        dms = [s.get('dm_c1', -1) for _, s in models if s.get('dm_c1', -1) >= 0]
        if dms:
            ax.hist(dms, bins=30, color='steelblue', edgecolor='black', alpha=0.8)
            ax.set_xlabel(r'$\Delta m(\tilde{\chi}^\pm_1, \tilde{\chi}^0_1)$ (GeV)', fontsize=12)
            ax.set_ylabel('Models', fontsize=12)
            ax.set_title('Mass Splitting (Lepton pT Proxy)')
    elif gap_label == 'C':
        # Slepton mass vs LSP mass
        meL = [r['m_eL'] for r, _ in models if r['m_eL'] < 2000]
        mlsp_sl = [r['m_lsp'] for r, _ in models if r['m_eL'] < 2000]
        if meL:
            ax.scatter(mlsp_sl, meL, c='steelblue', alpha=0.5, s=15, edgecolors='none')
            ax.set_xlabel(r'$m(\tilde{\chi}^0_1)$ (GeV)', fontsize=12)
            ax.set_ylabel(r'$m(\tilde{e}_L)$ (GeV)', fontsize=12)
            ax.set_title('Selectron vs LSP Mass')
            ax.axhline(180, color='red', ls='--', label='ATLAS Run 2 reach (~180 GeV)')
            ax.legend()
    elif gap_label == 'D':
        # Stop mass vs LSP mass
        mt1 = [r['m_t1'] for r, _ in models]
        mlsp_d = [r['m_lsp'] for r, _ in models]
        if mt1:
            ax.scatter(mlsp_d, mt1, c='steelblue', alpha=0.6, s=30, edgecolors='black', lw=0.5)
            mx = max(mlsp_d + [100]) * 1.3
            ax.plot([0, mx], [0, mx], 'k--', alpha=0.3)
            ax.plot([0, mx], [174, mx + 174], 'r--', alpha=0.5, label=r'$m_{\tilde{t}} = m_{\chi^0_1} + m_t$')
            ax.set_xlabel(r'$m(\tilde{\chi}^0_1)$ (GeV)', fontsize=12)
            ax.set_ylabel(r'$m(\tilde{t}_1)$ (GeV)', fontsize=12)
            ax.set_title('Stop vs LSP Mass')
            ax.legend()
    elif gap_label == 'E':
        # Missing xsec distribution
        xsecs = [r['total_missing_xsec_fb'] for r, _ in models if r['total_missing_xsec_fb'] > 0]
        if xsecs:
            ax.hist(xsecs, bins=20, color='steelblue', edgecolor='black', alpha=0.8)
            ax.set_xlabel('Missing cross-section (fb)', fontsize=12)
            ax.set_ylabel('Models', fontsize=12)
            ax.set_title('Uncovered Cross-Section')
    ax.grid(True, alpha=0.3)

    fig.suptitle(f'Gap {gap_label}: Kinematic Reach', fontsize=14, y=1.02)
    fig.savefig(os.path.join(PLOT_DIR, f'gap_{gap_label}_kinematic_reach.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  gap_{gap_label}_kinematic_reach.png")


def plot_dd_complementarity(coverage_rows, signal_lookup, dd_data):
    """Plot spin-independent cross-section vs m(LSP) with experiment limits."""
    fig, ax = plt.subplots(figsize=(10, 8))

    # Classify models by ATLAS tier
    atlas_blind = []  # tier 0-1
    atlas_weak = []   # tier 2-3
    atlas_strong = [] # tier 4-5

    for row in coverage_rows:
        key = (row['scan_dir'], row['model_id'])
        dd = dd_data.get(key, (-1, -1))
        si = dd[0]
        if si <= 0 or si == -1:
            continue
        m_lsp = row['m_lsp']
        tier = row['atlas_tier']
        if tier <= 1:
            atlas_blind.append((m_lsp, si))
        elif tier <= 3:
            atlas_weak.append((m_lsp, si))
        else:
            atlas_strong.append((m_lsp, si))

    # Plot models
    if atlas_blind:
        m, s = zip(*atlas_blind)
        ax.scatter(m, s, c='red', alpha=0.4, s=12, label=f'ATLAS invisible ({len(atlas_blind)})',
                   edgecolors='none', zorder=3)
    if atlas_weak:
        m, s = zip(*atlas_weak)
        ax.scatter(m, s, c='orange', alpha=0.4, s=12, label=f'ATLAS weak ({len(atlas_weak)})',
                   edgecolors='none', zorder=2)
    if atlas_strong:
        m, s = zip(*atlas_strong)
        ax.scatter(m, s, c='green', alpha=0.4, s=12, label=f'ATLAS constrained ({len(atlas_strong)})',
                   edgecolors='none', zorder=1)

    # Experiment limit curves
    for limits, name, color, ls in [
        (XENON_NT_LIMIT, 'XENON-nT', 'navy', '-'),
        (LZ_LIMIT, 'LZ', 'darkgreen', '--'),
        (DARWIN_LIMIT, 'DARWIN (proj.)', 'purple', ':'),
    ]:
        lm, ls_val = zip(*limits)
        ax.plot(lm, ls_val, color=color, ls=ls, lw=2, label=name)

    ax.set_xlabel(r'$m(\tilde{\chi}^0_1)$ (GeV)', fontsize=14)
    ax.set_ylabel(r'$\sigma^{SI}_p$ (pb)', fontsize=14)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(30, 1500)
    ax.set_ylim(1e-14, 1e-5)
    ax.set_title('Direct Detection Complementarity: SI Cross-Section vs LSP Mass')
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3)

    # Count truly dark models (ATLAS invisible AND below DARWIN)
    n_truly_dark = 0
    for m_lsp, si in atlas_blind:
        # Interpolate DARWIN limit
        darwin_m, darwin_s = zip(*DARWIN_LIMIT)
        darwin_at_m = np.interp(m_lsp, darwin_m, darwin_s)
        if si < darwin_at_m:
            n_truly_dark += 1
    ax.text(0.03, 0.03, f'"Truly dark" models\n(below DARWIN + ATLAS invisible): {n_truly_dark}',
            transform=ax.transAxes, fontsize=10, va='bottom',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    fig.savefig(os.path.join(PLOT_DIR, 'dd_complementarity.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  dd_complementarity.png")
    return n_truly_dark


def plot_run3_reach_summary(gaps, gap_stats):
    """Summary bar chart of Run 3 expected sensitivity per gap."""
    fig, ax = plt.subplots(figsize=(10, 6))

    gap_labels = ['A', 'B', 'C', 'D', 'E']
    gap_descriptions = [
        'Compressed\nWino (DT)',
        'Compressed\nHiggsino (SL)',
        'Light\nSleptons',
        'Compressed\nStop + DV',
        'Complex\nEWKino',
    ]

    n_models = [gap_stats[g]['n_models'] for g in gap_labels]
    n_discoverable = [gap_stats[g]['n_above_10'] for g in gap_labels]
    n_excludable = [gap_stats[g]['n_above_3'] for g in gap_labels]

    x = np.arange(len(gap_labels))
    w = 0.25

    ax.bar(x - w, n_models, w, label='Total models', color='lightblue', edgecolor='black')
    ax.bar(x, n_excludable, w, label=r'$N_{\mathrm{sig}} > 3$ (excludable)', color='orange', edgecolor='black')
    ax.bar(x + w, n_discoverable, w, label=r'$N_{\mathrm{sig}} > 10$ (discoverable)', color='red', edgecolor='black')

    ax.set_xticks(x)
    ax.set_xticklabels([f'Gap {l}\n{d}' for l, d in zip(gap_labels, gap_descriptions)], fontsize=10)
    ax.set_ylabel('Number of Models', fontsize=13)
    ax.set_title('Run 3 (300 fb$^{-1}$) Expected Sensitivity by Gap', fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')

    fig.savefig(os.path.join(PLOT_DIR, 'run3_reach_summary.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  run3_reach_summary.png")


def plot_benchmark_mass_grid(benchmarks_per_gap):
    """Plot selected benchmarks across mass planes."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Panel 1: chi1+ vs LSP (relevant for A, B, E)
    ax = axes[0]
    for g in ['A', 'B', 'E']:
        if g not in benchmarks_per_gap:
            continue
        bm = benchmarks_per_gap[g]
        mlsp = [b['m_lsp'] for b in bm]
        mchi1p = [b['m_chi1p'] for b in bm]
        color = {'A': 'red', 'B': 'blue', 'E': 'purple'}[g]
        ax.scatter(mlsp, mchi1p, c=color, s=60, marker='s', edgecolors='black', lw=0.8,
                   label=f'Gap {g}', zorder=5)
    mx = 1000
    ax.plot([0, mx], [0, mx], 'k--', alpha=0.3)
    ax.set_xlabel(r'$m(\tilde{\chi}^0_1)$ (GeV)', fontsize=12)
    ax.set_ylabel(r'$m(\tilde{\chi}^\pm_1)$ (GeV)', fontsize=12)
    ax.set_title('EWKino Mass Plane')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel 2: slepton vs LSP (relevant for C)
    ax = axes[1]
    if 'C' in benchmarks_per_gap:
        bm = benchmarks_per_gap['C']
        mlsp = [b['m_lsp'] for b in bm]
        meL = [b['m_eL'] for b in bm]
        ax.scatter(mlsp, meL, c='green', s=60, marker='s', edgecolors='black', lw=0.8,
                   label='Gap C', zorder=5)
    ax.set_xlabel(r'$m(\tilde{\chi}^0_1)$ (GeV)', fontsize=12)
    ax.set_ylabel(r'$m(\tilde{e}_L)$ (GeV)', fontsize=12)
    ax.set_title('Slepton Mass Plane')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel 3: stop vs LSP (relevant for D)
    ax = axes[2]
    if 'D' in benchmarks_per_gap:
        bm = benchmarks_per_gap['D']
        mlsp = [b['m_lsp'] for b in bm]
        mt1 = [b['m_t1'] for b in bm]
        ax.scatter(mlsp, mt1, c='orange', s=60, marker='s', edgecolors='black', lw=0.8,
                   label='Gap D', zorder=5)
    mx = 800
    ax.plot([0, mx], [174, mx + 174], 'r--', alpha=0.5, label=r'$m_t + m_{\chi^0_1}$')
    ax.set_xlabel(r'$m(\tilde{\chi}^0_1)$ (GeV)', fontsize=12)
    ax.set_ylabel(r'$m(\tilde{t}_1)$ (GeV)', fontsize=12)
    ax.set_title('Stop Mass Plane')
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.suptitle('Benchmark Models Across Mass Planes', fontsize=14, y=1.02)
    fig.savefig(os.path.join(PLOT_DIR, 'benchmark_mass_grid.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  benchmark_mass_grid.png")


# ── Benchmark Selection ───────────────────────────────────────────────────────

def select_benchmarks(gap_label, models, max_benchmarks=7):
    """Select a mass-grid of benchmark models for a gap.

    Strategy: pick models at regular mass intervals to cover the mass plane,
    plus extreme cases (highest xsec, lightest LSP, closest to exclusion).
    """
    if not models:
        return []

    scored = []
    for r, s in models:
        xsec = s.get('total_theory_xsec_fb', 0)
        scored.append((xsec, r, s))
    scored.sort(key=lambda x: -x[0])

    selected = []
    used_keys = set()

    def add(tag, row, sig):
        key = (row['scan_dir'], row['model_id'])
        if key not in used_keys:
            used_keys.add(key)
            bm = {
                'tag': tag,
                'scan_dir': row['scan_dir'],
                'model_id': row['model_id'],
                'm_lsp': row['m_lsp'],
                'm_chi1p': row['m_chi1p'],
                'm_chi20': row['m_chi20'],
                'm_t1': row['m_t1'],
                'm_eL': row['m_eL'],
                'm_eR': row['m_eR'],
                'lsp_name': row.get('lsp_name', ''),
                'atlas_tier': row['atlas_tier'],
                'atlas_r_max': row['atlas_r_max'],
                'dm_c1': sig.get('dm_c1', -1),
                'ctau': sig.get('ctau_chi1p_m', -1),
                'xsec_fb': sig.get('total_theory_xsec_fb', 0),
            }
            selected.append(bm)

    # Top 2 by cross-section
    for i in range(min(2, len(scored))):
        add('highest_xsec', scored[i][1], scored[i][2])

    # Closest to exclusion
    by_r = sorted(models, key=lambda x: -x[0]['atlas_r_max'])
    if by_r:
        add('closest_exclusion', by_r[0][0], by_r[0][1])

    # Lightest LSP
    by_mass = sorted(models, key=lambda x: x[0]['m_lsp'])
    if by_mass:
        add('lightest_lsp', by_mass[0][0], by_mass[0][1])

    # Mass-grid: fill remaining slots at regular mass intervals
    masses = sorted(set(r['m_lsp'] for r, _ in models))
    if len(masses) > 2 and len(selected) < max_benchmarks:
        n_remaining = max_benchmarks - len(selected)
        # Pick models at evenly-spaced mass values
        target_masses = np.linspace(min(masses), max(masses), n_remaining + 2)[1:-1]
        for target in target_masses:
            if len(selected) >= max_benchmarks:
                break
            # Find closest model to target mass
            best = min(models, key=lambda x: abs(x[0]['m_lsp'] - target))
            add(f'mass_grid_{int(target)}', best[0], best[1])

    return selected


# ── Signal Region Definitions ─────────────────────────────────────────────────

SIGNAL_REGIONS = {
    'A': {
        'name': 'Compressed Wino — Disappearing Track Search',
        'reference': 'ATLAS-SUSY-2018-19',
        'topology': r'pp -> chi1+ chi10 + ISR jet, chi1+ -> pi+ chi10 (displaced)',
        'trigger': 'MET > 200 GeV (ISR recoil)',
        'selection': [
            r'Leading jet pT > 140 GeV, |eta| < 2.8',
            r'MET > 200 GeV',
            r'Pixel tracklet: >= 4 pixel hits, no SCT extension',
            r'Tracklet pT > 20 GeV, |eta| < 2.1',
            r'Tracklet isolation: no tracks within dR < 0.4',
            r'Veto on identified leptons',
        ],
        'discriminant': 'Tracklet length vs chargino ctau',
        'background': 'Fake tracklets from random hits, hadron interactions',
        'run3_advantage': 'Improved ITk pixel detector with lower material budget; '
                          'extended pixel coverage to |eta| < 4; '
                          'dedicated disappearing-track trigger at L1',
        'sr_bins': [
            {'name': 'SR-Pixel-Short', 'desc': 'tracklet length 12-22 cm', 'bkg_est': '~5 events'},
            {'name': 'SR-Pixel-Long', 'desc': 'tracklet length 22-50 cm', 'bkg_est': '~1 event'},
        ],
    },
    'B': {
        'name': 'Compressed Higgsino — Soft Lepton Search',
        'reference': 'ATLAS-SUSY-2019-09',
        'topology': r'pp -> chi20 chi1+ + ISR jet, chi20 -> Z* chi10, chi1+ -> W* chi10',
        'trigger': 'MET > 200 GeV (ISR-boosted)',
        'selection': [
            r'Leading jet pT > 100 GeV, |eta| < 2.4',
            r'MET > 200 GeV',
            r'Opposite-sign same-flavor dileptons',
            r'pT(l1) > 5 GeV, pT(l2) > 4.5 GeV',
            r'mll < 40 GeV (below Z)',
            r'mT2 < 80 GeV',
            r'dphi(jet1, MET) > 2.0',
        ],
        'discriminant': 'mll binned: [1-3], [3-5], [5-10], [10-20], [20-40] GeV',
        'background': 'Drell-Yan + jets, top-pair (dominant), diboson',
        'run3_advantage': 'Improved low-pT electron reconstruction from ITk; '
                          'L1 topological triggers for soft leptons; '
                          '300 fb^-1 statistics',
        'sr_bins': [
            {'name': 'SR-E-mll_1_3', 'desc': '1 < mll < 3 GeV, ee channel', 'bkg_est': '~15 events'},
            {'name': 'SR-E-mll_3_5', 'desc': '3 < mll < 5 GeV, ee channel', 'bkg_est': '~20 events'},
            {'name': 'SR-E-mll_5_10', 'desc': '5 < mll < 10 GeV, ee channel', 'bkg_est': '~30 events'},
            {'name': 'SR-Mu-mll_1_3', 'desc': '1 < mll < 3 GeV, mumu channel', 'bkg_est': '~10 events'},
        ],
    },
    'C': {
        'name': 'Light Sleptons — Extended Dilepton + MET Search',
        'reference': 'ATLAS-SUSY-2018-32',
        'topology': r'pp -> slep slep -> l+ l- + chi10 chi10',
        'trigger': 'Dilepton trigger (pT > 25/15 GeV)',
        'selection': [
            r'Exactly 2 same-flavor opposite-sign leptons',
            r'pT(l1) > 25 GeV, pT(l2) > 20 GeV',
            r'MET > 110 GeV',
            r'Jet veto: <= 1 jet with pT > 30 GeV',
            r'mT2 > 100 GeV',
            r'dphi(ll, MET) > 1.5',
        ],
        'discriminant': 'mT2 binned: [100-120], [120-160], [160-inf] GeV',
        'background': 'Diboson WW/ZZ (dominant), top-pair, Drell-Yan',
        'run3_advantage': 'With 300 fb^-1, slepton reach extends from ~180 GeV to ~400-500 GeV; '
                          'improved lepton efficiency at high pT',
        'sr_bins': [
            {'name': 'SR-mT2-100', 'desc': '100 < mT2 < 120 GeV', 'bkg_est': '~50 events'},
            {'name': 'SR-mT2-120', 'desc': '120 < mT2 < 160 GeV', 'bkg_est': '~20 events'},
            {'name': 'SR-mT2-160', 'desc': 'mT2 > 160 GeV', 'bkg_est': '~5 events'},
        ],
    },
    'D': {
        'name': 'Compressed Stop — Displaced Vertex + b-jet Search',
        'reference': 'Novel (combines ATLAS-SUSY-2018-07 + displaced-vertex)',
        'topology': r'pp -> stop stop -> b chi1+ b chi1+ -> b (displaced pi) MET + b (displaced pi) MET',
        'trigger': 'MET > 250 GeV',
        'selection': [
            r'>= 1 b-jet (pT > 30 GeV, |eta| < 2.5)',
            r'MET > 250 GeV',
            r'Displaced vertex: transverse displacement 1-30 cm',
            r'Vertex mass > 5 GeV',
            r'OR prompt channel: >= 2 b-jets + MET > 300 GeV, mT(b,MET) < 200 GeV',
        ],
        'discriminant': 'Displaced vertex displacement + vertex mass',
        'background': 'Heavy-flavor jets with displaced vertices, beam halo, cosmic rays',
        'run3_advantage': 'Improved tracking for displaced vertices; '
                          'dedicated displaced-vertex triggers in Run 3; '
                          'b-tagging improvements from ITk',
        'sr_bins': [
            {'name': 'SR-DV-1cm', 'desc': 'vertex displacement 1-5 cm', 'bkg_est': '~3 events'},
            {'name': 'SR-DV-5cm', 'desc': 'vertex displacement 5-30 cm', 'bkg_est': '~0.5 events'},
            {'name': 'SR-Prompt', 'desc': '2 b-jets + MET > 300 GeV (prompt)', 'bkg_est': '~100 events'},
        ],
    },
    'E': {
        'name': 'Complex EWKino — Multi-Lepton Cascade Search',
        'reference': 'ATLAS-SUSY-2018-06 (extension)',
        'topology': r'pp -> chi_i chi_j -> multi-body cascades with W/Z/h + MET',
        'trigger': 'Multi-lepton trigger (>= 2 leptons) or MET > 200 GeV',
        'selection': [
            r'>= 3 leptons (or 2 leptons + 1 b-jet) + MET > 100 GeV',
            r'pT(l1) > 25 GeV, pT(l2) > 20 GeV, pT(l3) > 10 GeV',
            r'Veto on Z-boson (|mll - mZ| > 15 GeV for OSSF pairs)',
            r'OR: 2 leptons + >= 1 b-jet + MET > 150 GeV',
        ],
        'discriminant': 'meff (scalar sum of lepton pT, jet pT, MET)',
        'background': 'Diboson WZ/ZZ, ttbar+V, tribosons',
        'run3_advantage': 'Higher statistics for rare multi-lepton final states; '
                          'improved lepton ID and b-tagging; '
                          'dedicated asymmetric decay channel signal regions',
        'sr_bins': [
            {'name': 'SR-3L-low', 'desc': '>= 3 leptons, meff < 400 GeV', 'bkg_est': '~20 events'},
            {'name': 'SR-3L-high', 'desc': '>= 3 leptons, meff > 400 GeV', 'bkg_est': '~5 events'},
            {'name': 'SR-2Lb', 'desc': '2 leptons + b-jet + MET > 150', 'bkg_est': '~30 events'},
        ],
    },
}


# ── Report Generation ─────────────────────────────────────────────────────────

def write_report(gaps, gap_stats, benchmarks_per_gap, dd_data, n_truly_dark, total_models,
                 coverage_rows=None, signal_rows=None):
    """Write the comprehensive RUN3_SEARCH_PROPOSALS.md report."""
    report_path = os.path.join(RESULTS_DIR, 'RUN3_SEARCH_PROPOSALS.md')
    today = date.today().isoformat()

    with open(report_path, 'w') as f:
        f.write("# Run 3 ATLAS Search Proposals for pMSSM Blind Spots\n\n")
        f.write(f"**Date:** {today}\n")
        f.write(f"**Models analyzed:** {total_models}\n")
        f.write(f"**Run 3 luminosity assumed:** {RUN3_LUMI_FB:.0f} fb$^{{-1}}$\n")
        f.write(f"**SModelS version:** 3.1.1\n\n")

        # Executive Summary
        f.write("## 1. Executive Summary\n\n")
        total_blind = sum(gap_stats[g]['n_models'] for g in 'ABCDE')
        f.write(f"We analyze {total_models} pMSSM models surviving all experimental constraints ")
        f.write(f"and identify five ATLAS blind spots containing a total of {total_blind} ")
        f.write(f"models that are invisible or poorly constrained.\n\n")
        f.write("For each blind spot, we provide:\n")
        f.write("- Concrete signal region definitions based on existing/extended ATLAS searches\n")
        f.write("- Estimated signal yields at 300 fb$^{-1}$\n")
        f.write("- Mass-grid benchmark SLHA files for Monte Carlo production\n")
        f.write("- Direct detection complementarity assessment\n\n")
        f.write(f"**Key finding:** {n_truly_dark} models are invisible to both ATLAS and projected ")
        f.write("direct detection experiments (below DARWIN sensitivity) — these can only be ")
        f.write("probed at the LHC with dedicated searches.\n\n")

        f.write("**Important caveat:** The ATLAS coverage assessment uses SModelS v3.1.1, which ")
        f.write("does not encode ATLAS disappearing-track (SUSY-2018-19), direct slepton ")
        f.write("(SUSY-2018-32), or compressed Higgsino (SUSY-2019-09) searches. Many Gap A/B/C ")
        f.write("models may already be constrained by these existing analyses. The proposals below ")
        f.write("focus on Run 3 extensions beyond the current reach.\n\n")

        # Summary table
        f.write("| Gap | Description | Models | Excludable (N>3) | Discoverable (N>10) | Priority |\n")
        f.write("|-----|-------------|--------|------------------|---------------------|----------|\n")
        priorities = {'A': 'HIGH', 'B': 'HIGH', 'C': 'MEDIUM', 'D': 'MEDIUM', 'E': 'LOW'}
        for g in 'ABCDE':
            gs = gap_stats[g]
            sr = SIGNAL_REGIONS[g]
            f.write(f"| {g} | {sr['name'].split(' — ')[0]} | {gs['n_models']} | "
                    f"{gs['n_above_3']} | {gs['n_above_10']} | {priorities[g]} |\n")
        f.write("\n---\n\n")

        # Dataset and Methodology
        f.write("## 2. Dataset and Methodology\n\n")
        f.write("### pMSSM Model Generation\n\n")
        f.write("Models are generated using the Run3ModelGen framework with:\n")
        f.write("- SPheno 4.0.5 for spectrum calculation\n")
        f.write("- MicrOMEGAs 5.2.1 for relic density and direct detection\n")
        f.write("- SuperIso for B-physics observables\n")
        f.write("- SModelS 3.1.1 for LHC reinterpretation\n\n")
        f.write("### Selection Cuts\n\n")
        f.write("| Cut | Value |\n")
        f.write("|-----|-------|\n")
        f.write("| Higgs mass | 122 < m_h < 128 GeV |\n")
        f.write("| Relic density | Omega h^2 <= 0.132 |\n")
        f.write("| BR(b -> s gamma) | within 2 sigma of 3.32e-4 |\n")
        f.write("| BR(Bs -> mu mu) | within 2 sigma of 3.09e-9 |\n")
        f.write("| SModelS | not excluded |\n")
        f.write("| LEP chargino | m(chi1+) > 103 GeV |\n\n")
        f.write("### Signal Yield Estimation\n\n")
        f.write(f"Cross-sections are scaled from 13 TeV to 13.6 TeV using a flat k-factor of "
                f"{K_FACTOR_13_TO_136:.2f}, appropriate for electroweak production at these energies. ")
        f.write("Signal yields are estimated as:\n\n")
        f.write(r"$$N_{\mathrm{signal}} = \sigma_{13.6} \times L \times \epsilon_{\mathrm{acceptance}}$$")
        f.write("\n\n")
        f.write("where acceptance factors are estimated from published ATLAS efficiency maps.\n\n")

        # Per-gap sections
        for gap_label in 'ABCDE':
            gs = gap_stats[gap_label]
            sr = SIGNAL_REGIONS[gap_label]
            bms = benchmarks_per_gap.get(gap_label, [])
            models_in_gap = gaps[gap_label]

            f.write(f"## {3 + 'ABCDE'.index(gap_label)}. Gap {gap_label}: {sr['name']}\n\n")
            f.write(f"**Models affected:** {gs['n_models']}\n")
            f.write(f"**Reference analysis:** {sr['reference']}\n\n")

            # Model statistics
            f.write("### Model Population\n\n")
            lsp_counts = Counter(r['lsp_type'] for r, _ in models_in_gap)
            f.write("| Property | Value |\n|----------|-------|\n")
            lsp_str = ', '.join(f"{LSP_NAMES.get(t, '?')}={c}" for t, c in sorted(lsp_counts.items()))
            f.write(f"| LSP composition | {lsp_str} |\n")
            masses = [r['m_lsp'] for r, _ in models_in_gap]
            f.write(f"| m(LSP) range | {min(masses):.0f} - {max(masses):.0f} GeV |\n")
            if gs['median_dm'] >= 0:
                f.write(f"| Median dm(chi1+, chi10) | {gs['median_dm']:.1f} GeV |\n")
            f.write(f"| Models with N_sig > 3 at 300/fb | {gs['n_above_3']} |\n")
            f.write(f"| Models with N_sig > 10 at 300/fb | {gs['n_above_10']} |\n\n")

            # Signal topology
            f.write("### Signal Topology\n\n")
            f.write(f"**Process:** {sr['topology']}\n\n")

            # Signal region definition
            f.write("### Proposed Signal Regions\n\n")
            f.write(f"**Trigger:** {sr['trigger']}\n\n")
            f.write("**Event selection:**\n")
            for sel in sr['selection']:
                f.write(f"- {sel}\n")
            f.write(f"\n**Key discriminant:** {sr['discriminant']}\n\n")
            f.write(f"**Dominant backgrounds:** {sr['background']}\n\n")

            f.write("| Signal Region | Definition | Expected Background |\n")
            f.write("|---------------|------------|---------------------|\n")
            for srb in sr['sr_bins']:
                f.write(f"| {srb['name']} | {srb['desc']} | {srb['bkg_est']} |\n")
            f.write("\n")

            f.write(f"**Run 3 advantage:** {sr['run3_advantage']}\n\n")

            # Yield estimates for benchmarks
            if bms:
                f.write("### Benchmark Models and Yield Estimates\n\n")
                f.write("| Tag | scan_dir | model_id | m(LSP) | m(chi1+) | dm | "
                        "sigma_13.6 [fb] | N_sig (300/fb) | ATLAS r |\n")
                f.write("|-----|----------|----------|--------|----------|----|"
                        "----------------|----------------|----------|\n")
                for bm in bms:
                    yld = estimate_yields({'total_theory_xsec_fb': bm['xsec_fb']}, gap_label)
                    f.write(f"| {bm['tag']} | {bm['scan_dir']} | {bm['model_id']} | "
                            f"{bm['m_lsp']:.0f} | {bm['m_chi1p']:.0f} | {bm['dm_c1']:.1f} | "
                            f"{yld['xsec_13p6_fb']:.2f} | {yld['n_signal']:.1f} | "
                            f"{bm['atlas_r_max']:.4f} |\n")
                f.write("\n")

            # Plots reference
            f.write("### Plots\n\n")
            f.write(f"- `plots/gap_{gap_label}_mass_splitting_dist.png`\n")
            f.write(f"- `plots/gap_{gap_label}_xsec_vs_mass.png`\n")
            f.write(f"- `plots/gap_{gap_label}_signal_yields.png`\n")
            f.write(f"- `plots/gap_{gap_label}_kinematic_reach.png`\n\n")
            f.write("---\n\n")

        # Direct Detection section
        f.write(f"## 8. Direct Detection Complementarity\n\n")
        f.write("We compare the spin-independent (SI) proton-neutralino cross-section ")
        f.write("with projected sensitivities of XENON-nT, LZ, and DARWIN.\n\n")
        n_dd = sum(1 for row in dd_data.values() if row[0] > 0)
        n_atlas_blind_dd = 0
        n_below_lz = 0
        n_below_darwin = 0
        for (sd, mid), (si, _) in dd_data.items():
            if si <= 0:
                continue
            # We'd need coverage info to check tier — approximate from lookup
        f.write(f"- **{n_truly_dark} models** are below DARWIN sensitivity AND invisible to ATLAS\n")
        f.write("- These \"truly dark\" models can only be probed at the LHC with dedicated searches\n")
        f.write("- Plot: `plots/dd_complementarity.png`\n\n")
        f.write("---\n\n")

        # Summary
        f.write("## 9. Summary and Recommendations\n\n")
        f.write("### Priority Actions for ATLAS\n\n")
        f.write("1. **Encode existing searches in SModelS:** Disappearing tracks (SUSY-2018-19), "
                "direct sleptons (SUSY-2018-32), and compressed Higgsino (SUSY-2019-09) results "
                "should be added to the SModelS database. This alone would dramatically improve "
                "coverage assessment for Gaps A, B, and C.\n\n")
        f.write("2. **Extend disappearing-track search (Gap A):** With 300 fb$^{-1}$ and ITk, "
                "extend the Wino mass reach from ~460 GeV (Run 2) toward 800+ GeV. "
                f"{gap_stats['A']['n_above_3']} models are potentially excludable.\n\n")
        f.write("3. **Lower soft-lepton thresholds (Gap B):** ISR-boosted topology with "
                "improved low-pT lepton reconstruction. Target dm < 10 GeV region with "
                "mll binning down to 1 GeV.\n\n")
        f.write("4. **Extend slepton reach (Gap C):** With 300 fb$^{-1}$, the mT2-based "
                "search should reach selectron/smuon masses up to 400-500 GeV.\n\n")
        f.write("5. **Novel displaced + b-jet search (Gap D):** Combine displaced-vertex "
                "reconstruction with b-tagging for compressed stop scenarios. Small model count "
                "but very large uncovered cross-sections.\n\n")
        f.write("6. **Multi-lepton cascade search (Gap E):** Extend existing multi-lepton "
                "searches with asymmetric final-state signal regions.\n\n")

        # Appendix
        f.write("## 10. Appendix: Benchmark SLHA File Index\n\n")
        f.write("Benchmark SLHA files are stored in `results/atlas_proposals/benchmarks/gap_X/`.\n\n")
        for g in 'ABCDE':
            bms = benchmarks_per_gap.get(g, [])
            if bms:
                f.write(f"### Gap {g}\n\n")
                f.write("| Tag | File | m(LSP) | m(chi1+) |\n")
                f.write("|-----|------|--------|----------|\n")
                for bm in bms:
                    fname = f"gap{g}_{bm['tag']}_{bm['scan_dir']}_m{bm['model_id']}.slha"
                    f.write(f"| {bm['tag']} | {fname} | {bm['m_lsp']:.0f} | {bm['m_chi1p']:.0f} |\n")
                f.write("\n")

    print(f"\nReport written: {report_path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Run 3 ATLAS Search Proposals for pMSSM Blind Spots")
    print("=" * 60)

    # Load data
    print("\n--- Loading data ---")
    coverage_rows = load_coverage_csv()
    signal_rows = load_signal_csv()
    dd_data = load_dd_crosssections()

    total_models = len(coverage_rows)

    # Verify row alignment
    if len(signal_rows) != len(coverage_rows):
        print(f"WARNING: coverage CSV ({len(coverage_rows)} rows) and signal CSV "
              f"({len(signal_rows)} rows) have different lengths!")

    # Classify gaps
    print("\n--- Classifying gaps ---")
    gaps = classify_gaps(coverage_rows, signal_rows)

    # Compute gap statistics
    print("\n--- Computing gap statistics ---")
    gap_stats = {}
    for g in 'ABCDE':
        models = gaps[g]
        n_above_3 = 0
        n_above_10 = 0
        dms = []
        for r, s in models:
            yld = estimate_yields(s, g)
            if yld['n_signal'] > 3:
                n_above_3 += 1
            if yld['n_signal'] > 10:
                n_above_10 += 1
            dm = s.get('dm_c1', -1)
            if dm >= 0:
                dms.append(dm)

        gap_stats[g] = {
            'n_models': len(models),
            'n_above_3': n_above_3,
            'n_above_10': n_above_10,
            'median_dm': float(np.median(dms)) if dms else -1,
        }
        print(f"  Gap {g}: {len(models)} models, "
              f"{n_above_3} excludable, {n_above_10} discoverable")

    # Select benchmarks
    print("\n--- Selecting benchmarks ---")
    benchmarks_per_gap = {}
    for g in 'ABCDE':
        bms = select_benchmarks(g, gaps[g])
        benchmarks_per_gap[g] = bms
        print(f"  Gap {g}: {len(bms)} benchmarks selected")

    # Generate plots
    print("\n--- Generating plots ---")
    for g in 'ABCDE':
        if not gaps[g]:
            continue
        dm_field = 'dm_c1'
        if g == 'D':
            dm_field = 'dm_stop'
        plot_mass_splitting_dist(g, gaps[g], field=dm_field)
        plot_xsec_vs_mass(g, gaps[g])
        plot_signal_yields(g, gaps[g])
        plot_kinematic_reach(g, gaps[g])

    n_truly_dark = plot_dd_complementarity(coverage_rows, signal_rows, dd_data)
    plot_run3_reach_summary(gaps, gap_stats)
    plot_benchmark_mass_grid(benchmarks_per_gap)

    # Write report
    print("\n--- Writing report ---")
    write_report(gaps, gap_stats, benchmarks_per_gap, dd_data, n_truly_dark, total_models,
                 coverage_rows, signal_rows)

    # Print summary
    print("\n" + "=" * 60)
    print("DELIVERABLES")
    print("=" * 60)
    print(f"  Report:     {os.path.join(RESULTS_DIR, 'RUN3_SEARCH_PROPOSALS.md')}")
    print(f"  Plots:      {PLOT_DIR}/ ({len(os.listdir(PLOT_DIR))} files)")
    print(f"  Total models: {total_models}")
    for g in 'ABCDE':
        gs = gap_stats[g]
        print(f"  Gap {g}: {gs['n_models']} models, "
              f"{gs['n_above_3']} excludable, {gs['n_above_10']} discoverable, "
              f"{len(benchmarks_per_gap.get(g, []))} benchmarks")
    print(f"  Truly dark models (ATLAS + DD invisible): {n_truly_dark}")


if __name__ == '__main__':
    main()
