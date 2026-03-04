#!/usr/bin/env python
"""ATLAS-specific gap analysis on all surviving pMSSM models.

Parses raw SModelS output for each passing model to extract:
- Per-analysis r-values (ATLAS vs CMS)
- Missing topology SMS strings and cross-sections (prompt + displaced)
- Topologies outside the grid
- ATLAS coverage tier classification

Outputs:
  results/atlas_coverage/model_atlas_coverage.csv
  results/atlas_coverage/ATLAS_COVERAGE_REPORT.md
"""

import os
import sys
import csv
import glob
import numpy as np
import awkward as ak
from collections import Counter, defaultdict

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results', 'atlas_coverage')
os.makedirs(RESULTS_DIR, exist_ok=True)

sys.path.insert(0, os.path.dirname(__file__))
from final_classification import REQUIRED_FIELDS, apply_all_cuts, classify_model
from extract_benchmarks import load_ntuples_with_provenance


def parse_smodels_file(filepath):
    """Parse a SModelS .slha.py output file using exec().

    Returns dict with keys:
      expt_results: list of dicts (AnalysisID, TxNames, r, r_expected, ...)
      missing_topos: list of (SMS, weight_fb)
      missing_prompt: list of (SMS, weight_fb)
      missing_displaced: list of (SMS, weight_fb)
      outside_grid: list of (SMS, weight_fb)
      total_missing_xsec: float
      total_missing_prompt_xsec: float
      total_missing_displaced_xsec: float
      total_outside_grid_xsec: float
    """
    if not os.path.isfile(filepath):
        return None

    smodels_dict = {}
    try:
        with open(filepath, 'r') as f:
            exec(f.read(), smodels_dict)
    except Exception:
        return None

    output = smodels_dict.get('smodelsOutput')
    if output is None:
        return None

    result = {
        'expt_results': [],
        'missing_topos': [],
        'missing_prompt': [],
        'missing_displaced': [],
        'outside_grid': [],
        'total_missing_xsec': output.get('Total xsec for missing topologies (fb)', 0.0),
        'total_missing_prompt_xsec': output.get('Total xsec for missing topologies with prompt decays (fb)', 0.0),
        'total_missing_displaced_xsec': output.get('Total xsec for missing topologies with displaced decays (fb)', 0.0),
        'total_outside_grid_xsec': output.get('Total xsec for topologies outside the grid (fb)', 0.0),
    }

    for res in output.get('ExptRes', []):
        result['expt_results'].append({
            'AnalysisID': res.get('AnalysisID', ''),
            'TxNames': res.get('TxNames', []),
            'FinalStates': res.get('FinalStates', []),
            'theory_prediction_fb': res.get('theory prediction (fb)', 0.0),
            'upper_limit_fb': res.get('upper limit (fb)', 0.0),
            'expected_upper_limit_fb': res.get('expected upper limit (fb)', 0.0),
            'r': res.get('r', 0.0),
            'r_expected': res.get('r_expected', 0.0),
            'dataType': res.get('dataType', ''),
        })

    for topo in output.get('missing topologies', []):
        result['missing_topos'].append((topo.get('SMS', ''), topo.get('weight (fb)', 0.0)))

    for topo in output.get('missing topologies with prompt decays', []):
        result['missing_prompt'].append((topo.get('SMS', ''), topo.get('weight (fb)', 0.0)))

    for topo in output.get('missing topologies with displaced decays', []):
        result['missing_displaced'].append((topo.get('SMS', ''), topo.get('weight (fb)', 0.0)))

    for topo in output.get('topologies outside the grid', []):
        result['outside_grid'].append((topo.get('SMS', ''), topo.get('weight (fb)', 0.0)))

    return result


def classify_atlas_tier(atlas_r_max):
    """Classify ATLAS coverage tier based on maximum ATLAS r-value.

    Tiers:
      0 - Invisible:       no ATLAS result at all (r_max = 0)
      1 - Negligible:      r_max < 0.01
      2 - Weak:            0.01 <= r_max < 0.1
      3 - Moderate:        0.1 <= r_max < 0.5
      4 - Near-exclusion:  0.5 <= r_max < 1.0
      5 - Excluded:        r_max >= 1.0
    """
    if atlas_r_max == 0.0:
        return 0, 'Invisible'
    elif atlas_r_max < 0.01:
        return 1, 'Negligible'
    elif atlas_r_max < 0.1:
        return 2, 'Weak'
    elif atlas_r_max < 0.5:
        return 3, 'Moderate'
    elif atlas_r_max < 1.0:
        return 4, 'Near-exclusion'
    else:
        return 5, 'Excluded'


def main():
    print("=" * 70)
    print("ATLAS COVERAGE ANALYSIS")
    print("=" * 70)

    # Load and filter models
    data, provenance = load_ntuples_with_provenance()
    mask = apply_all_cuts(data)
    passing = data[mask]
    passing_mask = ak.to_numpy(mask)
    passing_provenance = [p for p, m in zip(provenance, passing_mask) if m]

    n_pass = len(passing)
    print(f"\n{n_pass} models pass all cuts")

    # Classify each model and extract SModelS details
    rows = []
    tier_counts = Counter()
    tier_by_lsp = defaultdict(Counter)
    tier_by_category = defaultdict(Counter)
    atlas_analyses_seen = Counter()
    cms_analyses_seen = Counter()
    all_missing_prompt_sms = Counter()
    all_missing_displaced_sms = Counter()
    all_outside_grid_sms = Counter()
    atlas_txnames_seen = Counter()

    n_parsed = 0
    n_missing_file = 0

    for i in range(n_pass):
        p = passing[i]
        scan_dir, model_id = passing_provenance[i]
        categories = classify_model(p)

        lsp_type = int(p['SP_LSP_type'])
        lsp_names = {1: 'Bino', 2: 'Wino', 3: 'Higgsino'}
        lsp_name = lsp_names.get(lsp_type, 'Unknown')
        m_lsp = abs(float(p['SP_m_chi_10']))
        m_chi1p = abs(float(p['SP_m_chi_1p']))
        m_chi20 = abs(float(p['SP_m_chi_20']))
        m_t1 = abs(float(p['SP_m_t_1']))
        m_b1 = abs(float(p['SP_m_b_1']))
        m_eL = abs(float(p['SP_m_e_L']))
        m_eR = abs(float(p['SP_m_e_R']))

        # Compute ntuple-based SModelS r
        sm_tp = float(p['SModelS_bestExpUL_TheoryPrediction'])
        sm_ul = float(p['SModelS_bestExpUL_UpperLimit'])
        ntuple_r = sm_tp / sm_ul if sm_tp > 0 and sm_ul > 0 else 0.0

        # Parse raw SModelS output
        smodels_path = os.path.join(scan_dir, 'SModelS', f'{model_id}.slha.py')
        sm = parse_smodels_file(smodels_path)

        atlas_r_max = 0.0
        cms_r_max = 0.0
        atlas_best_analysis = ''
        cms_best_analysis = ''
        atlas_txnames = []
        cms_txnames = []
        n_atlas_results = 0
        n_cms_results = 0

        if sm is not None:
            n_parsed += 1
            for res in sm['expt_results']:
                aid = res['AnalysisID']
                r_val = res['r'] if res['r'] is not None else 0.0
                txn = res['TxNames']

                if 'ATLAS' in aid.upper():
                    n_atlas_results += 1
                    atlas_analyses_seen[aid] += 1
                    for tx in txn:
                        atlas_txnames_seen[tx] += 1
                    if r_val > atlas_r_max:
                        atlas_r_max = r_val
                        atlas_best_analysis = aid
                        atlas_txnames = txn
                elif 'CMS' in aid.upper():
                    n_cms_results += 1
                    cms_analyses_seen[aid] += 1
                    if r_val > cms_r_max:
                        cms_r_max = r_val
                        cms_best_analysis = aid
                        cms_txnames = txn

            # Accumulate missing topology SMS strings
            for sms, wt in sm['missing_prompt']:
                all_missing_prompt_sms[sms] += 1
            for sms, wt in sm['missing_displaced']:
                all_missing_displaced_sms[sms] += 1
            for sms, wt in sm['outside_grid']:
                all_outside_grid_sms[sms] += 1

            total_missing = sm['total_missing_xsec']
            total_prompt = sm['total_missing_prompt_xsec']
            total_displaced = sm['total_missing_displaced_xsec']
            total_outside = sm['total_outside_grid_xsec']
            top_missing_sms = sm['missing_topos'][0][0] if sm['missing_topos'] else ''
            top_missing_xsec = sm['missing_topos'][0][1] if sm['missing_topos'] else 0.0
        else:
            n_missing_file += 1
            total_missing = 0.0
            total_prompt = 0.0
            total_displaced = 0.0
            total_outside = 0.0
            top_missing_sms = ''
            top_missing_xsec = 0.0

        tier_num, tier_label = classify_atlas_tier(atlas_r_max)
        tier_counts[tier_num] += 1
        tier_by_lsp[lsp_name][tier_num] += 1
        for cat in categories:
            tier_by_category[cat][tier_num] += 1

        rows.append({
            'scan_dir': os.path.basename(scan_dir),
            'model_id': model_id,
            'lsp_type': lsp_type,
            'lsp_name': lsp_name,
            'm_lsp': f'{m_lsp:.1f}',
            'm_chi1p': f'{m_chi1p:.1f}',
            'm_chi20': f'{m_chi20:.1f}',
            'm_t1': f'{m_t1:.1f}',
            'm_b1': f'{m_b1:.1f}',
            'm_eL': f'{m_eL:.1f}',
            'm_eR': f'{m_eR:.1f}',
            'categories': ';'.join(categories),
            'ntuple_r': f'{ntuple_r:.6f}',
            'atlas_r_max': f'{atlas_r_max:.6f}',
            'atlas_best_analysis': atlas_best_analysis,
            'atlas_txnames': ';'.join(atlas_txnames),
            'n_atlas_results': n_atlas_results,
            'cms_r_max': f'{cms_r_max:.6f}',
            'cms_best_analysis': cms_best_analysis,
            'cms_txnames': ';'.join(cms_txnames),
            'n_cms_results': n_cms_results,
            'atlas_tier': tier_num,
            'atlas_tier_label': tier_label,
            'total_missing_xsec_fb': f'{total_missing:.4f}',
            'total_missing_prompt_fb': f'{total_prompt:.4f}',
            'total_missing_displaced_fb': f'{total_displaced:.4f}',
            'total_outside_grid_fb': f'{total_outside:.4f}',
            'top_missing_sms': top_missing_sms,
            'top_missing_xsec_fb': f'{top_missing_xsec:.4f}',
        })

    # Write CSV
    csv_path = os.path.join(RESULTS_DIR, 'model_atlas_coverage.csv')
    fieldnames = list(rows[0].keys())
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nCSV written: {csv_path} ({len(rows)} rows)")

    # Print summary
    tier_labels = {0: 'Invisible', 1: 'Negligible', 2: 'Weak',
                   3: 'Moderate', 4: 'Near-exclusion', 5: 'Excluded'}
    print(f"\nSModelS files parsed: {n_parsed}/{n_pass} (missing: {n_missing_file})")

    print(f"\n{'='*60}")
    print("ATLAS Coverage Tier Distribution")
    print(f"{'='*60}")
    for t in range(6):
        n = tier_counts.get(t, 0)
        pct = 100 * n / n_pass if n_pass > 0 else 0
        print(f"  Tier {t} ({tier_labels[t]:15s}): {n:4d} ({pct:5.1f}%)")

    print(f"\nBy LSP type:")
    for lsp_name in ['Bino', 'Wino', 'Higgsino']:
        counts = tier_by_lsp.get(lsp_name, {})
        total = sum(counts.values())
        parts = []
        for t in range(6):
            n = counts.get(t, 0)
            if n > 0:
                parts.append(f"T{t}:{n}")
        print(f"  {lsp_name:10s} ({total:3d}): {', '.join(parts)}")

    print(f"\nATLAS analyses providing constraints:")
    for aid, cnt in atlas_analyses_seen.most_common(20):
        print(f"  {aid}: {cnt} models")

    print(f"\nCMS analyses providing constraints:")
    for aid, cnt in cms_analyses_seen.most_common(20):
        print(f"  {aid}: {cnt} models")

    print(f"\nATLAS TxNames matched:")
    for txn, cnt in atlas_txnames_seen.most_common(20):
        print(f"  {txn}: {cnt} models")

    print(f"\nTop 15 missing prompt topology SMS strings (across all models):")
    for sms, cnt in all_missing_prompt_sms.most_common(15):
        print(f"  {sms}: appears in {cnt} models")

    print(f"\nTop 15 missing displaced topology SMS strings:")
    for sms, cnt in all_missing_displaced_sms.most_common(15):
        print(f"  {sms}: appears in {cnt} models")

    # Write markdown report
    write_coverage_report(
        n_pass, n_parsed, n_missing_file,
        tier_counts, tier_labels, tier_by_lsp, tier_by_category,
        atlas_analyses_seen, cms_analyses_seen, atlas_txnames_seen,
        all_missing_prompt_sms, all_missing_displaced_sms, all_outside_grid_sms,
        rows,
    )


def write_coverage_report(
    n_pass, n_parsed, n_missing_file,
    tier_counts, tier_labels, tier_by_lsp, tier_by_category,
    atlas_analyses_seen, cms_analyses_seen, atlas_txnames_seen,
    all_missing_prompt_sms, all_missing_displaced_sms, all_outside_grid_sms,
    rows,
):
    """Write ATLAS_COVERAGE_REPORT.md"""
    report_path = os.path.join(RESULTS_DIR, 'ATLAS_COVERAGE_REPORT.md')

    # Compute statistics from rows
    atlas_r_vals = [float(r['atlas_r_max']) for r in rows]
    cms_r_vals = [float(r['cms_r_max']) for r in rows]
    displaced_vals = [float(r['total_missing_displaced_fb']) for r in rows]
    prompt_vals = [float(r['total_missing_prompt_fb']) for r in rows]

    n_atlas_zero = sum(1 for v in atlas_r_vals if v == 0.0)
    n_cms_zero = sum(1 for v in cms_r_vals if v == 0.0)
    n_both_zero = sum(1 for a, c in zip(atlas_r_vals, cms_r_vals) if a == 0.0 and c == 0.0)
    max_displaced = max(displaced_vals) if displaced_vals else 0
    max_prompt = max(prompt_vals) if prompt_vals else 0

    with open(report_path, 'w') as f:
        f.write("# ATLAS Coverage Analysis Report\n\n")
        f.write(f"**Date:** 2026-03-03\n")
        f.write(f"**Models analyzed:** {n_pass}\n")
        f.write(f"**SModelS files parsed:** {n_parsed} (missing: {n_missing_file})\n\n")

        f.write("## Summary\n\n")
        f.write(f"Of {n_pass} pMSSM models surviving all experimental constraints:\n\n")
        f.write(f"- **{n_atlas_zero} models ({100*n_atlas_zero/n_pass:.1f}%)** have zero ATLAS sensitivity (no ATLAS analysis provides any constraint)\n")
        f.write(f"- **{n_cms_zero} models ({100*n_cms_zero/n_pass:.1f}%)** have zero CMS sensitivity\n")
        f.write(f"- **{n_both_zero} models** have zero sensitivity from either experiment\n")
        f.write(f"- Maximum uncovered displaced cross-section: {max_displaced:.1f} fb\n")
        f.write(f"- Maximum uncovered prompt cross-section: {max_prompt:.1f} fb\n\n")

        f.write("## ATLAS Coverage Tiers\n\n")
        f.write("| Tier | Label | Count | Fraction |\n")
        f.write("|------|-------|-------|----------|\n")
        for t in range(6):
            n = tier_counts.get(t, 0)
            pct = 100 * n / n_pass if n_pass > 0 else 0
            f.write(f"| {t} | {tier_labels[t]} | {n} | {pct:.1f}% |\n")

        f.write("\n## Coverage by LSP Type\n\n")
        f.write("| LSP | Total | Invisible | Negligible | Weak | Moderate | Near-excl. | Excluded |\n")
        f.write("|-----|-------|-----------|------------|------|----------|------------|----------|\n")
        for lsp_name in ['Bino', 'Wino', 'Higgsino']:
            counts = tier_by_lsp.get(lsp_name, {})
            total = sum(counts.values())
            vals = [str(counts.get(t, 0)) for t in range(6)]
            f.write(f"| {lsp_name} | {total} | {' | '.join(vals)} |\n")

        f.write("\n## Coverage by Physics Category\n\n")
        f.write("| Category | Total | Invisible | Negligible | Weak | Moderate | Near-excl. | Excluded |\n")
        f.write("|----------|-------|-----------|------------|------|----------|------------|----------|\n")
        for cat in sorted(tier_by_category.keys()):
            counts = tier_by_category[cat]
            total = sum(counts.values())
            vals = [str(counts.get(t, 0)) for t in range(6)]
            f.write(f"| {cat} | {total} | {' | '.join(vals)} |\n")

        f.write("\n## ATLAS Analyses Providing Constraints\n\n")
        f.write("| Analysis | Models constrained |\n")
        f.write("|----------|-------------------|\n")
        for aid, cnt in atlas_analyses_seen.most_common():
            f.write(f"| {aid} | {cnt} |\n")
        if not atlas_analyses_seen:
            f.write("| (none) | 0 |\n")

        f.write("\n## CMS Analyses Providing Constraints\n\n")
        f.write("| Analysis | Models constrained |\n")
        f.write("|----------|-------------------|\n")
        for aid, cnt in cms_analyses_seen.most_common(20):
            f.write(f"| {aid} | {cnt} |\n")

        f.write("\n## ATLAS TxNames (Simplified Model Topologies)\n\n")
        f.write("| TxName | Occurrences |\n")
        f.write("|--------|-------------|\n")
        for txn, cnt in atlas_txnames_seen.most_common():
            f.write(f"| {txn} | {cnt} |\n")
        if not atlas_txnames_seen:
            f.write("| (none) | 0 |\n")

        f.write("\n## Missing Topologies (Prompt)\n\n")
        f.write("Top SMS strings not covered by any analysis, by number of models affected:\n\n")
        f.write("| SMS | Models |\n")
        f.write("|-----|--------|\n")
        for sms, cnt in all_missing_prompt_sms.most_common(20):
            f.write(f"| `{sms}` | {cnt} |\n")

        f.write("\n## Missing Topologies (Displaced)\n\n")
        f.write("| SMS | Models |\n")
        f.write("|-----|--------|\n")
        for sms, cnt in all_missing_displaced_sms.most_common(20):
            f.write(f"| `{sms}` | {cnt} |\n")
        if not all_missing_displaced_sms:
            f.write("| (none) | 0 |\n")

        f.write("\n## Topologies Outside Grid\n\n")
        f.write("| SMS | Models |\n")
        f.write("|-----|--------|\n")
        for sms, cnt in all_outside_grid_sms.most_common(20):
            f.write(f"| `{sms}` | {cnt} |\n")

    print(f"\nReport written: {report_path}")


if __name__ == '__main__':
    main()
