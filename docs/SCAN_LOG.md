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

### Scan: phase1_seed137 (PENDING)
- **Config:** configs/phase1_flat_config.yaml, seed 137

### Scan: phase1_seed256 (PENDING)
- **Config:** configs/phase1_flat_config.yaml, seed 256

### Scan: phase1_seed999 (PENDING)
- **Config:** configs/phase1_flat_config.yaml, seed 999

---

## Phase 2: Targeted MCMC Scans

(entries will be added as scans complete)
