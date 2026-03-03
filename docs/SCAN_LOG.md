# Scan Log

Running log of all pMSSM scans performed in this project. Updated after each scan completes.

---

## Template

```
### Scan: [name]
- **Date:** YYYY-MM-DD
- **Config:** configs/[filename].yaml
- **Prior:** flat / mcmc
- **Seed:** [N]
- **Num models (requested):** [N]
- **Num models (produced):** [N]
- **Runtime:** [HH:MM:SS]
- **MCMC acceptance rate:** [N/A or X%]
- **Pipeline success rates:**
  - SPheno: X/N (Y%)
  - Softsusy: X/N (Y%)
  - micrOMEGAs: X/N (Y%)
  - SuperISO: X/N (Y%)
  - GM2Calc: X/N (Y%)
  - FeynHiggs: X/N (Y%)
  - SModelS: X/N (Y%)
- **Constraint pass rates (of valid models):**
  - Neutralino LSP: X/N (Y%)
  - Higgs mass: X/N (Y%)
  - Relic density: X/N (Y%)
  - B-physics: X/N (Y%)
  - SModelS allowed: X/N (Y%)
  - All cuts: X/N (Y%)
- **Observations:** [notes]
- **Ntuple path:** scans/[path]/ntuple.0.0.root
```

---

## Smoke Test

### Scan: smoke_test
- **Date:** 2026-02-25
- **Config:** configs/smoke_test_config.yaml
- **Prior:** flat
- **Seed:** 42
- **Num models (requested):** 5
- **Num models (produced):** 5
- **Runtime:** ~2 min
- **Pipeline success rates:**
  - SPheno: 1/5 (20%)
  - Full pipeline (through SModelS): 1/5 (20%)
- **Observations:** Most random pMSSM points fail SPheno (spectrum generator cannot find a valid SUSY spectrum). This is expected for flat sampling — the viable pMSSM parameter space is a small fraction of the full volume. SModelS was the slowest step due to Pythia compilation and cross-section computation on first run. Ntuple verified: 1131 branches in `susy` tree.
- **Ntuple path:** scans/smoke_test/ntuple.0.0.root

---

## Phase 1: Flat Exploration

### Scan: phase1_seed42 (COMPLETE)
- **Date:** 2026-02-25
- **Config:** configs/phase1_flat_config.yaml
- **Prior:** flat
- **Seed:** 42
- **Num models (requested):** 500
- **Num models (produced):** 500
- **Runtime:** ~12 min
- **Pipeline success rates:**
  - SPheno: 40/500 (8.0%)
  - micrOMEGAs: 40/500 (8.0%) — all SPheno successes proceed
  - SuperISO: 40/500 (8.0%)
  - GM2Calc: 40/500 (8.0%)
  - FeynHiggs: 40/500 (8.0%)
  - SModelS: 40/500 (8.0%)
- **Observations:** SPheno convergence rate of 8% confirms flat-sampling expectation: the vast majority of uniformly-drawn pMSSM points are unphysical (tachyonic masses, no EWSB). Once SPheno succeeds, all downstream tools succeed — zero pipeline dropout. 40 models have full spectra, dark matter, flavor, g-2, Higgs corrections, and LHC exclusion results. Constraint pass rates will be computed during Phase 1 analysis.
- **Ntuple path:** scans/phase1/scan_seed42/ntuple.0.0.root

### Scan: phase1_seed137 (COMPLETE)
- **Date:** 2026-03-03
- **Config:** configs/phase1_flat_config.yaml
- **Prior:** flat
- **Seed:** 137
- **Num models (requested):** 500
- **Num models (produced):** 500
- **Ntuple path:** scans/phase1/scan_seed137/ntuple.0.0.root

### Scan: phase1_seed256 (COMPLETE)
- **Date:** 2026-03-03
- **Config:** configs/phase1_flat_config.yaml
- **Prior:** flat
- **Seed:** 256
- **Num models (requested):** 500
- **Num models (produced):** 500
- **Ntuple path:** scans/phase1/scan_seed256/ntuple.0.0.root

### Scan: phase1_seed999 (COMPLETE)
- **Date:** 2026-03-03
- **Config:** configs/phase1_flat_config.yaml
- **Prior:** flat
- **Seed:** 999
- **Num models (requested):** 500
- **Num models (produced):** 500
- **Ntuple path:** scans/phase1/scan_seed999/ntuple.0.0.root

### Phase 1 Combined Results (all 4 seeds merged)
- **Total models:** 2000
- **Pipeline success rates:**
  - SPheno: 211/2000 (10.5%)
  - Softsusy: 196/2000 (9.8%)
  - micrOMEGAs: 196/2000 (9.8%)
  - SuperISO: 195/2000 (9.8%)
  - GM2Calc: 194/2000 (9.7%)
  - FeynHiggs: 185/2000 (9.2%)
  - SModelS: 171/2000 (8.6%)
- **Cutflow:**
  - Quality (both specgen OK): 196 (9.8%)
  - Neutralino LSP: 192 (9.6%)
  - Higgs mass [122-128]: 40 (2.0%)
  - Relic density [≤0.132]: 36 (1.8%)
  - B-physics [2σ]: 7 (0.4%)
  - SModelS allowed: 7 (0.4%)
  - **All cuts: 7 (0.4%)**
- **LSP composition (7 survivors):** 4 Wino, 3 Higgsino, 0 Bino
- **Plots:** results/plots/phase1_*.png

---

## Phase 2: Targeted MCMC Scans

All Phase 2 scans used 3 seeds each (42, 137, 256) running in parallel with max 10 workers.
MCMC scans hit max_attempts before reaching 500 models in most cases (especially sleptons and compressed).
Ntuples were generated post-hoc using `run_ntupling.py`.

### Phase 2a: Light Electroweakinos
- **Date:** 2026-03-03
- **Config:** configs/phase2a_ewkino_config.yaml
- **Prior:** mcmc
- **Seeds:** 42, 137, 256
- **Models produced:** 226 + 143 + 233 = 602 (of 500×3 = 1500 requested)
- **Cutflow (combined 1503 ntuple entries):**
  - Quality (both specgen OK): 602 (40.1%)
  - Neutralino LSP: 598 (39.8%)
  - Higgs mass: 258 (17.2%)
  - Relic density: 258 (17.2%)
  - B-physics: 232 (15.4%)
  - SModelS allowed: 231 (15.4%)
  - **All cuts: 231**
- **LSP composition:** Bino=12, Wino=137, Higgsino=82
- **Ntuple paths:** scans/phase2a/scan_seed{42,137,256}/ntuple.0.0.root

### Phase 2b: Light Stops/Sbottoms
- **Date:** 2026-03-03
- **Config:** configs/phase2b_stop_config.yaml
- **Prior:** mcmc
- **Seeds:** 42, 137, 256
- **Models produced:** 184 + 154 + 202 = 540
- **Cutflow (combined 1503 ntuple entries):**
  - Quality: 540 (35.9%)
  - Neutralino LSP: 538 (35.8%)
  - Higgs mass: 182 (12.1%)
  - Relic density: 182 (12.1%)
  - B-physics: 177 (11.8%)
  - SModelS allowed: 166 (11.0%)
  - **All cuts: 166**
- **LSP composition:** Bino=2, Wino=161, Higgsino=3
- **Notable:** 11 models excluded by SModelS — these have light stops/sbottoms near current limits
- **Ntuple paths:** scans/phase2b/scan_seed{42,137,256}/ntuple.0.0.root

### Phase 2c: Light Sleptons
- **Date:** 2026-03-03
- **Config:** configs/phase2c_slepton_config.yaml
- **Prior:** mcmc
- **Seeds:** 42, 137, 256
- **Models produced:** 102 + 103 + 1 = 206 (lowest yield — slepton models hard to find)
- **Cutflow (combined 1503 ntuple entries):**
  - Quality: 206 (13.7%)
  - Neutralino LSP: 197 (13.1%)
  - Higgs mass: 77 (5.1%)
  - Relic density: 77 (5.1%)
  - B-physics: 62 (4.1%)
  - SModelS allowed: 60 (4.0%)
  - **All cuts: 60**
- **LSP composition:** Bino=11, Wino=35, Higgsino=14
- **Notable:** Seed 256 produced only 1 model (likely MCMC chain stuck; needs retry)
- **Ntuple paths:** scans/phase2c/scan_seed{42,137,256}/ntuple.0.0.root

### Phase 2d: Compressed Spectra
- **Date:** 2026-03-03
- **Config:** configs/phase2d_compressed_config.yaml
- **Prior:** mcmc
- **Seeds:** 42, 137, 256
- **Models produced:** 146 + 245 + 1 = 392
- **Cutflow (combined 1503 ntuple entries):**
  - Quality: 392 (26.1%)
  - Neutralino LSP: 392 (26.1%)
  - Higgs mass: 153 (10.2%)
  - Relic density: 153 (10.2%)
  - B-physics: 136 (9.0%)
  - SModelS allowed: 136 (9.0%)
  - **All cuts: 136**
- **LSP composition:** Bino=3, Wino=81, Higgsino=52
- **Notable:** Seed 256 produced only 1 model; seed 42 may have hit max_attempts=40000
- **Ntuple paths:** scans/phase2d/scan_seed{42,137,256}/ntuple.0.0.root

### Phase 2 Combined Results
- **Total models generated:** 1740 (across 12 scans)
- **Passing all cuts:** 593
- **LSP composition:** Bino=28, Wino=414, Higgsino=151
- **Category populations (non-exclusive):**
  - Compressed_EWK: 585
  - Wino_compressed: 414
  - Light_sbottom: 357
  - Light_slepton: 312
  - Light_stop: 224
  - Higgsino_compressed: 104
  - Heavy_Higgs: 88
  - Bino+lightEWK: 28
  - Compressed_stop: 5
- **Plots:** results/plots/phase2_*.png

---

## Phase 3: Refinement Scans

Phase 3 targeted specific gaps identified in Phase 2 analysis. Three new scan types plus reruns of failed Phase 2 seeds.

### Phase 3a: Bino Co-annihilation (FAILED — 0 accepted models)
- **Date:** 2026-03-03
- **Config:** configs/phase3a_bino_coannihilation_config.yaml
- **Prior:** mcmc (max_attempts=40000)
- **Seeds:** 42, 137, 256
- **Models produced:** 0 (all 3 seeds hit max_attempts with 0 accepted models)
- **Observations:** The co-annihilation corridor (m_slepton ≈ m_Bino ± 50 GeV) is extremely narrow. With M_2/mu at [800,2000] to force Bino LSP and sleptons at [100,700], the MCMC chain never found a point satisfying all constraints simultaneously. The burn-in threshold (100 accepted models) was never reached. Would require alternative sampling strategies (e.g., grid scan near known co-annihilation lines, or adaptive MCMC with temperature annealing).

### Phase 3b: A-funnel (PARTIAL SUCCESS — 31 accepted models from seed 256)
- **Date:** 2026-03-03
- **Config:** configs/phase3b_afunnel_config.yaml
- **Prior:** mcmc (max_attempts=40000)
- **Seeds:** 42, 137, 256
- **Models produced:** 0 + 0 + 31 = 31 (only seed 256 found the funnel)
- **Passing all offline cuts:** 2
- **Observations:** Pure Bino LSP models (N11²≈0.998) with mA ≈ 2×m(chi10), confirming A-funnel resonant annihilation mechanism. tanb~25-29, m_h(SPheno)~117-120 GeV. Most models have SPheno m_h slightly below our 122 GeV offline cut but FeynHiggs corrections push some into the window. 2 models survive all cuts including LEP chargino limit.
- **Ntuple paths:** scans/phase3b/scan_seed{42,137,256}/ntuple.0.0.root

### Phase 3c: Compressed Stop (FAILED — 0 accepted models)
- **Date:** 2026-03-03
- **Config:** configs/phase3c_compressed_stop_config.yaml
- **Prior:** mcmc (max_attempts=40000)
- **Seeds:** 42, 137, 256
- **Models produced:** 0 (all seeds hit max_attempts with 0 accepted)
- **Observations:** Achieving dm(stop1, LSP) < 200 GeV while simultaneously satisfying Higgs mass, relic density, and B-physics constraints is extremely challenging. The combination of light 3rd-gen squarks (mqL3, mtR in [200,800]) with M_1/M_2 in [-600,600] creates a narrow viable region that the MCMC chain could not locate.

### Phase 2c Rerun (seed 314) — SUCCESS (97 accepted models)
- **Date:** 2026-03-03
- **Config:** configs/phase2c_slepton_config.yaml
- **Prior:** mcmc
- **Seed:** 314
- **Models produced:** 97 (replacing failed seed 256 which produced 1 model)
- **Ntuple path:** scans/phase2c/scan_seed314/ntuple.0.0.root

### Phase 2d Rerun (seed 314) — FAILED (0 accepted models)
- **Date:** 2026-03-03
- **Config:** configs/phase2d_compressed_config.yaml
- **Prior:** mcmc
- **Seed:** 314
- **Models produced:** 0 (hit max_attempts)
- **Ntuple path:** scans/phase2d/scan_seed314/ntuple.0.0.root

---

## Final Combined Results (All Phases, with LEP cut)

- **Total ntuple entries:** 13523 (2000 Phase 1 + 7516 Phase 2 + 4507 Phase 3)
- **Passing all cuts (including m(chi1+) > 103 GeV):** 458 (3.4%)
  - Phase 1: 5
  - Phase 2a: 163
  - Phase 2b: 134
  - Phase 2c: 71
  - Phase 2d: 83
  - Phase 3b: 2
- **LSP composition:** Bino=29, Wino=359, Higgsino=70
- **All 9 physics categories populated**
- **Benchmark models extracted per category**
- **Plots:** results/plots/final_*.png
