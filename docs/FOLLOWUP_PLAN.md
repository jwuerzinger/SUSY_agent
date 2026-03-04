# Follow-up Plan: Next Steps After ATLAS Gap Analysis

**Date:** 2026-03-03
**Status:** ALL STAGES COMPLETE (including Phase 4 scans, ntupling, and re-analysis)

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
    benchmarks/gap_{A,B,C,D,E}/      (25 SLHA files total)
```

---

## Next Steps

### Priority 1: Fix Failed Scans (Phase4c Sleptons, Phase4d Compressed Stop)

Phase4c and phase4d effectively produced no models. The MCMC sampling cannot find viable points in these narrow parameter corridors. Three approaches to try:

**Option A: Grid-based scanning**
Create a new scan mode that uses a structured grid rather than MCMC. For phase4c (slepton+Bino), the key constraint is m(Bino) < m(slepton) < ~700 GeV with all other sparticles heavy. A grid over (M_1, meL, meR) with fixed heavy M_2/mu/M_3 should directly populate this space.

**Option B: Wider MCMC with post-selection**
Loosen the MCMC constraints (e.g., remove relic density from MCMC acceptance) and apply them only at the ntuple analysis stage. This lets the chain explore more freely and post-selects the physically valid models.

**Option C: Importance sampling from Phase 2c**
Use the Phase 2c slepton scan output as a proposal distribution. The 71 passing models from Phase 2c define the viable region — generate new points by perturbing these with small proposal widths.

### Priority 2: Refine Benchmark Selection

With 2,063 models now available:
- Create a mass-grid of benchmark points for each gap (e.g., m(Wino) = 100, 200, 300, ..., 800 GeV)
- Select benchmarks that are maximally spread across the mass plane
- Include both "typical" and "extreme" benchmarks per gap
- Write a systematic benchmark table for ATLAS consumption

### Priority 3: Quantify ATLAS Reach Boundaries

Create proper exclusion contour overlays on mass-plane plots:
- Download published ATLAS exclusion contours from HEPData for:
  - ATLAS-SUSY-2018-19 (disappearing tracks) — directly relevant for Gap A
  - ATLAS-SUSY-2018-32 (direct sleptons) — directly relevant for Gap C
  - ATLAS-SUSY-2019-09 (compressed Higgsino) — directly relevant for Gap B
- Overlay on our mass-plane plots to show where pMSSM models fall relative to ATLAS reach
- Quantify the gap between the ATLAS contour boundary and our model populations

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

### Priority 7: Direct Detection Complementarity

For each ATLAS-blind model:
- Extract spin-independent (SI) and spin-dependent (SD) direct detection cross-sections from MicrOMEGAs output
- Compare with XENON-nT, LZ, and projected DARWIN sensitivities
- Identify "truly dark" models invisible to both LHC and direct detection experiments
- This provides complementary physics motivation beyond LHC searches

### Priority 8: Publication Preparation

- Polish all plots for publication quality (ATLAS style, proper labels, error bands)
- Write paper draft: "Identifying Gaps in the ATLAS SUSY Search Program: A pMSSM Study"
- Structure: introduction, methodology, gap taxonomy, signal characterization, analysis proposals, conclusions
- Prepare benchmark SLHA files in standardized SLHA2 format for ATLAS SUSY working group
- Consider submission as ATLAS internal note or public paper

---

## Lessons Learned

1. **MCMC limitations for narrow corridors:** Phase4c (slepton+Bino) and phase4d (compressed stop) failed, matching Phase 3a/3c failures. Alternative sampling methods (grid, nested, importance) are essential for these targets.

2. **Scan timeout:** The 2-hour timeout in run_scans.py was too short for 500-model MCMC scans with burn_in=100. Consider increasing to 4 hours or implementing checkpointing.

3. **SModelS topology coverage is the main bottleneck:** The dominance of T2tt/T2bb topologies and absence of EWKino/slepton/disappearing-track ATLAS topologies in SModelS v3.1.1 means our "ATLAS invisible" count is an overestimate of true ATLAS insensitivity. Encoding more ATLAS results in SModelS would significantly change the picture.

4. **Phase 4 dramatically increased statistics:** Going from 458 to 2,063 models (4.5x) confirms that the blind-spot regions are densely populated in viable pMSSM parameter space — these are not edge cases but a large fraction of the physically allowed models.

---

## Execution Priority Summary

| Priority | Task | Effort |
|----------|------|--------|
| **P1** | Fix Phase4c/4d with grid sampling | 2-4 hours |
| **P1** | Refine benchmark selection | 1-2 hours |
| **P2** | ATLAS contour overlays from HEPData | 2-3 hours |
| **P2** | SModelS database update requests | External contact |
| **P3** | CheckMATE2/MadAnalysis5 reinterpretation | 1-2 days |
| **P3** | HL-LHC projections | 1 day |
| **P4** | Direct detection complementarity | 1 day |
| **P4** | Publication preparation | 1-2 weeks |
