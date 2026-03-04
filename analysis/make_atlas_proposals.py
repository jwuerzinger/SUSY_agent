#!/usr/bin/env python
"""Generate ATLAS gap analysis proposals and extract benchmark SLHA files.

For each ATLAS blind spot (Gaps A-E):
1. Extract 3-5 benchmark SLHA files (highest xsec, closest to exclusion, most extreme spectrum)
2. Write structured analysis proposals with signal characterization
3. Produce final ATLAS_GAP_ANALYSIS.md report

Requires:
  results/atlas_coverage/model_atlas_coverage.csv
  results/atlas_coverage/signal_characterization.csv
"""

import os
import sys
import csv
import shutil
import numpy as np
from collections import Counter

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results', 'atlas_proposals')
COVERAGE_DIR = os.path.join(PROJECT_ROOT, 'results', 'atlas_coverage')
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_csv(path):
    """Load CSV into list of dicts with numeric conversion."""
    with open(path) as f:
        rows = list(csv.DictReader(f))
    float_fields = [
        'm_lsp', 'm_chi1p', 'm_chi20', 'm_t1', 'm_b1', 'm_eL', 'm_eR',
        'atlas_r_max', 'cms_r_max',
        'total_missing_xsec_fb', 'total_missing_prompt_fb',
        'total_missing_displaced_fb', 'total_outside_grid_fb',
    ]
    int_fields = ['lsp_type', 'atlas_tier', 'model_id']
    for row in rows:
        for fld in float_fields:
            if fld in row:
                try:
                    row[fld] = float(row[fld])
                except (ValueError, KeyError):
                    pass
        for fld in int_fields:
            if fld in row:
                try:
                    row[fld] = int(row[fld])
                except (ValueError, KeyError):
                    pass
    return rows


def load_signal_csv():
    """Load signal characterization CSV."""
    path = os.path.join(COVERAGE_DIR, 'signal_characterization.csv')
    if not os.path.isfile(path):
        return {}
    with open(path) as f:
        rows = list(csv.DictReader(f))
    lookup = {}
    for r in rows:
        try:
            key = (r['scan_dir'], int(r['model_id']))
        except (ValueError, KeyError):
            continue
        lookup[key] = r
    return lookup


def find_scan_dir_for_model(scan_dir_base, model_id):
    """Find the full scan directory path that contains a specific model's SLHA file."""
    import glob as globmod
    matches = globmod.glob(os.path.join(PROJECT_ROOT, f'scans/phase*/{scan_dir_base}'))
    for m in matches:
        if os.path.isfile(os.path.join(m, 'SPheno', f'{model_id}.slha')):
            return m
        if os.path.isfile(os.path.join(m, 'input', f'{model_id}.slha')):
            return m
    # Fallback: return first match
    if matches:
        return matches[0]
    return None


def extract_benchmarks_for_gap(gap_label, models, signal_lookup, max_benchmarks=5):
    """Extract benchmark SLHA files for a gap.

    Selection criteria:
    - Highest missing cross-section
    - Closest to ATLAS exclusion (highest atlas_r_max)
    - Most extreme spectrum (lightest LSP)
    """
    gap_dir = os.path.join(RESULTS_DIR, 'benchmarks', f'gap_{gap_label}')
    os.makedirs(gap_dir, exist_ok=True)

    if not models:
        return []

    # Score and rank models
    scored = []
    for r in models:
        total_xsec = r.get('total_missing_xsec_fb', 0)
        if isinstance(total_xsec, str):
            total_xsec = float(total_xsec)
        scored.append((total_xsec, r))

    # Sort by missing xsec descending
    scored.sort(key=lambda x: -x[0])

    # Take top by xsec, closest to exclusion, and lightest LSP
    selected = []
    selected_keys = set()

    # Top 2 by missing xsec
    for xsec, r in scored[:2]:
        key = (r['scan_dir'], r['model_id'])
        if key not in selected_keys:
            selected.append(('highest_xsec', r))
            selected_keys.add(key)

    # Top 1 closest to ATLAS exclusion
    by_atlas_r = sorted(models, key=lambda x: -x.get('atlas_r_max', 0))
    for r in by_atlas_r[:1]:
        key = (r['scan_dir'], r['model_id'])
        if key not in selected_keys:
            selected.append(('closest_exclusion', r))
            selected_keys.add(key)

    # Top 1 lightest LSP
    by_lsp = sorted(models, key=lambda x: x.get('m_lsp', 9999))
    for r in by_lsp[:1]:
        key = (r['scan_dir'], r['model_id'])
        if key not in selected_keys:
            selected.append(('lightest_lsp', r))
            selected_keys.add(key)

    # Fill up to max_benchmarks
    for xsec, r in scored:
        if len(selected) >= max_benchmarks:
            break
        key = (r['scan_dir'], r['model_id'])
        if key not in selected_keys:
            selected.append(('additional', r))
            selected_keys.add(key)

    # Copy SLHA files
    extracted = []
    for tag, r in selected:
        sd = find_scan_dir_for_model(r['scan_dir'], r['model_id'])
        if sd is None:
            continue
        model_id = r['model_id']
        slha_path = os.path.join(sd, 'SPheno', f'{model_id}.slha')
        if not os.path.isfile(slha_path):
            slha_path = os.path.join(sd, 'input', f'{model_id}.slha')
        if os.path.isfile(slha_path):
            out_name = f'gap{gap_label}_{tag}_{r["scan_dir"]}_m{model_id}.slha'
            out_path = os.path.join(gap_dir, out_name)
            shutil.copy2(slha_path, out_path)

            sig = signal_lookup.get((r['scan_dir'], model_id), {})
            extracted.append({
                'tag': tag,
                'model': r,
                'signal': sig,
                'slha_path': out_path,
            })

    return extracted


def write_gap_analysis_report(all_gaps, coverage_rows, signal_lookup):
    """Write the comprehensive ATLAS_GAP_ANALYSIS.md report."""
    report_path = os.path.join(RESULTS_DIR, 'ATLAS_GAP_ANALYSIS.md')

    n_total = len(coverage_rows)
    n_inv = sum(1 for r in coverage_rows if r['atlas_tier'] == 0)
    n_neg = sum(1 for r in coverage_rows if r['atlas_tier'] == 1)
    n_weak = sum(1 for r in coverage_rows if r['atlas_tier'] == 2)

    with open(report_path, 'w') as f:
        f.write("# ATLAS Gap Analysis: pMSSM Models Missing from the ATLAS Search Program\n\n")
        f.write("**Date:** 2026-03-03\n")
        f.write("**SModelS version:** 3.1.1\n")
        f.write(f"**Models analyzed:** {n_total} pMSSM models surviving all experimental constraints\n\n")

        f.write("## Executive Summary\n\n")
        f.write(f"We analyze ATLAS coverage of {n_total} pMSSM models that survive Higgs mass, ")
        f.write(f"relic density, B-physics, SModelS exclusion, and LEP constraints. ")
        f.write(f"We find:\n\n")
        f.write(f"- **{n_inv} models ({100*n_inv/n_total:.1f}%)** are completely invisible to ATLAS ")
        f.write(f"(no ATLAS analysis provides any constraint)\n")
        f.write(f"- **{n_neg} models ({100*n_neg/n_total:.1f}%)** have negligible ATLAS sensitivity (r < 0.01)\n")
        f.write(f"- **{n_weak} models ({100*n_weak/n_total:.1f}%)** have only weak ATLAS constraints (0.01 < r < 0.1)\n")
        f.write(f"- Combined: **{n_inv+n_neg+n_weak} models ({100*(n_inv+n_neg+n_weak)/n_total:.1f}%)** have ")
        f.write(f"r_ATLAS < 0.1\n\n")
        f.write("The ATLAS constraints that exist come almost exclusively from stop/sbottom simplified models ")
        f.write("(T2tt, T2bb). There are no ATLAS electroweakino, slepton, or disappearing-track topologies ")
        f.write("in the SModelS v3.1.1 database.\n\n")

        f.write("We identify five specific gaps in the ATLAS search program and provide benchmark ")
        f.write("SLHA files and concrete analysis proposals for each.\n\n")

        f.write("---\n\n")

        # Gap details
        for gap_label, gap_title, gap_desc, gap_models, benchmarks, strategy in all_gaps:
            f.write(f"## Gap {gap_label}: {gap_title}\n\n")
            f.write(f"**Models affected:** {len(gap_models)}\n\n")
            f.write(f"### Description\n\n{gap_desc}\n\n")

            # Model statistics
            if gap_models:
                lsp_counts = Counter(r.get('lsp_name', r.get('lsp_type', '?')) for r in gap_models)
                m_lsp_vals = [r['m_lsp'] for r in gap_models]
                f.write(f"### Model Statistics\n\n")
                f.write(f"- LSP types: {', '.join(f'{k}={v}' for k, v in lsp_counts.most_common())}\n")
                f.write(f"- m(LSP) range: {min(m_lsp_vals):.0f} - {max(m_lsp_vals):.0f} GeV\n")

                missing_xsec = [r['total_missing_xsec_fb'] for r in gap_models]
                f.write(f"- Missing cross-section: {min(missing_xsec):.2f} - {max(missing_xsec):.2f} fb\n")

                displaced = [r['total_missing_displaced_fb'] for r in gap_models]
                if any(d > 0 for d in displaced):
                    f.write(f"- Displaced missing xsec: up to {max(displaced):.1f} fb\n")
                f.write("\n")

            # Benchmarks
            if benchmarks:
                f.write(f"### Benchmark Models ({len(benchmarks)} extracted)\n\n")
                f.write("| Selection | scan_dir | model_id | m(LSP) | m(chi1+) | dm | Missing xsec [fb] | ATLAS r_max |\n")
                f.write("|-----------|----------|----------|--------|----------|----|-------------------|-------------|\n")
                for bm in benchmarks:
                    r = bm['model']
                    dm = r['m_chi1p'] - r['m_lsp']
                    f.write(f"| {bm['tag']} | {r['scan_dir']} | {r['model_id']} | {r['m_lsp']:.0f} | {r['m_chi1p']:.0f} | {dm:.1f} | {r['total_missing_xsec_fb']:.2f} | {r['atlas_r_max']:.4f} |\n")

                # Signal characterization for benchmarks
                f.write("\n### Signal Characterization\n\n")
                for bm in benchmarks:
                    sig = bm.get('signal', {})
                    if sig:
                        r = bm['model']
                        ctau = sig.get('ctau_chi1p_m', '-1')
                        chain = sig.get('dominant_chain', '')
                        f.write(f"**{bm['tag']}** (model {r['model_id']} from {r['scan_dir']}):\n")
                        if chain:
                            f.write(f"- Dominant decay: {chain}\n")
                        if ctau and float(ctau) > 0:
                            f.write(f"- Chargino ctau: {float(ctau)*100:.2f} cm\n")
                        f.write(f"- Expected visible pT: {sig.get('expected_vis_pt', 'N/A')}\n\n")

                f.write(f"\nBenchmark SLHA files: `results/atlas_proposals/benchmarks/gap_{gap_label}/`\n\n")

            # Analysis strategy
            f.write(f"### Proposed Analysis Strategy\n\n{strategy}\n\n")
            f.write("---\n\n")

        # Summary table
        f.write("## Summary\n\n")
        f.write("| Gap | Description | Models | Benchmarks | Key signal | Priority |\n")
        f.write("|-----|-------------|--------|------------|------------|----------|\n")
        priorities = {'A': 'HIGH', 'B': 'HIGH', 'C': 'MEDIUM', 'D': 'MEDIUM', 'E': 'LOW'}
        for gap_label, gap_title, _, gap_models, benchmarks, _ in all_gaps:
            f.write(f"| {gap_label} | {gap_title} | {len(gap_models)} | {len(benchmarks)} | ")
            f.write(f"See above | {priorities.get(gap_label, 'MEDIUM')} |\n")

        f.write("\n## Methodology\n\n")
        f.write("1. Generated 458 pMSSM models surviving Higgs mass [122-128 GeV], relic density <= 0.132, ")
        f.write("B-physics (2 sigma), SModelS exclusion, and LEP chargino mass > 103 GeV constraints\n")
        f.write("2. Parsed raw SModelS v3.1.1 output for each model to extract per-analysis r-values\n")
        f.write("3. Classified ATLAS coverage into tiers: Invisible (r=0), Negligible (r<0.01), ")
        f.write("Weak (r<0.1), Moderate (r<0.5), Near-exclusion (r<1), Excluded (r>=1)\n")
        f.write("4. Identified five specific gaps and extracted benchmark SLHA files\n")
        f.write("5. Characterized signals using SPheno branching fractions, widths, and SModelS decomposition\n\n")

        f.write("## References\n\n")
        f.write("- SModelS v3.1.1: https://smodels.github.io/\n")
        f.write("- SPheno: https://spheno.hepforge.org/\n")
        f.write("- MicrOMEGAs: https://lapth.cnrs.fr/micromegas/\n")

    print(f"Report written: {report_path}")
    return report_path


def main():
    print("=" * 70)
    print("ATLAS GAP ANALYSIS PROPOSALS")
    print("=" * 70)

    # Load data
    coverage_rows = load_csv(os.path.join(COVERAGE_DIR, 'model_atlas_coverage.csv'))
    signal_lookup = load_signal_csv()
    print(f"Loaded {len(coverage_rows)} coverage rows, {len(signal_lookup)} signal characterizations")

    # Define gaps
    gap_a_models = [r for r in coverage_rows if r['lsp_type'] == 2 and r['atlas_tier'] == 0]
    gap_b_models = [r for r in coverage_rows if r['lsp_type'] == 3 and r['atlas_tier'] <= 1]
    gap_c_models = [r for r in coverage_rows if min(r['m_eL'], r['m_eR']) < 600 and r['atlas_tier'] <= 2]
    gap_d_models = [r for r in coverage_rows if r['m_t1'] - r['m_lsp'] < 200 and r['total_missing_displaced_fb'] > 1.0]
    gap_e_models = [r for r in coverage_rows if r['atlas_tier'] <= 1 and r['total_missing_prompt_fb'] > 0.5]

    print(f"\nGap A (Compressed Wino): {len(gap_a_models)} models")
    print(f"Gap B (Compressed Higgsino): {len(gap_b_models)} models")
    print(f"Gap C (Light sleptons): {len(gap_c_models)} models")
    print(f"Gap D (Compressed stop + displaced): {len(gap_d_models)} models")
    print(f"Gap E (Complex EWKino cascades): {len(gap_e_models)} models")

    # Extract benchmarks
    print("\nExtracting benchmark SLHA files...")
    bm_a = extract_benchmarks_for_gap('A', gap_a_models, signal_lookup)
    bm_b = extract_benchmarks_for_gap('B', gap_b_models, signal_lookup)
    bm_c = extract_benchmarks_for_gap('C', gap_c_models, signal_lookup)
    bm_d = extract_benchmarks_for_gap('D', gap_d_models, signal_lookup)
    bm_e = extract_benchmarks_for_gap('E', gap_e_models, signal_lookup)

    print(f"  Gap A: {len(bm_a)} benchmarks")
    print(f"  Gap B: {len(bm_b)} benchmarks")
    print(f"  Gap C: {len(bm_c)} benchmarks")
    print(f"  Gap D: {len(bm_d)} benchmarks")
    print(f"  Gap E: {len(bm_e)} benchmarks")

    # Define gap descriptions and strategies
    all_gaps = [
        ('A', 'Compressed Wino (disappearing tracks)',
         "The Wino LSP scenario with mass splitting dm(chi1+, chi10) ~ 0.2 GeV produces "
         "charginos with macroscopic lifetimes (ctau ~ 5-20 cm). These charginos produce "
         "disappearing tracks in the inner detector before decaying to a soft pion and the "
         "invisible LSP. The SModelS v3.1.1 database does not encode ATLAS disappearing-track "
         "searches, making these models completely invisible despite large production cross-sections.",
         gap_a_models, bm_a,
         "**Extend ATLAS-SUSY-2018-19 (disappearing tracks):**\n"
         "- The existing ATLAS disappearing-track search should already cover many of these models\n"
         "- Encoding this analysis topology in SModelS would immediately provide constraints\n"
         "- Request SModelS collaboration to add ATLAS disappearing-track results\n"
         "- For Run 3: extend the search to higher chargino masses using the full 300 fb-1 dataset\n"
         "- Consider dedicated triggers for short tracks (pixel-only) to access ctau < 5 cm"),

        ('B', 'Compressed Higgsino (soft leptons)',
         "Higgsino LSP scenarios with mass splitting dm ~ 1-20 GeV produce soft dileptons + MET "
         "from chi20 -> Z* chi10 and chi1+ -> W* chi10 decays. The visible decay products "
         "have pT typically below 10 GeV, challenging standard trigger and reconstruction thresholds.",
         gap_b_models, bm_b,
         "**Extend ATLAS-SUSY-2019-09 (compressed Higgsino) and ATLAS-SUSY-2021-01:**\n"
         "- Lower lepton pT thresholds using ISR-boosted topology (monojet + soft leptons)\n"
         "- Use VBF topology as additional trigger path for compressed spectra\n"
         "- For Run 3: exploit improved low-pT reconstruction from ITk upgrade studies\n"
         "- Encode existing ATLAS compressed-Higgsino results in SModelS"),

        ('C', 'Light Sleptons above ATLAS Reach',
         "Models with sleptons in the 180-600 GeV range produce clean dilepton + MET signatures "
         "from slepton pair production. The ATLAS Run 2 reach extends to ~180 GeV for direct "
         "slepton production (ATLAS-SUSY-2018-32), but many models have sleptons well above this. "
         "No ATLAS slepton simplified model topology is encoded in SModelS v3.1.1.",
         gap_c_models, bm_c,
         "**Extend ATLAS-SUSY-2018-32 (direct slepton):**\n"
         "- With 300 fb-1 Run 3 data, extend slepton reach from ~180 GeV toward 400-500 GeV\n"
         "- Encode the existing ATLAS slepton results in SModelS for proper coverage assessment\n"
         "- Consider di-tau final states for stau scenarios\n"
         "- For Bino LSP models: the 2-body decay slepton -> l + chi10 is very clean"),

        ('D', 'Compressed Stop with Displaced Chargino',
         "Models with compressed stop spectra where stop -> b + chi1+ and the chargino has "
         "macroscopic lifetime (ctau ~ cm). These produce both displaced and prompt signatures "
         "with massive uncovered cross-sections (up to ~14,000 fb displaced). "
         "The ATLAS r_max for these models is only ~0.01, far from exclusion.",
         gap_d_models, bm_d,
         "**New search: displaced b-jets + MET:**\n"
         "- Combine b-tagging with displaced-vertex reconstruction\n"
         "- Target: stop pair -> b + displaced-track + MET\n"
         "- Also extend ATLAS-SUSY-2018-07 (stop compressed) to include displaced signatures\n"
         "- The prompt component (b + soft jet + MET) may be accessible with monojet-like searches"),

        ('E', 'Complex EWKino Cascade Topologies',
         "Models with complex neutralino/chargino cascade decays producing multi-body final states "
         "like (b,MET)+(t,nu,l,MET) or (b,l,l,MET)+(t,nu,l,MET). No ATLAS simplified model "
         "covers these topologies, which arise from mixed Bino/Wino/Higgsino spectra with "
         "multiple intermediate states.",
         gap_e_models, bm_e,
         "**Extend existing multi-lepton + jets + MET searches:**\n"
         "- ATLAS-SUSY-2018-06 (multi-lepton) should have some sensitivity\n"
         "- Create new signal regions targeting asymmetric final states (e.g., 1 b-jet + 1 lepton + MET)\n"
         "- Consider top+b+lepton+MET as a dedicated final state\n"
         "- For pMSSM interpretation: perform full pMSSM scan reinterpretation against these analyses"),
    ]

    # Write report
    write_gap_analysis_report(all_gaps, coverage_rows, signal_lookup)

    # Summary
    total_benchmarks = len(bm_a) + len(bm_b) + len(bm_c) + len(bm_d) + len(bm_e)
    print(f"\n{'='*60}")
    print(f"DELIVERABLES COMPLETE")
    print(f"{'='*60}")
    print(f"  Benchmark SLHA files: {total_benchmarks} across 5 gaps")
    print(f"  Report: results/atlas_proposals/ATLAS_GAP_ANALYSIS.md")
    print(f"  Benchmarks: results/atlas_proposals/benchmarks/gap_{{A,B,C,D,E}}/")


if __name__ == '__main__':
    main()
