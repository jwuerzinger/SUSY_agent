# pMSSM Investigation: Final Summary

## Executive Summary

This investigation systematically explored the 19-parameter phenomenological MSSM (pMSSM) to identify viable SUSY models and assess the coverage of the ATLAS search programme at the LHC. Using a five-phase scan strategy — flat exploration, targeted MCMC sampling, refinement scans, ATLAS blind spot targeting, and importance sampling — we evaluated **26,048 parameter points** through a full physics pipeline (SPheno, Softsusy, micrOMEGAs, SuperISO, GM2Calc, FeynHiggs, SModelS) and applied all current experimental constraints.

**Key results:**

- **2,087 pMSSM models survive all constraints**, covering 9 distinct physics categories
- **69.7% of surviving models (1,456) are invisible to ATLAS** in SModelS v3.1.1 reinterpretation
- **Five specific ATLAS blind spots** identified with Run 3 search proposals and 30 benchmark SLHA spectra
- The viable pMSSM is dominated by compressed electroweakino spectra: **Wino LSP (48%), Higgsino LSP (48%), Bino LSP (4%)**
- **15 models are "truly dark"** — invisible to both ATLAS and projected DARWIN direct detection sensitivity

---

## Methodology

### Pipeline
Each pMSSM parameter point was evaluated through an 8-step pipeline:
```
Input SLHA -> SPheno -> Softsusy -> micrOMEGAs -> SuperISO -> GM2Calc -> FeynHiggs -> SModelS -> Ntuple
```

### Constraints Applied
1. **Quality:** Both SPheno and Softsusy converge; neutralino is LSP
2. **Higgs mass:** 122 < m_h < 128 GeV (FH preferred, SP fallback)
3. **Relic density:** Omega h^2 <= 0.132
4. **B-physics:** BR(b->sgamma) and BR(Bs->mumu) within 2 sigma of measurements
5. **LHC exclusions:** SModelS r < 1 (not excluded by ATLAS/CMS simplified-model limits)
6. **LEP chargino:** m(chi1+) > 103 GeV (LEP2 direct search limit)

### Scan Phases

| Phase | Strategy | Models evaluated | Passing all cuts |
|-------|----------|:---------------:|:---------------:|
| Phase 1 (flat) | Uniform random | 2,000 | 5 |
| Phase 2a (EWKino) | MCMC targeted | 1,503 | 163 |
| Phase 2b (Stop) | MCMC targeted | 1,503 | 134 |
| Phase 2c (Slepton) | MCMC targeted | 2,004 | 71 |
| Phase 2d (Compressed) | MCMC targeted | 2,004 | 83 |
| Phase 3a-c (Refinements) | MCMC targeted | 4,509 | 2 |
| Phase 4a (Wino mapping) | MCMC targeted | 987 | 698 |
| Phase 4b (Higgsino soft) | MCMC targeted | 916 | 532 |
| Phase 4c (Slepton+Bino) | MCMC + grid | 2,895 | 0 |
| Phase 4d (Compressed stop) | MCMC + grid | 1,376 | 0 |
| Phase 4e (Mixed EWKino) | MCMC targeted | 952 | 375 |
| Phase 5a (Bino importance) | Importance sampling | 1,860 | 24 |
| Phase 5b (Stop importance) | Importance sampling | 2,940 | 0 |
| **Total** | | **26,048** | **2,087** |

---

## Results

### LSP Composition

| LSP Type | Count | Fraction | Dark matter mechanism |
|----------|:-----:|:--------:|----------------------|
| Wino | 1,009 | 48.3% | Efficient SU(2) annihilation -> under-abundant |
| Higgsino | 998 | 47.8% | Efficient gauge/Yukawa annihilation -> under-abundant |
| Bino | 80 | 3.8% | Co-annihilation or A-funnel resonance needed |

Wino and Higgsino LSPs naturally satisfy the relic density constraint. Bino LSPs require special mechanisms (co-annihilation with sleptons/stops, or resonant A-funnel annihilation through the pseudoscalar Higgs) to avoid overproducing dark matter.

### Physics Categories (non-exclusive)

| Category | Count | LHC Signature |
|----------|:-----:|---------------|
| Compressed EWKino (dm < 50 GeV) | 2,077 | Soft leptons + MET, disappearing tracks, monojet |
| Wino compressed (dm < 20 GeV) | 1,009 | Disappearing charged tracks |
| Higgsino compressed (dm < 30 GeV) | 863 | Soft leptons + MET, VBF + MET |
| Light slepton (< 600 GeV) | 653 | Opposite-sign dileptons + MET |
| Light sbottom (< 1.2 TeV) | 405 | b-jets + MET |
| Heavy Higgs accessible (< 1 TeV) | 308 | Ditau/diboson resonances |
| Light stop (< 1.2 TeV) | 293 | Top pairs + MET |
| Bino + light EWKinos | 80 | Multi-lepton + MET, WZ/Wh + MET |
| Compressed stop (dm < 200 GeV) | 7 | Charm-tagged jets + MET, monojet |

### Benchmark Models

9 benchmark SLHA files in `results/benchmarks/`, one per category, plus 30 gap-specific benchmarks in `results/atlas_proposals/benchmarks/`.

---

## ATLAS Coverage Assessment

Using SModelS v3.1.1, each model's spectrum is decomposed into simplified-model topologies and compared against published ATLAS/CMS limits.

| Tier | Label | Count | Fraction |
|------|-------|:-----:|:--------:|
| 0 | Invisible (no ATLAS constraint) | 1,372 | 65.7% |
| 1 | Negligible (r < 0.01) | 84 | 4.0% |
| 2 | Weak (0.01 < r < 0.3) | 301 | 14.4% |
| 3 | Moderate (0.3 < r < 0.8) | 227 | 10.9% |
| 4 | Near-exclusion (0.8 < r < 1.0) | 58 | 2.8% |
| 5 | Excluded (r > 1.0) | 45 | 2.2% |

**Important caveat:** SModelS v3.1.1 does not encode ATLAS disappearing-track (SUSY-2018-19), direct slepton (SUSY-2018-32), or compressed Higgsino (SUSY-2019-09) searches. Published ATLAS exclusion contours overlaid on mass-plane scatter plots confirm that a substantial fraction of "invisible" models fall within the reach of these existing analyses. The 65.7% invisible fraction is therefore an overestimate of true insensitivity.

### Five ATLAS Blind Spots

| Gap | Description | Models | Key signal | Priority |
|-----|-------------|:------:|------------|:--------:|
| A | Compressed Wino (dm ~ 0.2 GeV) | 520 | Disappearing tracks + MET | HIGH |
| B | Compressed Higgsino (dm ~ 1-20 GeV) | 737 | Soft dileptons + MET | HIGH |
| C | Light sleptons (200-600 GeV) | 509 | Dilepton + MET | MEDIUM |
| D | Compressed stop + displaced chargino | 2 | b-jet + displaced vertex | MEDIUM |
| E | Complex EWKino cascades | 80 | Multi-lepton + MET | LOW |

### Unexpected Blind Spots

Three categories are genuinely surprising — models at masses and cross-sections where simplified model results would predict exclusion:

1. **Light sleptons with Bino LSP (21 models):** Sleptons at 270-580 GeV with Bino LSP at 140-400 GeV are invisible despite direct slepton pair production being one of the cleanest SUSY signatures (ATLAS reach ~700 GeV for massless LSP). The pMSSM branching ratios dilute the clean dilepton signal compared to simplified-model assumptions, and SModelS lacks the slepton topology entirely.

2. **Compressed stops with displaced charginos (2 models, up to 14 pb):** Stops at 268 and 337 GeV are firmly within the T2tt exclusion contour but escape because the Wino LSP creates a long-lived chargino (ctau ~ 1-10 cm). The stop -> b + chi1+(displaced) -> b + soft pion + MET signature falls between prompt and displaced searches. A dedicated b-jet + displaced vertex search would target this novel gap.

3. **534 Wino models below the disappearing-track limit:** ATLAS-SUSY-2018-19 excludes pure Winos up to ~660 GeV, yet 534 Wino models with m(chi1+) < 660 GeV are invisible in SModelS — primarily because the disappearing-track topology is not encoded in the SModelS database. Encoding this single analysis would reclassify the majority of the 1,372 "invisible" models.

---

## Physics Conclusions

1. **Compressed electroweakino spectra dominate the viable pMSSM.** 99.5% of models have dm(chi1+, LSP) < 50 GeV. Dedicated compressed-spectrum searches are the highest-priority channels.

2. **Wino and Higgsino LSPs dominate; Bino requires fine-tuning.** Wino (48%) and Higgsino (48%) LSPs naturally satisfy the relic density constraint. Bino LSPs (4%) survive only through co-annihilation (extremely narrow corridor, ~O(1%) of parameter range) or A-funnel resonance (rare: 2 of 31 models pass).

3. **Light 3rd-generation squarks are abundant but partially uncovered.** 405 models have sbottom < 1.2 TeV and 293 have stop < 1.2 TeV, yet only ~2% are excluded by current LHC limits.

4. **B-physics is the harshest discriminant** after the Higgs mass, eliminating 15-20% of otherwise-viable models.

5. **Current LHC limits have limited impact** on the pMSSM. Only ~2% of physics-viable models are excluded by SModelS.

6. **Narrow corridors are intrinsically difficult.** The Bino co-annihilation strip (~10-20 GeV wide) and compressed-stop mixing line defeat both MCMC and grid sampling. Importance sampling from known viable seeds is the most effective method, achieving 1.3% yield for the co-annihilation corridor where other methods produced zero.

---

## Run 3 Search Recommendations

1. **Encode existing searches in SModelS** (highest impact): Adding SUSY-2018-19, SUSY-2018-32, and SUSY-2019-09 to SModelS would dramatically improve coverage assessment.
2. **Extend disappearing-track search (Gap A):** Reach from ~460 GeV toward 800+ GeV with ITk. 102 models excludable.
3. **Lower soft-lepton thresholds (Gap B):** ISR-boosted topology with mll binning down to 1 GeV. 42 models excludable.
4. **Extend slepton reach (Gap C):** mT2-based search to 400-500 GeV with 300 fb^-1. 165 models excludable.
5. **Novel displaced + b-jet search (Gap D):** Combine displaced vertex with b-tagging. Very large uncovered cross-sections (up to 14 pb).
6. **Multi-lepton cascade search (Gap E):** Asymmetric final-state signal regions. 22 models excludable.

---

## Deliverables

| Path | Description |
|------|-------------|
| `results/COMPLETE_FINDINGS.md` | Comprehensive report with all details |
| `results/SUMMARY.md` | This summary document |
| `results/atlas_coverage/` | SModelS coverage analysis (CSV, reports, 8 plots) |
| `results/atlas_proposals/` | Run 3 search proposals (30 benchmarks, 23 plots) |
| `results/benchmarks/` | 9 category benchmark SLHA files |
| `results/plots/` | 15 classification and summary plots |
| `analysis/` | All analysis scripts (7 scripts) |
| `configs/` | All scan configuration files |
| `scans/` | ROOT ntuples (54 files, ~1,131 branches per model) |
| `docs/` | Investigation plan, scan log, analysis notes, followup plan |

---

## Limitations

1. **Stau masses decoupled** at 2 TeV. Light staus would open co-annihilation channels.
2. **1st/2nd gen squarks decoupled** at 4 TeV. Some compressed scenarios could evade limits.
3. **No CP violation.** Relaxing this would enable new phenomenology.
4. **SModelS topology coverage** is incomplete. Three key ATLAS analyses are missing from the database.
5. **Statistics.** 2,087 models is sufficient for categories/benchmarks but insufficient for robust probability statements.
6. **Narrow corridors undersampled.** The compressed-stop line remains sparsely sampled (7 models) despite MCMC, grid, and importance sampling attempts.
