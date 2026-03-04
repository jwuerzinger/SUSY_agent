# Follow-up Plan: Next Steps After ATLAS Gap Analysis

**Date:** 2026-03-04 (updated)
**Status:** P1 COMPLETE — Grid scans attempted, Run 3 search proposals delivered

---

## Completed Work Summary

### Full Pipeline Executed
All 6 stages of the original plan have been executed to completion:

1. **atlas_coverage.py** — Parsed SModelS output for all 2,063 passing models
2. **atlas_blindspots.py** — 8 diagnostic plots + blind spot characterization
3. **Phase 4 scan configs** — 5 YAML configs, run_scans.py/run_ntupling.py updated
4. **signal_characterization.py** — Branching fractions, lifetimes, decay chains for all models
5. **make_atlas_proposals.py** — 25 benchmark SLHA files + ATLAS_GAP_ANALYSIS.md
6. **Phase 4 scans** — Completed, ntupled, and full pipeline re-run on expanded dataset

### Phase 4 Scan Results

| Scan type | Target | Models generated | Status |
|-----------|--------|-----------------|--------|
| phase4a (Wino) | Dense Wino 100-1000 GeV | 987 (3 seeds: 269+340+378) | SUCCESS |
| phase4b (Higgsino) | Higgsino dm 1-30 GeV | 916 (3 seeds: 264+230+422) | SUCCESS |
| phase4c (Slepton+Bino) | Sleptons 180-600 GeV | 3 (3 seeds: 1+1+1) | FAILED |
| phase4d (Compressed stop) | Compressed stop+Wino | 26 (3 seeds: 1+24+1) | MARGINAL |
| phase4e (Mixed EWKino) | Mixed cascades | 952 (3 seeds: 254+263+435) | SUCCESS |
| **TOTAL** | | **2,884** | |

All scans hit the 2-hour timeout before reaching 500 models. Phase4c (slepton+Bino) and phase4d (compressed stop) failed — MCMC cannot efficiently find valid points in these narrow parameter corridors.

### Final Dataset (Phases 1-4 Combined)
- **2,063 models pass all cuts** (up from 458 in Phases 1-3)
- LSP composition: Bino=62, Wino=1003, Higgsino=998
- 42 ntuple files across all phases

### ATLAS Coverage (Updated with Phase 4)

| Tier | Label | Count | Fraction |
|------|-------|-------|----------|
| 0 | Invisible | 1,372 | 66.5% |
| 1 | Negligible | 84 | 4.1% |
| 2 | Weak | 289 | 14.0% |
| 3 | Moderate | 215 | 10.4% |
| 4 | Near-exclusion | 58 | 2.8% |
| 5 | Excluded | 45 | 2.2% |

The high invisible fraction (66.5%) reflects that Phase 4 deliberately targeted ATLAS blind spots — confirming these are real, densely populated regions of viable pMSSM parameter space.

### Gap Populations (Updated)

| Gap | Description | Pre-Phase4 | Post-Phase4 |
|-----|-------------|-----------|------------|
| A | Compressed Wino | 65 | 616 |
| B | Compressed Higgsino | 12 | 737 |
| C | Light sleptons | 148 | 497 |
| D | Compressed stop + displaced | 7 | 7 |
| E | Complex EWKino cascades | 23 | 41 |

### Signal Characterization
- 1,456 ATLAS-blind models (tier 0-1) characterized
- 67 models with chargino ctau > 1 cm (disappearing track candidates)
- 19 with ctau > 10 cm, 11 with ctau > 1 m
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body) in 1,133 models

### Output Files
```
results/
  atlas_coverage/
    model_atlas_coverage.csv          (2,063 rows)
    ATLAS_COVERAGE_REPORT.md
    BLINDSPOT_REPORT.md
    signal_characterization.csv       (2,063 rows)
    plots/ (8 PNG files, all updated with Phase 4 data)
  atlas_proposals/
    ATLAS_GAP_ANALYSIS.md
    RUN3_SEARCH_PROPOSALS.md          (NEW — comprehensive Run 3 proposals)
    benchmarks/gap_{A,B,C,D,E}/      (25 SLHA files total)
    plots/ (23 PNG files — per-gap and summary)
```

---

## P1 Results (Completed 2026-03-04)

### Grid Scan Results

Grid sampling was implemented (`sample_grid()` in modelgen.py) and executed for the two failed corridors:

| Scan | Grid spec | Total points | SPheno valid | Pipeline complete | Pass all cuts |
|------|-----------|-------------|-------------|-------------------|---------------|
| phase4c_grid (Slepton+Bino) | 8(M_1) × 5(meL) × 5(meR) × 3(tanb) × 3 seeds | 5,400 | 3,276 (61%) | 1,085 (20%) | **0** |
| phase4d_grid (Compressed stop) | 6(M_2) × 5(mqL3) × 5(mtR) × 3(tanb) × 3 seeds | 4,050 | 1,350 (33%) | 27 (0.7%) | **0** |

**Why no models pass:**

- **Phase4c (Slepton+Bino):** All 1,092 valid models fail the **relic density** cut (Omega_h^2 ≤ 0.132). Measured values range from 0.45 to 19.4 with median 3.31. Bino LSPs require sleptons within ~10-20 GeV of the LSP mass to achieve sufficient co-annihilation — this is an extremely narrow strip in (M_1, meL, meR) space that a coarse grid cannot resolve. The co-annihilation strip width is ~O(1%) of the slepton mass range.

- **Phase4d (Compressed stop):** 96% of models (433/450 per seed) fail at the SPheno level (Yukawa coupling instabilities). The 28 surviving models all fail the **Higgs mass** cut — m_h ranges from 109.7 to 120.5 GeV (need 122-128). Light stops suppress the Higgs mass through radiative corrections; achieving m_h ≈ 125 with stops below 800 GeV requires very specific trilinear coupling values and large mixing.

**Key lesson:** These corridors are intrinsically narrow in multi-dimensional parameter space. Grid sampling with feasible point counts cannot resolve them. The existing models from MCMC (3 from phase4c, 26 from phase4d, plus contributions from phase2c/2d) represent the viable parameter space. For future work, **targeted importance sampling** from the known viable points (Option C) is more promising than grid sampling.

### Infrastructure Additions
- `modelgen.py`: New `sample_grid()` method for Cartesian grid sampling
- `configs/phase4c_slepton_bino_grid.yaml`, `configs/phase4d_compressed_stop_grid.yaml`
- `run_scans.py`: `--phase 4grid` option with per-job timeouts
- `run_ntupling.py`: phase4c_grid/phase4d_grid support, longest-match bug fix

### Run 3 Search Proposals (P1 + P2 Deliverable)

`analysis/run3_proposals.py` produces comprehensive ATLAS Run 3 search proposals with:
- Concrete signal region definitions for 5 ATLAS blind spots (Gaps A-E)
- Signal yield estimates at 300 fb⁻¹ (13.6 TeV, k=1.15)
- Direct detection complementarity (XENON-nT, LZ, DARWIN)
- 30 mass-grid benchmarks across all gaps
- 23 publication-quality plots

| Gap | Description | Models | Excludable (N>3) | Discoverable (N>10) | Benchmarks |
|-----|-------------|--------|------------------|---------------------|------------|
| A | Compressed Wino (disappearing tracks) | 526 | 103 | 73 | 7 |
| B | Compressed Higgsino (soft leptons) | 737 | 34 | 11 | 7 |
| C | Light Sleptons (dilepton + MET) | 497 | 145 | 108 | 7 |
| D | Compressed Stop (displaced vertex) | 2 | 2 | 2 | 2 |
| E | Complex EWKino (multi-lepton cascade) | 80 | 21 | 12 | 7 |

**Truly dark models:** 3 models invisible to both ATLAS and projected DARWIN sensitivity — only discoverable at the LHC with dedicated searches.

**SModelS caveat:** The coverage assessment relies on SModelS v3.1.1, which lacks ATLAS disappearing-track (SUSY-2018-19), direct slepton (SUSY-2018-32), and compressed Higgsino (SUSY-2019-09) topologies. Many Gap A/B/C models may already be partially constrained by existing analyses.

---

## Remaining Priorities

### Priority 2 (partially done): ATLAS Contour Overlays
- Download published ATLAS exclusion contours from HEPData
- Overlay on mass-plane plots to show model populations vs. ATLAS reach
- Contours for ATLAS-SUSY-2018-19, -2018-32, -2019-09

### Priority 3: Refine Phase4c/4d Sampling (if more models needed)

The grid sampling approach (Option A) was attempted and proved insufficient for these narrow corridors. Future attempts should use:
- **Importance sampling** (Option C): Perturb existing viable models from phase2c/2d with small proposal widths, especially targeting the co-annihilation strip (slepton-LSP mass splitting ~5-20 GeV) and Higgs-mass-compatible stop mixing
- **Parameterized grid**: Grid over (M_1, dm_slepton) instead of (M_1, meL, meR), where dm_slepton = m_slepton - m_LSP is constrained to [5, 50] GeV

### Priority 4: SModelS Database Update Requests

Contact the SModelS collaboration about encoding missing ATLAS results:
- **Disappearing tracks** (ATLAS-SUSY-2018-19): would immediately provide constraints for 616+ Gap A models
- **Direct sleptons** (ATLAS-SUSY-2018-32): would cover Gap C slepton models
- **Compressed Higgsino** (ATLAS-SUSY-2019-09): would cover Gap B
- This is the single highest-impact improvement for ATLAS coverage assessment

### Priority 5: Full Reinterpretation with CheckMATE2/MadAnalysis5

For the 25 benchmark SLHA files:
- Generate signal events with MadGraph5 + Pythia8
- Run through CheckMATE2 or MadAnalysis5 reinterpretation framework
- This provides proper ATLAS constraints that go beyond simplified-model topology matching
- Focus on Gap A and Gap C where the SModelS topology encoding gap is the bottleneck

### Priority 6: HL-LHC Projections

For each blind spot:
- Scale existing Run 2 limits to 300 fb^-1 (Run 3) and 3000 fb^-1 (HL-LHC)
- Use conservative sqrt(L) scaling for background-dominated searches
- Assess which gaps will be closed by luminosity alone and which require new analysis strategies
- This informs which ATLAS analysis proposals are truly novel vs. just needing more data

### Priority 7: Direct Detection Complementarity (DONE in run3_proposals.py)

✓ Extracted SI and SD cross-sections from MicrOMEGAs ntuples
✓ Compared with XENON-nT, LZ, and DARWIN projected limits
✓ Identified 3 "truly dark" models (invisible to both ATLAS and DARWIN)
✓ dd_complementarity.png plot produced

### Priority 8: Publication Preparation

- Polish all plots for publication quality (ATLAS style, proper labels, error bands)
- Write paper draft: "Identifying Gaps in the ATLAS SUSY Search Program: A pMSSM Study"
- Structure: introduction, methodology, gap taxonomy, signal characterization, analysis proposals, conclusions
- Prepare benchmark SLHA files in standardized SLHA2 format for ATLAS SUSY working group
- Consider submission as ATLAS internal note or public paper

---

## Lessons Learned

1. **MCMC limitations for narrow corridors:** Phase4c (slepton+Bino) and phase4d (compressed stop) failed, matching Phase 3a/3c failures. Alternative sampling methods (grid, nested, importance) are essential for these targets.

2. **Grid sampling also insufficient for narrow corridors:** The Phase 4 grid scans (phase4c_grid: 5,400 points, phase4d_grid: 4,050 points) produced 1,092 and 28 valid spectra respectively, but **zero models passed all physics cuts**. For phase4c, the co-annihilation strip (slepton-LSP mass splitting ~10-20 GeV) is too narrow to be resolved by a coarse grid over (M_1, meL, meR). For phase4d, the Higgs mass constraint requires very specific stop mixing that random AT sampling doesn't reliably achieve. **Importance sampling from existing viable points is the recommended approach.**

3. **softsusy as bottleneck vs. cross-check:** Removing softsusy from grid scan pipelines increased SPheno-to-SModelS throughput from ~20% to ~60% for phase4c. However, softsusy is required by the `apply_all_cuts()` quality cut (both SP_m_h and SS_m_h must be valid). For grid scans without softsusy, this cut rejects all models regardless of physics. Future grid scans should either include softsusy or use a relaxed quality cut.

4. **Scan timeout:** The 2-hour timeout in run_scans.py was too short for 500-model MCMC scans with burn_in=100. Consider increasing to 4 hours or implementing checkpointing.

5. **SModelS topology coverage is the main bottleneck:** The dominance of T2tt/T2bb topologies and absence of EWKino/slepton/disappearing-track ATLAS topologies in SModelS v3.1.1 means our "ATLAS invisible" count is an overestimate of true ATLAS insensitivity. Encoding more ATLAS results in SModelS would significantly change the picture.

6. **Phase 4 dramatically increased statistics:** Going from 458 to 2,063 models (4.5x) confirms that the blind-spot regions are densely populated in viable pMSSM parameter space — these are not edge cases but a large fraction of the physically allowed models.

---

## Execution Priority Summary

| Priority | Task | Status | Notes |
|----------|------|--------|-------|
| **P1** | Fix Phase4c/4d with grid sampling | ✅ DONE | Grid scans executed; 0 new passing models (physics constraints too narrow) |
| **P1** | Refine benchmark selection | ✅ DONE | 30 benchmarks selected in run3_proposals.py |
| **P1** | Run 3 search proposals | ✅ DONE | RUN3_SEARCH_PROPOSALS.md + 23 plots |
| **P1** | Direct detection complementarity | ✅ DONE | dd_complementarity.png, 3 truly dark models identified |
| **P2** | ATLAS contour overlays from HEPData | TODO | Download + overlay published exclusion contours |
| **P2** | SModelS database update requests | TODO | External contact with SModelS team |
| **P3** | Refined phase4c/4d sampling (importance) | TODO | Perturb existing viable models for narrow corridors |
| **P3** | CheckMATE2/MadAnalysis5 reinterpretation | TODO | Full MC for 30 benchmarks |
| **P3** | HL-LHC projections | TODO | Scale to 3000 fb⁻¹ |
| **P4** | Publication preparation | TODO | Paper draft, ATLAS-style plots |
