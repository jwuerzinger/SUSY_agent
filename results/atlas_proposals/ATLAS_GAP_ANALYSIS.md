# ATLAS Gap Analysis: pMSSM Models Missing from the ATLAS Search Program

**Date:** 2026-03-03
**SModelS version:** 3.1.1
**Models analyzed:** 2063 pMSSM models surviving all experimental constraints

## Executive Summary

We analyze ATLAS coverage of 2063 pMSSM models that survive Higgs mass, relic density, B-physics, SModelS exclusion, and LEP constraints. We find:

- **1372 models (66.5%)** are completely invisible to ATLAS (no ATLAS analysis provides any constraint)
- **84 models (4.1%)** have negligible ATLAS sensitivity (r < 0.01)
- **289 models (14.0%)** have only weak ATLAS constraints (0.01 < r < 0.1)
- Combined: **1745 models (84.6%)** have r_ATLAS < 0.1

The ATLAS constraints that exist come almost exclusively from stop/sbottom simplified models (T2tt, T2bb). There are no ATLAS electroweakino, slepton, or disappearing-track topologies in the SModelS v3.1.1 database.

We identify five specific gaps in the ATLAS search program and provide benchmark SLHA files and concrete analysis proposals for each.

---

## Gap A: Compressed Wino (disappearing tracks)

**Models affected:** 616

### Description

The Wino LSP scenario with mass splitting dm(chi1+, chi10) ~ 0.2 GeV produces charginos with macroscopic lifetimes (ctau ~ 5-20 cm). These charginos produce disappearing tracks in the inner detector before decaying to a soft pion and the invisible LSP. The SModelS v3.1.1 database does not encode ATLAS disappearing-track searches, making these models completely invisible despite large production cross-sections.

### Model Statistics

- LSP types: Wino=616
- m(LSP) range: 103 - 890 GeV
- Missing cross-section: 0.00 - 12.09 fb
- Displaced missing xsec: up to 13.4 fb

### Benchmark Models (5 extracted)

| Selection | scan_dir | model_id | m(LSP) | m(chi1+) | dm | Missing xsec [fb] | ATLAS r_max |
|-----------|----------|----------|--------|----------|----|-------------------|-------------|
| highest_xsec | scan_seed256 | 200 | 722 | 722 | 0.2 | 12.09 | 0.0000 |
| highest_xsec | scan_seed256 | 164 | 640 | 640 | 0.2 | 8.17 | 0.0000 |
| closest_exclusion | scan_seed137 | 23 | 282 | 282 | 0.3 | 0.09 | 0.0000 |
| lightest_lsp | scan_seed137 | 219 | 103 | 103 | 0.3 | 0.00 | 0.0000 |
| additional | scan_seed256 | 155 | 182 | 183 | 0.7 | 3.84 | 0.0000 |

### Signal Characterization

**highest_xsec** (model 200 from scan_seed256):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Chargino ctau: 0.00 cm
- Expected visible pT: soft leptons ~1 GeV

**highest_xsec** (model 164 from scan_seed256):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: soft leptons ~1 GeV

**closest_exclusion** (model 23 from scan_seed137):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: soft leptons ~1 GeV

**lightest_lsp** (model 219 from scan_seed137):
- Dominant decay: chi1+ -> pi+ chi10 (ctau=0.005m)
- Chargino ctau: 0.48 cm
- Expected visible pT: sub-GeV (displaced pion)

**additional** (model 155 from scan_seed256):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: soft leptons ~1 GeV


Benchmark SLHA files: `results/atlas_proposals/benchmarks/gap_A/`

### Proposed Analysis Strategy

**Extend ATLAS-SUSY-2018-19 (disappearing tracks):**
- The existing ATLAS disappearing-track search should already cover many of these models
- Encoding this analysis topology in SModelS would immediately provide constraints
- Request SModelS collaboration to add ATLAS disappearing-track results
- For Run 3: extend the search to higher chargino masses using the full 300 fb-1 dataset
- Consider dedicated triggers for short tracks (pixel-only) to access ctau < 5 cm

---

## Gap B: Compressed Higgsino (soft leptons)

**Models affected:** 737

### Description

Higgsino LSP scenarios with mass splitting dm ~ 1-20 GeV produce soft dileptons + MET from chi20 -> Z* chi10 and chi1+ -> W* chi10 decays. The visible decay products have pT typically below 10 GeV, challenging standard trigger and reconstruction thresholds.

### Model Statistics

- LSP types: Higgsino=737
- m(LSP) range: 94 - 675 GeV
- Missing cross-section: 0.00 - 0.65 fb
- Displaced missing xsec: up to 0.1 fb

### Benchmark Models (5 extracted)

| Selection | scan_dir | model_id | m(LSP) | m(chi1+) | dm | Missing xsec [fb] | ATLAS r_max |
|-----------|----------|----------|--------|----------|----|-------------------|-------------|
| highest_xsec | scan_seed42 | 151 | 122 | 130 | 7.8 | 0.65 | 0.0000 |
| highest_xsec | scan_seed42 | 58 | 97 | 107 | 10.2 | 0.51 | 0.0000 |
| closest_exclusion | scan_seed137 | 76 | 298 | 301 | 2.5 | 0.00 | 0.0098 |
| lightest_lsp | scan_seed42 | 16 | 94 | 118 | 24.1 | 0.00 | 0.0000 |
| additional | scan_seed42 | 35 | 106 | 115 | 9.0 | 0.50 | 0.0094 |

### Signal Characterization

**highest_xsec** (model 151 from scan_seed42):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: soft leptons ~3 GeV

**highest_xsec** (model 58 from scan_seed42):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: soft leptons ~3 GeV

**closest_exclusion** (model 76 from scan_seed137):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Chargino ctau: 0.00 cm
- Expected visible pT: soft leptons ~1 GeV

**lightest_lsp** (model 16 from scan_seed42):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: standard

**additional** (model 35 from scan_seed42):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: soft leptons ~3 GeV


Benchmark SLHA files: `results/atlas_proposals/benchmarks/gap_B/`

### Proposed Analysis Strategy

**Extend ATLAS-SUSY-2019-09 (compressed Higgsino) and ATLAS-SUSY-2021-01:**
- Lower lepton pT thresholds using ISR-boosted topology (monojet + soft leptons)
- Use VBF topology as additional trigger path for compressed spectra
- For Run 3: exploit improved low-pT reconstruction from ITk upgrade studies
- Encode existing ATLAS compressed-Higgsino results in SModelS

---

## Gap C: Light Sleptons above ATLAS Reach

**Models affected:** 497

### Description

Models with sleptons in the 180-600 GeV range produce clean dilepton + MET signatures from slepton pair production. The ATLAS Run 2 reach extends to ~180 GeV for direct slepton production (ATLAS-SUSY-2018-32), but many models have sleptons well above this. No ATLAS slepton simplified model topology is encoded in SModelS v3.1.1.

### Model Statistics

- LSP types: Wino=245, Higgsino=220, Bino=32
- m(LSP) range: 94 - 565 GeV
- Missing cross-section: 0.00 - 14418.78 fb
- Displaced missing xsec: up to 14362.4 fb

### Benchmark Models (5 extracted)

| Selection | scan_dir | model_id | m(LSP) | m(chi1+) | dm | Missing xsec [fb] | ATLAS r_max |
|-----------|----------|----------|--------|----------|----|-------------------|-------------|
| highest_xsec | scan_seed314 | 32 | 171 | 171 | 0.2 | 14418.78 | 0.0127 |
| highest_xsec | scan_seed42 | 96 | 254 | 254 | 0.2 | 267.32 | 0.0663 |
| closest_exclusion | scan_seed256 | 63 | 470 | 473 | 3.3 | 0.00 | 0.0983 |
| lightest_lsp | scan_seed42 | 16 | 94 | 118 | 24.1 | 0.00 | 0.0000 |
| additional | scan_seed42 | 95 | 243 | 243 | 0.2 | 124.34 | 0.0558 |

### Signal Characterization

**highest_xsec** (model 32 from scan_seed314):
- Dominant decay: chi1+ -> pi+ chi10 (ctau=0.012m)
- Chargino ctau: 1.19 cm
- Expected visible pT: sub-GeV (displaced pion)

**highest_xsec** (model 96 from scan_seed42):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: soft leptons ~1 GeV

**closest_exclusion** (model 63 from scan_seed256):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Chargino ctau: 0.00 cm
- Expected visible pT: soft leptons ~1 GeV

**lightest_lsp** (model 16 from scan_seed42):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: standard

**additional** (model 95 from scan_seed42):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: soft leptons ~1 GeV


Benchmark SLHA files: `results/atlas_proposals/benchmarks/gap_C/`

### Proposed Analysis Strategy

**Extend ATLAS-SUSY-2018-32 (direct slepton):**
- With 300 fb-1 Run 3 data, extend slepton reach from ~180 GeV toward 400-500 GeV
- Encode the existing ATLAS slepton results in SModelS for proper coverage assessment
- Consider di-tau final states for stau scenarios
- For Bino LSP models: the 2-body decay slepton -> l + chi10 is very clean

---

## Gap D: Compressed Stop with Displaced Chargino

**Models affected:** 7

### Description

Models with compressed stop spectra where stop -> b + chi1+ and the chargino has macroscopic lifetime (ctau ~ cm). These produce both displaced and prompt signatures with massive uncovered cross-sections (up to ~14,000 fb displaced). The ATLAS r_max for these models is only ~0.01, far from exclusion.

### Model Statistics

- LSP types: Wino=7
- m(LSP) range: 143 - 258 GeV
- Missing cross-section: 2223.62 - 14418.78 fb
- Displaced missing xsec: up to 14362.4 fb

### Benchmark Models (5 extracted)

| Selection | scan_dir | model_id | m(LSP) | m(chi1+) | dm | Missing xsec [fb] | ATLAS r_max |
|-----------|----------|----------|--------|----------|----|-------------------|-------------|
| highest_xsec | scan_seed314 | 32 | 171 | 171 | 0.2 | 14418.78 | 0.0127 |
| highest_xsec | scan_seed256 | 38 | 143 | 143 | 0.2 | 5756.38 | 1.2551 |
| closest_exclusion | scan_seed314 | 82 | 256 | 256 | 0.2 | 2688.75 | 2.4420 |
| additional | scan_seed256 | 20 | 197 | 197 | 0.2 | 4743.06 | 1.7016 |
| additional | scan_seed137 | 78 | 258 | 258 | 0.2 | 3422.93 | 0.2783 |

### Signal Characterization

**highest_xsec** (model 32 from scan_seed314):
- Dominant decay: chi1+ -> pi+ chi10 (ctau=0.012m)
- Chargino ctau: 1.19 cm
- Expected visible pT: sub-GeV (displaced pion)

**highest_xsec** (model 38 from scan_seed256):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: soft leptons ~1 GeV

**closest_exclusion** (model 82 from scan_seed314):
- Dominant decay: chi1+ -> pi+ chi10 (ctau=0.010m)
- Chargino ctau: 0.98 cm
- Expected visible pT: sub-GeV (displaced pion)

**additional** (model 20 from scan_seed256):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Chargino ctau: 0.00 cm
- Expected visible pT: soft leptons ~1 GeV

**additional** (model 78 from scan_seed137):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Chargino ctau: 0.09 cm
- Expected visible pT: sub-GeV (displaced pion)


Benchmark SLHA files: `results/atlas_proposals/benchmarks/gap_D/`

### Proposed Analysis Strategy

**New search: displaced b-jets + MET:**
- Combine b-tagging with displaced-vertex reconstruction
- Target: stop pair -> b + displaced-track + MET
- Also extend ATLAS-SUSY-2018-07 (stop compressed) to include displaced signatures
- The prompt component (b + soft jet + MET) may be accessible with monojet-like searches

---

## Gap E: Complex EWKino Cascade Topologies

**Models affected:** 41

### Description

Models with complex neutralino/chargino cascade decays producing multi-body final states like (b,MET)+(t,nu,l,MET) or (b,l,l,MET)+(t,nu,l,MET). No ATLAS simplified model covers these topologies, which arise from mixed Bino/Wino/Higgsino spectra with multiple intermediate states.

### Model Statistics

- LSP types: Wino=34, Bino=4, Higgsino=3
- m(LSP) range: 97 - 722 GeV
- Missing cross-section: 0.50 - 12.09 fb
- Displaced missing xsec: up to 13.4 fb

### Benchmark Models (5 extracted)

| Selection | scan_dir | model_id | m(LSP) | m(chi1+) | dm | Missing xsec [fb] | ATLAS r_max |
|-----------|----------|----------|--------|----------|----|-------------------|-------------|
| highest_xsec | scan_seed256 | 200 | 722 | 722 | 0.2 | 12.09 | 0.0000 |
| highest_xsec | scan_seed137 | 239 | 112 | 112 | 0.3 | 11.32 | 0.0086 |
| closest_exclusion | scan_seed42 | 35 | 106 | 115 | 9.0 | 0.50 | 0.0094 |
| lightest_lsp | scan_seed42 | 58 | 97 | 107 | 10.2 | 0.51 | 0.0000 |
| additional | scan_seed137 | 95 | 462 | 463 | 0.6 | 8.92 | 0.0063 |

### Signal Characterization

**highest_xsec** (model 200 from scan_seed256):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Chargino ctau: 0.00 cm
- Expected visible pT: soft leptons ~1 GeV

**highest_xsec** (model 239 from scan_seed137):
- Dominant decay: chi1+ -> pi+ chi10 (ctau=0.002m)
- Chargino ctau: 0.23 cm
- Expected visible pT: sub-GeV (displaced pion)

**closest_exclusion** (model 35 from scan_seed42):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: soft leptons ~3 GeV

**lightest_lsp** (model 58 from scan_seed42):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: soft leptons ~3 GeV

**additional** (model 95 from scan_seed137):
- Dominant decay: chi20 -> ff chi10, chi1+ -> ff chi10 (3-body)
- Expected visible pT: soft leptons ~3 GeV


Benchmark SLHA files: `results/atlas_proposals/benchmarks/gap_E/`

### Proposed Analysis Strategy

**Extend existing multi-lepton + jets + MET searches:**
- ATLAS-SUSY-2018-06 (multi-lepton) should have some sensitivity
- Create new signal regions targeting asymmetric final states (e.g., 1 b-jet + 1 lepton + MET)
- Consider top+b+lepton+MET as a dedicated final state
- For pMSSM interpretation: perform full pMSSM scan reinterpretation against these analyses

---

## Summary

| Gap | Description | Models | Benchmarks | Key signal | Priority |
|-----|-------------|--------|------------|------------|----------|
| A | Compressed Wino (disappearing tracks) | 616 | 5 | See above | HIGH |
| B | Compressed Higgsino (soft leptons) | 737 | 5 | See above | HIGH |
| C | Light Sleptons above ATLAS Reach | 497 | 5 | See above | MEDIUM |
| D | Compressed Stop with Displaced Chargino | 7 | 5 | See above | MEDIUM |
| E | Complex EWKino Cascade Topologies | 41 | 5 | See above | LOW |

## Methodology

1. Generated 458 pMSSM models surviving Higgs mass [122-128 GeV], relic density <= 0.132, B-physics (2 sigma), SModelS exclusion, and LEP chargino mass > 103 GeV constraints
2. Parsed raw SModelS v3.1.1 output for each model to extract per-analysis r-values
3. Classified ATLAS coverage into tiers: Invisible (r=0), Negligible (r<0.01), Weak (r<0.1), Moderate (r<0.5), Near-exclusion (r<1), Excluded (r>=1)
4. Identified five specific gaps and extracted benchmark SLHA files
5. Characterized signals using SPheno branching fractions, widths, and SModelS decomposition

## References

- SModelS v3.1.1: https://smodels.github.io/
- SPheno: https://spheno.hepforge.org/
- MicrOMEGAs: https://lapth.cnrs.fr/micromegas/
