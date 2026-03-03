# pMSSM Investigation: Final Summary

## Executive Summary

This investigation systematically explored the 19-parameter phenomenological MSSM (pMSSM) to identify viable SUSY models relevant for LHC Run 3 searches. Using a three-phase scan strategy — flat exploration, targeted MCMC sampling, and refinement scans — we evaluated ~13,500 parameter points through a full physics pipeline (SPheno, Softsusy, micrOMEGAs, SuperISO, GM2Calc, FeynHiggs, SModelS) and applied all current experimental constraints.

**Key result: 458 pMSSM models survive all constraints**, covering 9 distinct physics categories with concrete benchmark spectra for each.

---

## Methodology

### Pipeline
Each pMSSM parameter point was evaluated through an 8-step pipeline:
```
Input SLHA → SPheno → Softsusy → micrOMEGAs → SuperISO → GM2Calc → FeynHiggs → SModelS → Ntuple
```

### Constraints Applied
1. **Quality:** Both SPheno and Softsusy converge; neutralino is LSP
2. **Higgs mass:** 122 < m_h < 128 GeV (FH preferred, SP fallback)
3. **Relic density:** Omega h^2 <= 0.132
4. **B-physics:** BR(b→sγ) and BR(Bs→μμ) within 2σ of measurements
5. **LHC exclusions:** SModelS r < 1 (not excluded by ATLAS/CMS simplified-model limits)
6. **LEP chargino:** m(chi1+) > 103 GeV (LEP2 direct search limit)

### Scan Phases

| Phase | Strategy | Models evaluated | Passing all cuts |
|-------|----------|-----------------|-----------------|
| Phase 1 (flat) | Uniform random | 2000 | 5 |
| Phase 2a (EWKino) | MCMC targeted | 1503 | 163 |
| Phase 2b (Stop) | MCMC targeted | 1503 | 134 |
| Phase 2c (Slepton) | MCMC targeted | 2004 | 71 |
| Phase 2d (Compressed) | MCMC targeted | 2004 | 83 |
| Phase 3b (A-funnel) | MCMC targeted | 1503 | 2 |
| Phase 3a,3c (Co-ann., Comp. stop) | MCMC targeted | 3006 | 0 |
| **Total** | | **13523** | **458** |

---

## Results

### LSP Composition

| LSP Type | Count | Fraction | Dark matter mechanism |
|----------|-------|----------|----------------------|
| Wino | 359 | 78.4% | Efficient SU(2) annihilation → under-abundant |
| Higgsino | 70 | 15.3% | Efficient gauge/Yukawa annihilation → under-abundant |
| Bino | 29 | 6.3% | Co-annihilation or A-funnel resonance needed |

The Wino dominance is a robust physics result: Wino-like neutralinos naturally satisfy the relic density constraint because they annihilate efficiently through SU(2) gauge interactions. Bino LSPs require special mechanisms (co-annihilation with sleptons/stops, or resonant A-funnel annihilation through the pseudoscalar Higgs) to avoid overproducing dark matter. Our Phase 3 A-funnel scan confirmed this mechanism works but occupies an extremely narrow parameter corridor.

### Physics Categories (non-exclusive)

| Category | Count | LHC Signature |
|----------|-------|---------------|
| Compressed EWKino (dm < 50 GeV) | 448 | Soft leptons + MET, disappearing tracks, monojet |
| Wino compressed (dm < 20 GeV) | 359 | Disappearing charged tracks |
| Light sbottom (< 1.2 TeV) | 290 | b-jets + MET |
| Light slepton (< 600 GeV) | 259 | Opposite-sign dileptons + MET |
| Light stop (< 1.2 TeV) | 198 | Top pairs + MET, single lepton + jets + MET |
| Heavy Higgs accessible (< 1 TeV) | 60 | Ditau/diboson resonances |
| Higgsino compressed (dm < 30 GeV) | 58 | Soft leptons + MET, VBF + MET |
| Bino + light EWKinos | 29 | Multi-lepton + MET, WZ/Wh + MET |
| Compressed stop (dm < 200 GeV) | 7 | Charm-tagged jets + MET, monojet |

### Benchmark Models

9 benchmark SLHA files extracted to `results/benchmarks/`, one per category:

| Category | LSP | m(LSP) | Key feature | SModelS r |
|----------|-----|--------|-------------|-----------|
| Bino+lightEWK | Bino | 95 GeV | m(chi20)=107 GeV, light sleptons | 0.049 |
| Wino compressed | Wino | 722 GeV | dm(chi1+)=0.2 GeV, heavy spectrum | 0.029 |
| Higgsino compressed | Higgsino | 122 GeV | dm(chi1+)=1.1 GeV | 0.003 |
| Light stop | Wino | 171 GeV | m(t1)=268 GeV, stealth stop | <0.001 |
| Light sbottom | Higgsino | 174 GeV | m(b1)=295 GeV, near exclusion | 0.751 |
| Light slepton | Bino | 127 GeV | m(eL)=162 GeV, clean dilepton | 0.469 |
| Compressed EWKino | Wino | 722 GeV | dm=0.2 GeV | 0.029 |
| Compressed stop | Wino | 171 GeV | dm(t1,LSP)=97 GeV | <0.001 |
| Heavy Higgs | Higgsino | 211 GeV | m(H,A)=530 GeV, ditau target | 0.024 |

---

## Physics Conclusions

### 1. Compressed electroweakino spectra dominate the viable pMSSM

448 of 458 surviving models (97.8%) have dm(chi1+, LSP) < 50 GeV. This is the natural prediction of the pMSSM when constrained by current data: the lightest neutralino and chargino are nearly degenerate, making conventional LHC searches with hard leptons/jets insensitive.

**Implication for Run 3:** Dedicated compressed-spectrum searches (disappearing tracks, soft leptons + MET, monojet) are the highest-priority channels for discovering pMSSM SUSY.

### 2. Light 3rd-generation squarks remain abundant and partially uncovered

290 models have sbottom masses below 1.2 TeV and 198 have stop masses below 1.2 TeV. Yet only ~2% of physics-viable models are excluded by current LHC limits (SModelS r > 1). The gap between current exclusion boundaries and the bulk of viable models represents genuine discovery territory.

**Implication for Run 3:** Stop and sbottom searches should push to higher masses and explore compressed-spectrum scenarios (dm < 200 GeV) where current analyses lose sensitivity.

### 3. Bino dark matter requires fine-tuned mechanisms

Only 29 Bino LSP models survive (6.3%), all requiring either co-annihilation with nearby sleptons/stops or A-funnel resonance (mA ≈ 2m_Bino). Our dedicated Phase 3 scans confirmed:
- **A-funnel mechanism works** but occupies a very narrow corridor (2/31 models pass all cuts)
- **Bino-slepton co-annihilation** could not be found by standard MCMC (0/3 seeds succeeded)

**Implication:** If the neutralino is Bino-like, there must be a specific mass relation with other sparticles — either a slepton/stop near-degenerate with the LSP, or a pseudoscalar Higgs at twice the LSP mass.

### 4. Current LHC limits have limited impact on the pMSSM

Only ~2% of models passing all physics constraints are excluded by SModelS (which encodes all published ATLAS/CMS simplified-model limits). This confirms that the pMSSM parameter space is largely unprobed by current searches — the simplified-model interpretations used by the experiments cover only a subset of the full pMSSM phenomenology.

### 5. B-physics is the harshest discriminant after the Higgs mass

Across all phases, the B-physics constraints (b→sγ and Bs→μμ branching ratios) eliminate 15-20% of otherwise-viable models. These constraints are sensitive to chargino-stop loop corrections at large tanβ, providing complementary discrimination to direct LHC searches.

### 6. LEP chargino limit remains relevant

Adding m(chi1+) > 103 GeV removed ~24% of pre-LEP models (600→458), eliminating ultra-light Wino and Higgsino scenarios. Even 20+ years after LEP, this constraint shapes the viable parameter space.

---

## Run 3 Search Recommendations

Based on these findings, the following LHC Run 3 search strategies would have maximum impact on the pMSSM:

1. **Disappearing charged tracks** — Wino-like compressed models (359 surviving) predict tracks of ~5-20 cm from the slightly heavier chargino. This is the single most common signature.

2. **Soft lepton + MET** — Higgsino compressed models with dm ~ 1-30 GeV produce soft opposite-sign leptons from chi20→chi10 + Z* decays.

3. **Slepton pair production** — 259 models have selectrons/smuons below 600 GeV, giving clean dilepton + MET signatures. The lightest benchmark has m(eL)=162 GeV.

4. **Light stop in compressed corridor** — 7 models with dm(stop,LSP) < 200 GeV are invisible to conventional stop searches. Charm-tagging (for stop→c+chi10) and monojet (for stop→t*+chi10 → bW*+chi10) are needed.

5. **Heavy Higgs ditau resonance** — 60 models have mH or mA below 1 TeV with large tanβ, making H/A→ττ a viable discovery channel.

6. **Direct sbottom production** — The Light_sbottom benchmark (m(b1)=295 GeV, SModelS r=0.751) is already at 75% of the exclusion boundary, suggesting Run 3 data may probe this region.

---

## File Inventory

| Path | Description |
|------|-------------|
| `results/benchmarks/*.slha` | 9 benchmark SLHA spectra (one per category) |
| `results/benchmarks/benchmark_summary.csv` | Benchmark properties in CSV format |
| `results/plots/final_*.png` | Summary plots (chargino vs LSP, stop vs LSP, categories) |
| `analysis/final_classification.py` | Classification and cutflow script |
| `analysis/extract_benchmarks.py` | Benchmark extraction script |
| `docs/INVESTIGATION_PLAN.md` | Full investigation plan with methodology |
| `docs/SCAN_LOG.md` | Complete log of all scans performed |
| `docs/ANALYSIS_NOTES.md` | Detailed physics observations per phase |
| `docs/PHYSICS_CATEGORIES.md` | Category definitions and cut thresholds |
| `docs/NTUPLE_VARIABLES.md` | ROOT ntuple branch reference |
| `configs/phase*.yaml` | All scan configuration files |
| `scans/phase*/scan_seed*/ntuple.*.root` | Raw ntuple data |
| `run_scans.py` | Parallel scan launcher |
| `run_ntupling.py` | Post-hoc ntuple generation |

---

## Limitations and Future Work

1. **Sampling bias:** MCMC scans favor regions easily navigable by the chain. Narrow corridors (Bino co-annihilation, compressed stop) require alternative methods (grid scans, nested sampling, or neural network-guided importance sampling).

2. **Stau decoupled:** Stau masses are fixed at 2 TeV in all scans. Allowing light staus would open stau co-annihilation channels for Bino dark matter and add stau pair production as a search target.

3. **1st/2nd gen squarks decoupled:** Fixed at 4 TeV. While well-motivated by LHC exclusions, some compressed scenarios (e.g., light squark near the LSP) could evade current limits.

4. **No CP violation:** The pMSSM framework assumes no new CP-violating phases. Relaxing this would add parameters but enable new phenomenology (EDMs, CP-violating Higgs sector).

5. **SModelS coverage:** The SModelS database covers only simplified-model topologies published by ATLAS and CMS. Full recasting of analyses (using tools like CheckMATE or MadAnalysis) would provide more accurate exclusion constraints.

6. **Statistics:** 458 surviving models is sufficient for identifying categories and benchmarks but insufficient for robust probability statements about the pMSSM. A full profile likelihood analysis would require O(10^6) models.
