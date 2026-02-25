# Analysis Notes

Observations and physics insights from each analysis phase. Updated continuously as results are produced.

---

## Smoke Test Observations (2026-02-25)

- **SPheno failure rate is high for flat sampling (~80-92%):** Most randomly-drawn pMSSM parameter points do not yield a valid SUSY spectrum. This is physically expected — the viable parameter space is a narrow subset of the full 19-dimensional volume. Common failure modes include tachyonic masses (negative mass-squared for scalars) and failure to achieve electroweak symmetry breaking.
- **Pipeline is serial and bottlenecked by SPheno:** If SPheno fails, no downstream tools run. Successfully computed models then pass through all downstream tools (Softsusy, micrOMEGAs, SuperISO, GM2Calc, FeynHiggs, SModelS).
- **SModelS is the slowest step:** First-time Pythia compilation adds ~1 min overhead; subsequent models compute cross-sections in ~30-60s each.
- **Implication for Phase 2:** MCMC sampling with physics constraints will dramatically improve the yield of viable models by concentrating sampling in physically allowed regions.

## Phase 1: Flat Exploration

### Seed42 scan: COMPLETE (500 models, 40 valid spectra)

- **SPheno success rate: 8.0% (40/500)** — the true flat-prior convergence rate for our parameter ranges. The 20% rate in the 5-model smoke test was small-number statistics.
- **Zero downstream dropout:** All 40 SPheno successes passed through micrOMEGAs, SuperISO, GM2Calc, FeynHiggs, and SModelS without failure. This is a robust feature — once SPheno produces a valid spectrum, the physics tools can always evaluate it.
- **Runtime: ~12 min** for 500 models. Failed models are essentially free (SPheno returns instantly on failure). The cost scales with the number of SPheno successes × ~30-60s per successful model.
- **Projection for full Phase 1:** 4 × 500 flat models → expect ~160 valid spectra. After Higgs mass, relic density, B-physics, and SModelS cuts, expect ~20-50 surviving models — sufficient for landscape characterization.
- **Seeds 137, 256, 999 pending** — will run next to complete Phase 1.

(Full Phase 1 cutflow analysis will be completed after all 4 seed scans finish)

---

## Phase 2: Targeted MCMC Scans

### Phase 2a: Light Electroweakinos
(to be filled)

### Phase 2b: Light Stops/Sbottoms
(to be filled)

### Phase 2c: Light Sleptons
(to be filled)

### Phase 2d: Compressed Spectra
(to be filled)

---

## Classification Results

(to be filled after Step 3 analysis)
