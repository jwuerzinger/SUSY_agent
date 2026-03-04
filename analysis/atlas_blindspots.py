#!/usr/bin/env python
"""ATLAS blind spot characterization and diagnostic plots.

Reads the CSV produced by atlas_coverage.py and creates:
1. ATLAS r_max vs CMS r_max scatter (colored by LSP type)
2. ATLAS r_max vs m(LSP) by LSP type
3. Mass-plane maps: m(chi1+) vs m(chi10), m(slepton) vs m(chi10), m(stop) vs m(chi10)
4. Missing topology bar chart
5. Coverage tier x physics category heatmap
6. BLINDSPOT_REPORT.md

Requires: results/atlas_coverage/model_atlas_coverage.csv (from atlas_coverage.py)
"""

import os
import sys
import csv
import numpy as np
from collections import Counter, defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results', 'atlas_coverage')
PLOT_DIR = os.path.join(RESULTS_DIR, 'plots')
CONTOUR_DIR = os.path.join(PROJECT_ROOT, 'results', 'atlas_contours')
os.makedirs(PLOT_DIR, exist_ok=True)


def load_contour(csv_path):
    """Load a 2-column CSV contour file, return (x, y) numpy arrays.
    Returns (None, None) if file doesn't exist."""
    if not os.path.isfile(csv_path):
        return None, None
    x, y = [], []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames
        for row in reader:
            x.append(float(row[cols[0]]))
            y.append(float(row[cols[1]]))
    return np.array(x), np.array(y)


def load_coverage_csv():
    """Load model_atlas_coverage.csv into list of dicts with numeric conversion."""
    csv_path = os.path.join(RESULTS_DIR, 'model_atlas_coverage.csv')
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Convert numeric fields
    float_fields = [
        'm_lsp', 'm_chi1p', 'm_chi20', 'm_t1', 'm_b1', 'm_eL', 'm_eR',
        'ntuple_r', 'atlas_r_max', 'cms_r_max',
        'total_missing_xsec_fb', 'total_missing_prompt_fb',
        'total_missing_displaced_fb', 'total_outside_grid_fb',
        'top_missing_xsec_fb',
    ]
    int_fields = ['lsp_type', 'n_atlas_results', 'n_cms_results', 'atlas_tier', 'model_id']

    for row in rows:
        for fld in float_fields:
            row[fld] = float(row[fld])
        for fld in int_fields:
            row[fld] = int(row[fld])
        row['categories'] = row['categories'].split(';') if row['categories'] else []

    return rows


def plot_atlas_vs_cms(rows):
    """Scatter: ATLAS r_max vs CMS r_max, colored by LSP type."""
    fig, ax = plt.subplots(figsize=(9, 8))

    colors = {1: '#ff6666', 2: '#6699ff', 3: '#66cc66'}
    labels = {1: 'Bino', 2: 'Wino', 3: 'Higgsino'}

    for lt in [1, 2, 3]:
        subset = [r for r in rows if r['lsp_type'] == lt]
        if not subset:
            continue
        atlas_r = np.array([r['atlas_r_max'] for r in subset])
        cms_r = np.array([r['cms_r_max'] for r in subset])
        # Clip zeros to small value for log scale
        atlas_r_plot = np.where(atlas_r > 0, atlas_r, 1e-5)
        cms_r_plot = np.where(cms_r > 0, cms_r, 1e-5)
        ax.scatter(cms_r_plot, atlas_r_plot, c=colors[lt], s=20, alpha=0.7,
                   label=f'{labels[lt]} ({len(subset)})', edgecolors='black', linewidths=0.3)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(5e-6, 5)
    ax.set_ylim(5e-6, 5)
    ax.axhline(1.0, color='red', linestyle='--', alpha=0.5, label='Exclusion (r=1)')
    ax.axvline(1.0, color='red', linestyle='--', alpha=0.5)
    ax.axhline(0.01, color='gray', linestyle=':', alpha=0.4)
    ax.axvline(0.01, color='gray', linestyle=':', alpha=0.4)
    ax.plot([1e-5, 5], [1e-5, 5], 'k:', alpha=0.3)
    ax.set_xlabel('CMS r_max', fontsize=13)
    ax.set_ylabel('ATLAS r_max', fontsize=13)
    ax.set_title('ATLAS vs CMS Sensitivity (458 Surviving pMSSM Models)', fontsize=14)
    ax.legend(fontsize=11)

    # Annotate quadrants
    ax.text(2e-4, 2.0, 'ATLAS covers\nCMS misses', fontsize=9, ha='center', alpha=0.5)
    ax.text(2.0, 2e-4, 'CMS covers\nATLAS misses', fontsize=9, ha='center', alpha=0.5)
    ax.text(2e-4, 2e-4, 'Both miss', fontsize=9, ha='center', alpha=0.5, color='red')

    fig.savefig(os.path.join(PLOT_DIR, 'atlas_vs_cms.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("  atlas_vs_cms.png")


def plot_atlas_r_vs_mlsp(rows):
    """ATLAS r_max vs m(LSP), by LSP type."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

    colors = {1: '#ff6666', 2: '#6699ff', 3: '#66cc66'}
    labels = {1: 'Bino', 2: 'Wino', 3: 'Higgsino'}

    for idx, lt in enumerate([1, 2, 3]):
        ax = axes[idx]
        subset = [r for r in rows if r['lsp_type'] == lt]
        if not subset:
            continue
        m_lsp = np.array([r['m_lsp'] for r in subset])
        atlas_r = np.array([r['atlas_r_max'] for r in subset])
        atlas_r_plot = np.where(atlas_r > 0, atlas_r, 1e-5)

        ax.scatter(m_lsp, atlas_r_plot, c=colors[lt], s=20, alpha=0.7,
                   edgecolors='black', linewidths=0.3)
        ax.set_yscale('log')
        ax.set_ylim(5e-6, 5)
        ax.axhline(1.0, color='red', linestyle='--', alpha=0.5)
        ax.axhline(0.01, color='gray', linestyle=':', alpha=0.4)
        ax.set_xlabel('m(LSP) [GeV]', fontsize=12)
        ax.set_title(f'{labels[lt]} LSP ({len(subset)} models)', fontsize=13)
        if idx == 0:
            ax.set_ylabel('ATLAS r_max', fontsize=12)

    fig.suptitle('ATLAS Sensitivity vs LSP Mass', fontsize=14, y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOT_DIR, 'atlas_r_vs_mlsp.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("  atlas_r_vs_mlsp.png")


def plot_massplane_ewkino(rows):
    """m(chi1+) vs m(chi10), colored by ATLAS tier."""
    fig, ax = plt.subplots(figsize=(9, 8))

    tier_colors = {0: 'red', 1: 'orangered', 2: 'orange', 3: 'gold', 4: 'limegreen', 5: 'green'}
    tier_labels = {0: 'Invisible', 1: 'Negligible', 2: 'Weak', 3: 'Moderate', 4: 'Near-excl.', 5: 'Excluded'}

    # Plot in reverse order so invisible models are on top
    for t in [5, 4, 3, 2, 1, 0]:
        subset = [r for r in rows if r['atlas_tier'] == t]
        if not subset:
            continue
        m_lsp = [r['m_lsp'] for r in subset]
        m_chi1p = [r['m_chi1p'] for r in subset]
        ax.scatter(m_chi1p, m_lsp, c=tier_colors[t], s=25, alpha=0.8,
                   label=f'{tier_labels[t]} ({len(subset)})', edgecolors='black', linewidths=0.3,
                   zorder=5-t)

    ax.plot([0, 1500], [0, 1500], 'k--', alpha=0.3, label='m(chi1+)=m(LSP)')
    ax.plot([103, 1603], [0, 1500], 'k:', alpha=0.3)  # LEP limit

    # --- ATLAS exclusion contour overlays ---
    # Contour CSVs: col0=m_chi10, col1=m_chi1pm. Plot as x=m_chi1pm, y=m_chi10.
    # Wino-bino (SUSY-2019-09)
    cw_lsp_obs, cw_c1p_obs = load_contour(os.path.join(CONTOUR_DIR, 'susy2019_09_wino_obs.csv'))
    cw_lsp_exp, cw_c1p_exp = load_contour(os.path.join(CONTOUR_DIR, 'susy2019_09_wino_exp.csv'))
    if cw_lsp_obs is not None:
        ax.plot(cw_c1p_obs, cw_lsp_obs, color='blue', linewidth=2, zorder=10,
                label='ATLAS Wino-bino (SUSY-2019-09)')
        ax.fill(np.append(cw_c1p_obs, cw_c1p_obs[-1]), np.append(cw_lsp_obs, cw_lsp_obs[0]),
                color='blue', alpha=0.10, zorder=9)
    if cw_lsp_exp is not None:
        ax.plot(cw_c1p_exp, cw_lsp_exp, color='blue', linewidth=1.5, linestyle='--', zorder=10)

    # Higgsino (SUSY-2019-09)
    ch_lsp_obs, ch_c1p_obs = load_contour(os.path.join(CONTOUR_DIR, 'susy2019_09_higgsino_obs.csv'))
    ch_lsp_exp, ch_c1p_exp = load_contour(os.path.join(CONTOUR_DIR, 'susy2019_09_higgsino_exp.csv'))
    if ch_lsp_obs is not None:
        ax.plot(ch_c1p_obs, ch_lsp_obs, color='purple', linewidth=2, zorder=10,
                label='ATLAS Higgsino (SUSY-2019-09)')
        ax.fill(np.append(ch_c1p_obs, ch_c1p_obs[-1]), np.append(ch_lsp_obs, ch_lsp_obs[0]),
                color='purple', alpha=0.10, zorder=9)
    if ch_lsp_exp is not None:
        ax.plot(ch_c1p_exp, ch_lsp_exp, color='purple', linewidth=1.5, linestyle='--', zorder=10)

    # Disappearing track pure Wino limit (SUSY-2018-19): m(chi1+) < 660 GeV
    # Vertical line at x=660, from y=0 to y=660
    ax.plot([660, 660], [0, 660], color='darkblue', linewidth=2, linestyle='-', zorder=10,
            label='ATLAS disapp. track (SUSY-2018-19)')
    ax.fill_betweenx([0, 660], 0, 660, color='darkblue', alpha=0.06, zorder=9)

    ax.set_xlabel('m(chi1+) [GeV]', fontsize=12)
    ax.set_ylabel('m(chi10) [GeV]', fontsize=12)
    ax.set_title('EWKino Mass Plane: ATLAS Coverage', fontsize=13)
    ax.legend(fontsize=8, loc='upper left')
    ax.set_xlim(0, max(r['m_chi1p'] for r in rows) * 1.05)
    ax.set_ylim(0, max(r['m_lsp'] for r in rows) * 1.05)
    fig.savefig(os.path.join(PLOT_DIR, 'massplane_ewkino.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("  massplane_ewkino.png")


def plot_massplane_slepton(rows):
    """min(m_eL, m_eR) vs m(chi10), colored by ATLAS tier."""
    fig, ax = plt.subplots(figsize=(9, 8))

    tier_colors = {0: 'red', 1: 'orangered', 2: 'orange', 3: 'gold', 4: 'limegreen', 5: 'green'}
    tier_labels = {0: 'Invisible', 1: 'Negligible', 2: 'Weak', 3: 'Moderate', 4: 'Near-excl.', 5: 'Excluded'}

    for t in [5, 4, 3, 2, 1, 0]:
        subset = [r for r in rows if r['atlas_tier'] == t]
        if not subset:
            continue
        m_lsp = [r['m_lsp'] for r in subset]
        m_sl = [min(r['m_eL'], r['m_eR']) for r in subset]
        ax.scatter(m_sl, m_lsp, c=tier_colors[t], s=25, alpha=0.8,
                   label=f'{tier_labels[t]} ({len(subset)})', edgecolors='black', linewidths=0.3,
                   zorder=5-t)

    ax.plot([0, 2000], [0, 2000], 'k--', alpha=0.3, label='m(slepton)=m(LSP)')

    # --- ATLAS exclusion contour overlay (SUSY-2018-32) ---
    # CSV: col0=m_chi10, col1=m_slepton. Plot as x=m_slepton, y=m_chi10.
    cs_lsp_obs, cs_sl_obs = load_contour(os.path.join(CONTOUR_DIR, 'susy2018_32_slepton_obs.csv'))
    cs_lsp_exp, cs_sl_exp = load_contour(os.path.join(CONTOUR_DIR, 'susy2018_32_slepton_exp.csv'))
    if cs_lsp_obs is not None:
        ax.plot(cs_sl_obs, cs_lsp_obs, color='magenta', linewidth=2, zorder=10,
                label='ATLAS sleptons (SUSY-2018-32)')
        ax.fill(np.append(cs_sl_obs, cs_sl_obs[-1]), np.append(cs_lsp_obs, cs_lsp_obs[0]),
                color='magenta', alpha=0.12, zorder=9)
    if cs_lsp_exp is not None:
        ax.plot(cs_sl_exp, cs_lsp_exp, color='magenta', linewidth=1.5, linestyle='--', zorder=10)

    ax.set_xlabel('min(m_eL, m_eR) [GeV]', fontsize=12)
    ax.set_ylabel('m(chi10) [GeV]', fontsize=12)
    ax.set_title('Slepton Mass Plane: ATLAS Coverage', fontsize=13)
    ax.legend(fontsize=8, loc='upper left')
    ax.set_xlim(0, 2100)
    ax.set_ylim(0, 1000)
    fig.savefig(os.path.join(PLOT_DIR, 'massplane_slepton.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("  massplane_slepton.png")


def plot_massplane_stop(rows):
    """m(stop1) vs m(chi10), colored by ATLAS tier."""
    fig, ax = plt.subplots(figsize=(9, 8))

    tier_colors = {0: 'red', 1: 'orangered', 2: 'orange', 3: 'gold', 4: 'limegreen', 5: 'green'}
    tier_labels = {0: 'Invisible', 1: 'Negligible', 2: 'Weak', 3: 'Moderate', 4: 'Near-excl.', 5: 'Excluded'}

    for t in [5, 4, 3, 2, 1, 0]:
        subset = [r for r in rows if r['atlas_tier'] == t]
        if not subset:
            continue
        m_lsp = [r['m_lsp'] for r in subset]
        m_t1 = [r['m_t1'] for r in subset]
        ax.scatter(m_t1, m_lsp, c=tier_colors[t], s=25, alpha=0.8,
                   label=f'{tier_labels[t]} ({len(subset)})', edgecolors='black', linewidths=0.3,
                   zorder=5-t)

    ax.plot([0, 3000], [0, 3000], 'k--', alpha=0.3, label='m(stop)=m(LSP)')
    ax.plot([173.3, 3173.3], [0, 3000], 'k:', alpha=0.3)  # m_stop = m_LSP + m_top

    # --- ATLAS exclusion contour overlay (stop all-hadronic) ---
    # CSV: col0=m_chi10, col1=m_stop. Plot as x=m_stop, y=m_chi10.
    ct_lsp_obs, ct_st_obs = load_contour(os.path.join(CONTOUR_DIR, 'stop_hadronic_obs.csv'))
    ct_lsp_exp, ct_st_exp = load_contour(os.path.join(CONTOUR_DIR, 'stop_hadronic_exp.csv'))
    if ct_lsp_obs is not None:
        ax.plot(ct_st_obs, ct_lsp_obs, color='cyan', linewidth=2, zorder=10,
                label='ATLAS stop (all-had.)')
        ax.fill(np.append(ct_st_obs, ct_st_obs[-1]), np.append(ct_lsp_obs, ct_lsp_obs[0]),
                color='cyan', alpha=0.12, zorder=9)
    if ct_lsp_exp is not None:
        ax.plot(ct_st_exp, ct_lsp_exp, color='cyan', linewidth=1.5, linestyle='--', zorder=10)

    ax.set_xlabel('m(stop1) [GeV]', fontsize=12)
    ax.set_ylabel('m(chi10) [GeV]', fontsize=12)
    ax.set_title('Stop Mass Plane: ATLAS Coverage', fontsize=13)
    ax.legend(fontsize=8, loc='upper left')
    fig.savefig(os.path.join(PLOT_DIR, 'massplane_stop.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("  massplane_stop.png")


def plot_missing_topo_bar(rows):
    """Bar chart of most common missing topology SMS strings."""
    prompt_counter = Counter()
    displaced_counter = Counter()

    for r in rows:
        if r['top_missing_sms']:
            prompt_counter[r['top_missing_sms']] += 1

    # Also count from categories data — use the full CSV which has top missing SMS
    # For a fuller picture, we need the raw data. Use what we have.
    fig, ax = plt.subplots(figsize=(12, 7))
    top_sms = prompt_counter.most_common(15)
    if top_sms:
        sms_labels = [s[0].replace('PV > ', '') for s in top_sms]
        sms_counts = [s[1] for s in top_sms]
        bars = ax.barh(range(len(sms_labels)), sms_counts, color='steelblue', edgecolor='black')
        ax.set_yticks(range(len(sms_labels)))
        ax.set_yticklabels(sms_labels, fontsize=9)
        ax.set_xlabel('Number of models (as top missing topology)', fontsize=12)
        ax.set_title('Most Common Missing Topologies (Prompt)', fontsize=13)
        for bar, count in zip(bars, sms_counts):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                    str(count), va='center', fontsize=9)
        ax.invert_yaxis()

    fig.tight_layout()
    fig.savefig(os.path.join(PLOT_DIR, 'missing_topologies_bar.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("  missing_topologies_bar.png")


def plot_coverage_heatmap(rows):
    """Heatmap: coverage tier vs physics category."""
    all_cats = set()
    for r in rows:
        all_cats.update(r['categories'])
    all_cats = sorted(all_cats)
    tier_labels = ['Invisible', 'Negligible', 'Weak', 'Moderate', 'Near-excl.', 'Excluded']

    matrix = np.zeros((len(all_cats), 6))
    for r in rows:
        t = r['atlas_tier']
        for cat in r['categories']:
            ci = all_cats.index(cat)
            matrix[ci, t] += 1

    fig, ax = plt.subplots(figsize=(10, max(6, len(all_cats)*0.6)))
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    ax.set_xticks(range(6))
    ax.set_xticklabels(tier_labels, fontsize=10, rotation=30, ha='right')
    ax.set_yticks(range(len(all_cats)))
    ax.set_yticklabels(all_cats, fontsize=10)

    # Annotate cells
    for i in range(len(all_cats)):
        for j in range(6):
            val = int(matrix[i, j])
            if val > 0:
                color = 'white' if val > matrix.max() * 0.6 else 'black'
                ax.text(j, i, str(val), ha='center', va='center', fontsize=9, color=color)

    ax.set_title('ATLAS Coverage Tier by Physics Category', fontsize=13)
    fig.colorbar(im, ax=ax, label='Number of models')
    fig.tight_layout()
    fig.savefig(os.path.join(PLOT_DIR, 'coverage_heatmap.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("  coverage_heatmap.png")


def plot_displaced_xsec_dist(rows):
    """Distribution of displaced missing cross-section."""
    displaced = [r['total_missing_displaced_fb'] for r in rows if r['total_missing_displaced_fb'] > 0]

    if not displaced:
        print("  (no displaced cross-sections to plot)")
        return

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.hist(displaced, bins=50, color='darkorange', edgecolor='black', alpha=0.8)
    ax.set_xlabel('Missing displaced cross-section [fb]', fontsize=12)
    ax.set_ylabel('Number of models', fontsize=12)
    ax.set_title(f'Uncovered Displaced Signal ({len(displaced)} models with displaced xsec > 0)', fontsize=13)
    ax.set_yscale('log')
    fig.tight_layout()
    fig.savefig(os.path.join(PLOT_DIR, 'displaced_xsec_dist.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("  displaced_xsec_dist.png")


def write_blindspot_report(rows):
    """Write BLINDSPOT_REPORT.md with detailed gap characterization."""
    report_path = os.path.join(RESULTS_DIR, 'BLINDSPOT_REPORT.md')

    # Identify models in each gap
    gap_a = [r for r in rows if r['lsp_type'] == 2 and r['atlas_tier'] == 0]
    gap_b = [r for r in rows if r['lsp_type'] == 3 and r['atlas_tier'] <= 1]
    gap_c = [r for r in rows if min(r['m_eL'], r['m_eR']) < 600 and r['atlas_tier'] <= 2]
    gap_d = [r for r in rows if r['m_t1'] - r['m_lsp'] < 200 and r['total_missing_displaced_fb'] > 1.0]
    gap_e = [r for r in rows if r['atlas_tier'] <= 1 and r['total_missing_prompt_fb'] > 0.5]

    with open(report_path, 'w') as f:
        f.write("# ATLAS Blind Spot Characterization Report\n\n")
        f.write("**Date:** 2026-03-03\n\n")

        n_total = len(rows)
        n_inv = sum(1 for r in rows if r['atlas_tier'] == 0)
        n_neg = sum(1 for r in rows if r['atlas_tier'] == 1)
        f.write("## Executive Summary\n\n")
        f.write(f"Of {n_total} surviving pMSSM models, **{n_inv} ({100*n_inv/n_total:.1f}%)** are completely ")
        f.write(f"invisible to ATLAS and **{n_neg}** have only negligible ATLAS sensitivity (r < 0.01). ")
        f.write(f"We identify five specific gaps in the ATLAS search program:\n\n")

        # Gap A
        f.write("---\n\n## Gap A: Compressed Wino (dm ~ 0.2 GeV)\n\n")
        f.write(f"**{len(gap_a)} models** with Wino LSP and zero ATLAS sensitivity.\n\n")
        if gap_a:
            dm_vals = [r['m_chi1p'] - r['m_lsp'] for r in gap_a]
            disp_vals = [r['total_missing_displaced_fb'] for r in gap_a]
            f.write(f"- Mass splitting: {min(dm_vals):.2f} - {max(dm_vals):.2f} GeV\n")
            f.write(f"- m(LSP) range: {min(r['m_lsp'] for r in gap_a):.0f} - {max(r['m_lsp'] for r in gap_a):.0f} GeV\n")
            f.write(f"- Displaced missing xsec: {min(disp_vals):.1f} - {max(disp_vals):.1f} fb\n")
            f.write(f"- Signal: Wino pair production -> chi1+ with ctau ~ 5-20 cm -> displaced pion + MET\n")
            f.write(f"- Why ATLAS misses it: disappearing-track searches not in SModelS topology set\n")
            f.write(f"- Relevant ATLAS analysis: ATLAS-SUSY-2018-19 (disappearing tracks)\n\n")

            f.write("### Example models (top 5 by displaced xsec):\n\n")
            f.write("| scan_dir | model_id | m(LSP) | m(chi1+) | dm | displaced xsec [fb] | prompt xsec [fb] |\n")
            f.write("|----------|----------|--------|----------|----|---------------------|------------------|\n")
            for r in sorted(gap_a, key=lambda x: -x['total_missing_displaced_fb'])[:5]:
                dm = r['m_chi1p'] - r['m_lsp']
                f.write(f"| {r['scan_dir']} | {r['model_id']} | {r['m_lsp']:.0f} | {r['m_chi1p']:.0f} | {dm:.2f} | {r['total_missing_displaced_fb']:.1f} | {r['total_missing_prompt_fb']:.1f} |\n")

        # Gap B
        f.write("\n---\n\n## Gap B: Compressed Higgsino (dm ~ 1-20 GeV)\n\n")
        f.write(f"**{len(gap_b)} models** with Higgsino LSP and ATLAS tier <= Negligible.\n\n")
        if gap_b:
            dm_vals = [r['m_chi1p'] - r['m_lsp'] for r in gap_b]
            f.write(f"- Mass splitting: {min(dm_vals):.1f} - {max(dm_vals):.1f} GeV\n")
            f.write(f"- m(LSP) range: {min(r['m_lsp'] for r in gap_b):.0f} - {max(r['m_lsp'] for r in gap_b):.0f} GeV\n")
            f.write(f"- Signal: chi20 chi1+ -> chi10 + soft Z*/W* -> soft dileptons + MET\n")
            f.write(f"- Why ATLAS misses it: soft lepton pT below trigger/reconstruction thresholds\n")
            f.write(f"- Relevant analyses: ATLAS-SUSY-2019-09, ATLAS-SUSY-2021-01\n\n")

            f.write("### Example models:\n\n")
            f.write("| scan_dir | model_id | m(LSP) | m(chi1+) | dm | CMS r_max |\n")
            f.write("|----------|----------|--------|----------|----|----------|\n")
            for r in sorted(gap_b, key=lambda x: x['m_chi1p'] - x['m_lsp'])[:5]:
                dm = r['m_chi1p'] - r['m_lsp']
                f.write(f"| {r['scan_dir']} | {r['model_id']} | {r['m_lsp']:.0f} | {r['m_chi1p']:.0f} | {dm:.1f} | {r['cms_r_max']:.4f} |\n")

        # Gap C
        f.write("\n---\n\n## Gap C: Light Sleptons 180-600 GeV\n\n")
        f.write(f"**{len(gap_c)} models** with sleptons < 600 GeV and ATLAS tier <= Weak.\n\n")
        if gap_c:
            sl_vals = [min(r['m_eL'], r['m_eR']) for r in gap_c]
            f.write(f"- Slepton mass range: {min(sl_vals):.0f} - {max(sl_vals):.0f} GeV\n")
            f.write(f"- LSP types: Bino={sum(1 for r in gap_c if r['lsp_type']==1)}, ")
            f.write(f"Wino={sum(1 for r in gap_c if r['lsp_type']==2)}, ")
            f.write(f"Higgsino={sum(1 for r in gap_c if r['lsp_type']==3)}\n")
            f.write(f"- Signal: slepton pair -> dilepton + MET (clean, low background)\n")
            f.write(f"- Why ATLAS misses it: no ATLAS slepton topology in SModelS v3.1.1\n")
            f.write(f"- ATLAS reach: ~180 GeV (ATLAS-SUSY-2018-32)\n\n")

        # Gap D
        f.write("\n---\n\n## Gap D: Compressed Stop with Displaced Chargino\n\n")
        f.write(f"**{len(gap_d)} models** with compressed stop and > 1 fb displaced missing xsec.\n\n")
        if gap_d:
            f.write(f"- dm(stop,LSP) range: {min(r['m_t1']-r['m_lsp'] for r in gap_d):.0f} - {max(r['m_t1']-r['m_lsp'] for r in gap_d):.0f} GeV\n")
            disp = [r['total_missing_displaced_fb'] for r in gap_d]
            f.write(f"- Displaced missing xsec: {min(disp):.1f} - {max(disp):.1f} fb\n")
            f.write(f"- Signal: stop pair -> b + chi1+ (displaced) -> b + soft-pion + chi10\n\n")

            f.write("### Example models (top 5 by displaced xsec):\n\n")
            f.write("| scan_dir | model_id | m(stop) | m(LSP) | dm | displaced [fb] | ATLAS r_max |\n")
            f.write("|----------|----------|---------|--------|----|----------------|-------------|\n")
            for r in sorted(gap_d, key=lambda x: -x['total_missing_displaced_fb'])[:5]:
                dm = r['m_t1'] - r['m_lsp']
                f.write(f"| {r['scan_dir']} | {r['model_id']} | {r['m_t1']:.0f} | {r['m_lsp']:.0f} | {dm:.0f} | {r['total_missing_displaced_fb']:.1f} | {r['atlas_r_max']:.4f} |\n")

        # Gap E
        f.write("\n---\n\n## Gap E: Complex EWKino Cascade Topologies\n\n")
        f.write(f"**{len(gap_e)} models** with ATLAS tier <= Negligible and > 0.5 fb prompt missing xsec.\n\n")
        if gap_e:
            f.write(f"- These represent multi-body final states from chargino/neutralino cascades\n")
            f.write(f"- No ATLAS simplified model covers these topologies\n\n")
            # Count common missing SMS strings
            sms_counter = Counter()
            for r in gap_e:
                if r['top_missing_sms']:
                    sms_counter[r['top_missing_sms']] += 1
            if sms_counter:
                f.write("### Most common missing topologies in these models:\n\n")
                f.write("| SMS | Count |\n|-----|-------|\n")
                for sms, cnt in sms_counter.most_common(10):
                    f.write(f"| `{sms}` | {cnt} |\n")

        f.write("\n---\n\n## Summary Table\n\n")
        f.write("| Gap | Description | Models | Key signal | Max missing xsec [fb] |\n")
        f.write("|-----|-------------|--------|------------|----------------------|\n")
        for gap_label, gap_desc, gap_models, signal in [
            ('A', 'Compressed Wino', gap_a, 'Displaced pion + MET'),
            ('B', 'Compressed Higgsino', gap_b, 'Soft dileptons + MET'),
            ('C', 'Light sleptons', gap_c, 'Dilepton + MET'),
            ('D', 'Compressed stop + displaced', gap_d, 'b + displaced pion + MET'),
            ('E', 'Complex EWKino cascades', gap_e, 'Multi-body finals'),
        ]:
            max_xsec = max((r['total_missing_xsec_fb'] for r in gap_models), default=0)
            f.write(f"| {gap_label} | {gap_desc} | {len(gap_models)} | {signal} | {max_xsec:.1f} |\n")

    print(f"\n  BLINDSPOT_REPORT.md written")


def main():
    print("=" * 70)
    print("ATLAS BLIND SPOT CHARACTERIZATION")
    print("=" * 70)

    rows = load_coverage_csv()
    print(f"Loaded {len(rows)} models from CSV\n")

    print("Generating plots:")
    plot_atlas_vs_cms(rows)
    plot_atlas_r_vs_mlsp(rows)
    plot_massplane_ewkino(rows)
    plot_massplane_slepton(rows)
    plot_massplane_stop(rows)
    plot_missing_topo_bar(rows)
    plot_coverage_heatmap(rows)
    plot_displaced_xsec_dist(rows)

    write_blindspot_report(rows)

    print(f"\nAll plots saved to {PLOT_DIR}/")
    print("Done.")


if __name__ == '__main__':
    main()
