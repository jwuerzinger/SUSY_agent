# Analysis Notes

Observations and physics insights from each analysis phase. Updated continuously as results are produced.

---

## Smoke Test Observations (2026-02-25)

- **SPheno failure rate is high for flat sampling (~80-92%):** Most randomly-drawn pMSSM parameter points do not yield a valid SUSY spectrum. This is physically expected — the viable parameter space is a narrow subset of the full 19-dimensional volume. Common failure modes include tachyonic masses (negative mass-squared for scalars) and failure to achieve electroweak symmetry breaking.
- **Pipeline is serial and bottlenecked by SPheno:** If SPheno fails, no downstream tools run. Successfully computed models then pass through all downstream tools (Softsusy, micrOMEGAs, SuperISO, GM2Calc, FeynHiggs, SModelS).
- **SModelS is the slowest step:** First-time Pythia compilation adds ~1 min overhead; subsequent models compute cross-sections in ~30-60s each.
- **Implication for Phase 2:** MCMC sampling with physics constraints will dramatically improve the yield of viable models by concentrating sampling in physically allowed regions.

## Phase 1: Flat Exploration

### Full Phase 1 Results (2000 models, 4 seeds merged)

**Pipeline:**
- SPheno convergence: 10.5% (211/2000). Slightly higher than seed42's 8.0% — normal statistical variation across seeds.
- Both spectrum generators agree: 196/2000 (9.8%) pass both SPheno and Softsusy.
- Small dropout through the pipeline: 196 → 195 → 194 → 185 → 171. FeynHiggs and SModelS have occasional failures (~5-12% of valid spectra), unlike the seed42 run where dropout was zero.

**Cutflow — where models die:**
1. Quality + neutralino LSP: 192/2000 (9.6%) — 4 models have charged/colored LSPs
2. **Higgs mass [122-128 GeV]**: 40/192 (20.8%) — the Higgs mass is the first major filter. Most valid spectra predict m_h < 122 GeV (insufficient stop mixing or too-low tan(beta)).
3. **Relic density [Ω ≤ 0.132]**: 36/40 (90%) — surprisingly mild at this stage. Most models that pass the Higgs cut already have moderate relic density. The bimodal relic density distribution shows peaks at Ω ~ 10⁻² (under-abundant, Wino/Higgsino LSP) and Ω ~ 1-100 (over-abundant, Bino LSP), with few models near the Planck value.
4. **B-physics [2σ]**: 7/36 (19%) — **the harshest physics cut**. BR(b→sγ) and BR(Bs→μμ) together eliminate ~80% of otherwise-viable models. This is driven by large tan(beta) combined with light charginos/stops entering the loop corrections.
5. **SModelS**: 7/7 (100%) — all B-physics survivors are also allowed by LHC direct searches. These models have heavy enough sparticles to evade current limits.

**LSP composition of 7 survivors: 4 Wino (57%), 3 Higgsino (43%), 0 Bino (0%)**

This is striking: **no Bino LSP models survive flat sampling**. Bino-like neutralinos generically overproduce dark matter (Ω >> 0.12) because they lack efficient annihilation channels. Surviving Binos would require co-annihilation or resonance enhancement, which is rare in flat sampling. Wino and Higgsino LSPs naturally have small relic density due to efficient electroweak annihilation.

**Properties of the 7 surviving models:**

| # | LSP type | m(LSP) | Δm(χ₁±,LSP) | m(t̃₁) | m(b̃₁) | Ωh² | SModelS r |
|---|----------|--------|-------------|--------|--------|------|-----------|
| 1 | Wino | 141 | 0.2 | 1367 | 829 | 0.0005 | 0.068 |
| 2 | Wino | 220 | 0.2 | 1449 | 1554 | 0.0012 | 0.040 |
| 3 | Wino | 43 | 0.1 | 1238 | 1492 | ~0 | — |
| 4 | Higgsino | 153 | 3.0 | 1226 | 1068 | 0.0033 | 0.479 |
| 5 | Higgsino | 193 | 5.3 | 1368 | 920 | 0.0041 | 0.008 |
| 6 | Wino | 266 | 0.2 | 765 | 786 | 0.0019 | 0.101 |
| 7 | Higgsino | 52 | 7.9 | 1421 | 577 | 0.0029 | 0.119 |

**Key physics observations:**
- **Wino LSPs** have tiny chargino-LSP splittings (~0.1-0.2 GeV) — classic disappearing-track signature at the LHC.
- **Higgsino LSPs** have moderate splittings (3-8 GeV) — soft lepton + MET signatures.
- **All models are deeply under-abundant** (Ωh² << 0.12) — the neutralino is only a small fraction of dark matter.
- **Model 6** has a light stop (765 GeV) — within Run 3 reach for direct stop searches.
- **Model 7** has a light sbottom (577 GeV) and very light 52 GeV Higgsino LSP.
- **Model 3** has a 43 GeV Wino LSP and light selectron_L (490 GeV) — potential slepton search target.
- **Model 4** is closest to SModelS exclusion (r=0.479) — half-way to being ruled out.
- All surviving models have mA > 1 TeV and tan(beta) > 20, indicating heavy Higgs sector is decoupled.

**Implications for Phase 2:**
- MCMC with physics constraints should dramatically increase the yield of viable models.
- Phase 2a (electroweakinos) should populate the Wino and Higgsino compressed regions seen here.
- Phase 2b (stops) should find more models like #6 with accessible stop masses.
- Phase 2c (sleptons) should find models like #3 with light sleptons.
- Phase 2d (compressed) should enrich the disappearing-track and soft-lepton scenarios.
- The absence of Bino survivors in flat sampling is a key result — MCMC may find Bino models near co-annihilation or A-funnel resonances.

---

## Phase 2: Targeted MCMC Scans (2026-03-03)

### Overview

MCMC sampling with physics constraints as likelihood dramatically improved yield: **593 models pass all cuts** from Phase 2 vs 7 from Phase 1. The MCMC approach concentrates sampling in physically viable regions, achieving a ~85× improvement in per-model yield. All 4 targeted scan types found viable models, confirming the scan strategy was well-designed.

**Technical note:** Scans were run with 3 seeds each (42, 137, 256) for 10 workers total. Most scans hit `max_attempts` (30000-40000) before reaching the 500-model target, especially slepton and compressed scans. Seed 256 produced only 1 model for phase2c and phase2d (MCMC chain likely got stuck in a bad region). Ntuples contain 501 entries per seed; empty slots (model IDs with no files) have -1 values, filtered by the quality cut.

### Phase 2a: Light Electroweakinos — 231 passing models

Best-performing scan type. MCMC found rich electroweakino phenomenology:
- **602 valid spectra** from 1503 ntuple entries → 231 pass all cuts (38.4% of valid)
- Dominated by Wino (137) and Higgsino (82) LSPs, with 12 Bino
- The Bino models are important: they show co-annihilation and A-funnel mechanisms that were absent in Phase 1
- All 231 have compressed EWKino spectra (dm(chi1+, LSP) < 50 GeV)
- 144 have light sleptons (< 600 GeV) — potential slepton pair production in addition to EWKino production
- 86 have light stops, 85 have light sbottoms

### Phase 2b: Light Stops/Sbottoms — 166 passing models

Overwhelmingly Wino LSP (161/166 = 97%):
- **540 valid spectra** → 166 pass all cuts (30.7% of valid)
- Only 3 Higgsino and 2 Bino LSP models — Wino LSP dominates when 3rd-gen squarks are light
- 116 have light stops (< 1.2 TeV), 144 have light sbottoms — many models have both
- SModelS excluded 11 models that passed all other cuts — these probe the boundary of current LHC stop/sbottom limits
- Only 2 compressed-stop models (dm(stop1, LSP) < 200 GeV) — most stops are far above the LSP

### Phase 2c: Light Sleptons — 60 passing models

Hardest region to sample (lowest yield):
- **206 valid spectra** → 60 pass all cuts (29.1% of valid, but only 206 spectra generated)
- Seed 256 essentially failed (1 model) — the narrow slepton mass window [100-700] combined with the need for M_1 < m_slepton makes this a challenging region
- All 60 have light sleptons by design; 51 also have light sbottoms
- Most diverse LSP composition: Bino=11, Wino=35, Higgsino=14
- The 11 Bino LSP models are especially interesting: direct slepton pair production followed by slepton → lepton + Bino gives the cleanest LHC signal
- 23 have accessible heavy Higgs (mH or mA < 1 TeV)

### Phase 2d: Compressed Spectra — 136 passing models

Explored the most experimentally challenging region:
- **392 valid spectra** → 136 pass all cuts (34.7% of valid)
- Wino=81, Higgsino=52, Bino=3
- All 136 have compressed EWKino spectra
- 82 have light sleptons — surprising overlap with slepton searches
- 42 have accessible heavy Higgs — could be discovered in ditau searches
- These models represent blind spots of conventional LHC searches; need dedicated disappearing-track and soft-lepton analyses

### Key Physics Observations from Phase 2

1. **Wino dominance (70%):** Wino-like LSPs dominate across all scan types (414/593). This is because:
   - Winos annihilate efficiently via SU(2) gauge interactions → naturally satisfy relic density
   - The MCMC likelihood strongly favors low Omega, and Winos deliver this easily
   - The Wino mass parameter M_2 directly controls m(chi1+) and m(chi10) with very small splitting

2. **B-physics remains the harshest cut:** Even with MCMC, B-physics eliminates ~15-20% of models that pass all other cuts. The b→sγ branching ratio is sensitive to chargino-stop loop corrections.

3. **Bino LSP is rare but found (28 models):** Phase 1 found zero Bino models; Phase 2 found 28 via MCMC exploration of co-annihilation regions. These are high-value targets.

4. **Sleptons are hard to sample:** Phase 2c had by far the lowest yield. The simultaneous requirements of light sleptons + heavier LSP + Higgs mass + B-physics create a narrow viable corridor.

5. **SModelS rarely excludes:** Only 11/604 models passing physics cuts were excluded by current LHC limits. Most surviving models have sparticle masses in regions not yet probed, confirming these as genuine discovery targets.

---

## Phase 3: Refinement Scans (2026-03-03)

### Overview

Phase 3 targeted three specific gaps identified in the Phase 2 analysis:
- **Phase 3a (Bino co-annihilation):** 0 accepted models (3 seeds) — corridor too narrow for MCMC
- **Phase 3b (A-funnel):** 31 models from seed 256 (seeds 42/137 failed) — 2 pass all offline cuts
- **Phase 3c (Compressed stop):** 0 accepted models (3 seeds) — parameter space too constrained
- **Phase 2c rerun (seed 314):** 97 models — successfully replaced failed seed 256
- **Phase 2d rerun (seed 314):** 0 models — hit max_attempts

### Phase 3b A-funnel: Physics Validation

The 31 A-funnel models confirm the resonance mechanism:
- All are nearly pure Bino (N11² ≈ 0.998)
- mA / (2 × m(chi10)) = 1.00–1.06 — precisely on the s-channel resonance
- tanβ ∈ [25, 29] — large tanβ enhances the A–Bino–Bino coupling
- m_h(SPheno) ~ 117–120 GeV — most below the 122 GeV offline cut
- FeynHiggs corrections push 2 models above 122 GeV → these survive all cuts
- **These are the only dedicated Bino-mechanism models in the entire sample**, confirming that the A-funnel works but is narrow

### Phase 3a/3c Failure Analysis

Both scans hit max_attempts=40000 with zero accepted models (never reaching burn-in=100):
- **3a:** Requiring simultaneously |M_1| < sleptons, m(slepton) ∈ [100,700], M_2/mu > 800, plus Higgs mass + relic density + B-physics is over-constrained for MCMC navigation. The co-annihilation corridor is a 1-2 dimensional surface in the 19D space.
- **3c:** Having mqL3/mtR ∈ [200,800] close to |M_1/M_2| ∈ [-600,600] while satisfying m_h > 122 GeV (which needs large AT and heavy stops for radiative corrections) creates a contradiction.

**Conclusion:** These narrow corridors require either grid scans near analytically known lines, importance sampling, or nested sampling — standard MCMC with broad proposal widths cannot efficiently discover them.

---

## Final Classification Results (All Phases Combined, with LEP cut, 2026-03-03)

### Combined Statistics
- **Total models:** 13523 ntuple entries (all phases)
- **Passing all cuts (including m(chi1+) > 103 GeV):** 458 (3.4%)
- **By source:** Phase 1: 5, Phase 2a: 163, Phase 2b: 134, Phase 2c: 71, Phase 2d: 83, Phase 3b: 2

### Impact of LEP Chargino Cut
Adding m(chi1+) > 103 GeV removes models with very light Wino/Higgsino LSP where the chargino would have been seen at LEP. This cut reduced the total from ~600 (pre-LEP) to 458 models. The most affected categories are Wino_compressed and Higgsino_compressed, losing the ultra-light benchmarks (6-8 GeV LSP models).

### LSP Composition (post-LEP cut)
| Type | Count | Fraction |
|------|-------|----------|
| Bino | 29 | 6.3% |
| Wino | 359 | 78.4% |
| Higgsino | 70 | 15.3% |

### Category Populations (non-exclusive)
| Category | Count | Description |
|----------|-------|-------------|
| Compressed_EWK | 448 | dm(chi1+, LSP) < 50 GeV |
| Wino_compressed | 359 | Wino LSP, dm(chi1+, LSP) < 20 GeV |
| Light_sbottom | 290 | m(b1) < 1.2 TeV |
| Light_slepton | 259 | min(m(eL), m(eR)) < 600 GeV |
| Light_stop | 198 | m(t1) < 1.2 TeV |
| Heavy_Higgs | 60 | m(H) or m(A) < 1 TeV |
| Higgsino_compressed | 58 | Higgsino LSP, dm(chi20, LSP) < 30 GeV |
| Bino+lightEWK | 29 | Bino LSP + light charginos/neutralinos |
| Compressed_stop | 7 | dm(stop1, LSP) < 200 GeV |

### Benchmark Models (best per category, post-LEP cut)

| Category | Source | LSP | m(LSP) | Key mass | Key feature |
|----------|--------|-----|--------|----------|-------------|
| Bino+lightEWK | phase2c | Bino | 95 GeV | m(chi20)=107 GeV | Bino with light electroweakinos |
| Wino_compressed | phase2b | Wino | 722 GeV | dm=0.2 GeV | High-mass disappearing tracks |
| Higgsino_compressed | phase2d | Higgsino | 122 GeV | dm(chi1+)=1.1 GeV | Soft leptons + MET |
| Light_stop | phase2c | Wino | 171 GeV | m(t1)=268 GeV | Lightest stop in sample |
| Light_sbottom | phase2b | Higgsino | 174 GeV | m(b1)=295 GeV | SModelS r=0.751, near exclusion |
| Light_slepton | phase2c | Bino | 127 GeV | m(eL)=162 GeV | Clean dilepton + MET |
| Compressed_EWK | phase2b | Wino | 722 GeV | dm=0.2 GeV | Same as Wino_compressed |
| Compressed_stop | phase2c | Wino | 171 GeV | dm(t1,LSP)=97 GeV | Stealth stop signature |
| Heavy_Higgs | phase2c | Higgsino | 211 GeV | m(H,A)=530 GeV | Accessible ditau resonance |

### Key Takeaways

1. **All 9 physics categories are populated** — the scan strategy successfully covered the pMSSM landscape.
2. **93.7% of surviving models are Wino or Higgsino LSP** — Bino models require fine-tuning (co-annihilation, A-funnel).
3. **Most models have compressed EWKino spectra** (448/458) — this is the dominant phenomenology.
4. **Light 3rd-gen squarks are common** — 290 models with light sbottom, 198 with light stop.
5. **Many models overlap multiple categories** — a model with a light stop may also have light sleptons and compressed EWKinos.
6. **Current LHC limits have weak impact** — only ~2% of physics-viable models are SModelS-excluded, confirming large unprobed territory.
7. **LEP chargino cut is important** — removes ~24% of pre-LEP models, especially affecting ultra-light LSP scenarios.
8. **A-funnel mechanism confirmed but narrow** — only 2 dedicated Bino A-funnel models survive all cuts, confirming the mechanism exists but requires precise parameter tuning.
9. **Co-annihilation and compressed-stop corridors remain elusive** — standard MCMC cannot efficiently sample these narrow corridors; alternative sampling methods would be needed for future investigation.
