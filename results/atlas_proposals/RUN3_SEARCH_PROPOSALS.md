# Run 3 ATLAS Search Proposals for pMSSM Blind Spots

**Date:** 2026-03-04
**Models analyzed:** 2063
**Run 3 luminosity assumed:** 300 fb$^{-1}$
**SModelS version:** 3.1.1

## 1. Executive Summary

We analyze 2063 pMSSM models surviving all experimental constraints and identify five ATLAS blind spots containing a total of 1842 models that are invisible or poorly constrained.

For each blind spot, we provide:
- Concrete signal region definitions based on existing/extended ATLAS searches
- Estimated signal yields at 300 fb$^{-1}$
- Mass-grid benchmark SLHA files for Monte Carlo production
- Direct detection complementarity assessment

**Key finding:** 3 models are invisible to both ATLAS and projected direct detection experiments (below DARWIN sensitivity) — these can only be probed at the LHC with dedicated searches.

**Important caveat:** The ATLAS coverage assessment uses SModelS v3.1.1, which does not encode ATLAS disappearing-track (SUSY-2018-19), direct slepton (SUSY-2018-32), or compressed Higgsino (SUSY-2019-09) searches. Many Gap A/B/C models may already be constrained by these existing analyses. The proposals below focus on Run 3 extensions beyond the current reach.

| Gap | Description | Models | Excludable (N>3) | Discoverable (N>10) | Priority |
|-----|-------------|--------|------------------|---------------------|----------|
| A | Compressed Wino | 526 | 103 | 73 | HIGH |
| B | Compressed Higgsino | 737 | 34 | 11 | HIGH |
| C | Light Sleptons | 497 | 145 | 108 | MEDIUM |
| D | Compressed Stop | 2 | 2 | 2 | MEDIUM |
| E | Complex EWKino | 80 | 21 | 12 | LOW |

---

## 2. Dataset and Methodology

### pMSSM Model Generation

Models are generated using the Run3ModelGen framework with:
- SPheno 4.0.5 for spectrum calculation
- MicrOMEGAs 5.2.1 for relic density and direct detection
- SuperIso for B-physics observables
- SModelS 3.1.1 for LHC reinterpretation

### Selection Cuts

| Cut | Value |
|-----|-------|
| Higgs mass | 122 < m_h < 128 GeV |
| Relic density | Omega h^2 <= 0.132 |
| BR(b -> s gamma) | within 2 sigma of 3.32e-4 |
| BR(Bs -> mu mu) | within 2 sigma of 3.09e-9 |
| SModelS | not excluded |
| LEP chargino | m(chi1+) > 103 GeV |

### Signal Yield Estimation

Cross-sections are scaled from 13 TeV to 13.6 TeV using a flat k-factor of 1.15, appropriate for electroweak production at these energies. Signal yields are estimated as:

$$N_{\mathrm{signal}} = \sigma_{13.6} \times L \times \epsilon_{\mathrm{acceptance}}$$

where acceptance factors are estimated from published ATLAS efficiency maps.

## 3. Gap A: Compressed Wino — Disappearing Track Search

**Models affected:** 526
**Reference analysis:** ATLAS-SUSY-2018-19

### Model Population

| Property | Value |
|----------|-------|
| LSP composition | Wino=526 |
| m(LSP) range | 103 - 890 GeV |
| Median dm(chi1+, chi10) | 1.9 GeV |
| Models with N_sig > 3 at 300/fb | 103 |
| Models with N_sig > 10 at 300/fb | 73 |

### Signal Topology

**Process:** pp -> chi1+ chi10 + ISR jet, chi1+ -> pi+ chi10 (displaced)

### Proposed Signal Regions

**Trigger:** MET > 200 GeV (ISR recoil)

**Event selection:**
- Leading jet pT > 140 GeV, |eta| < 2.8
- MET > 200 GeV
- Pixel tracklet: >= 4 pixel hits, no SCT extension
- Tracklet pT > 20 GeV, |eta| < 2.1
- Tracklet isolation: no tracks within dR < 0.4
- Veto on identified leptons

**Key discriminant:** Tracklet length vs chargino ctau

**Dominant backgrounds:** Fake tracklets from random hits, hadron interactions

| Signal Region | Definition | Expected Background |
|---------------|------------|---------------------|
| SR-Pixel-Short | tracklet length 12-22 cm | ~5 events |
| SR-Pixel-Long | tracklet length 22-50 cm | ~1 event |

**Run 3 advantage:** Improved ITk pixel detector with lower material budget; extended pixel coverage to |eta| < 4; dedicated disappearing-track trigger at L1

### Benchmark Models and Yield Estimates

| Tag | scan_dir | model_id | m(LSP) | m(chi1+) | dm | sigma_13.6 [fb] | N_sig (300/fb) | ATLAS r |
|-----|----------|----------|--------|----------|----|----------------|----------------|----------|
| highest_xsec | scan_seed137 | 19 | 404 | 404 | 2.6 | 56.63 | 849.5 | 0.0000 |
| highest_xsec | scan_seed137 | 13 | 227 | 228 | 2.5 | 47.75 | 716.3 | 0.0000 |
| closest_exclusion | scan_seed42 | 99 | 266 | 266 | 4.4 | 4.26 | 63.8 | 0.0099 |
| lightest_lsp | scan_seed137 | 219 | 103 | 103 | 0.3 | 0.00 | 0.0 | 0.0000 |
| mass_grid_299 | scan_seed137 | 179 | 300 | 300 | 0.9 | 0.00 | 0.0 | 0.0000 |
| mass_grid_496 | scan_seed256 | 128 | 496 | 496 | 2.6 | 0.00 | 0.0 | 0.0000 |
| mass_grid_693 | scan_seed256 | 64 | 693 | 693 | 2.1 | 0.42 | 6.3 | 0.0000 |

### Plots

- `plots/gap_A_mass_splitting_dist.png`
- `plots/gap_A_xsec_vs_mass.png`
- `plots/gap_A_signal_yields.png`
- `plots/gap_A_kinematic_reach.png`

---

## 4. Gap B: Compressed Higgsino — Soft Lepton Search

**Models affected:** 737
**Reference analysis:** ATLAS-SUSY-2019-09

### Model Population

| Property | Value |
|----------|-------|
| LSP composition | Higgsino=737 |
| m(LSP) range | 94 - 675 GeV |
| Median dm(chi1+, chi10) | 3.0 GeV |
| Models with N_sig > 3 at 300/fb | 34 |
| Models with N_sig > 10 at 300/fb | 11 |

### Signal Topology

**Process:** pp -> chi20 chi1+ + ISR jet, chi20 -> Z* chi10, chi1+ -> W* chi10

### Proposed Signal Regions

**Trigger:** MET > 200 GeV (ISR-boosted)

**Event selection:**
- Leading jet pT > 100 GeV, |eta| < 2.4
- MET > 200 GeV
- Opposite-sign same-flavor dileptons
- pT(l1) > 5 GeV, pT(l2) > 4.5 GeV
- mll < 40 GeV (below Z)
- mT2 < 80 GeV
- dphi(jet1, MET) > 2.0

**Key discriminant:** mll binned: [1-3], [3-5], [5-10], [10-20], [20-40] GeV

**Dominant backgrounds:** Drell-Yan + jets, top-pair (dominant), diboson

| Signal Region | Definition | Expected Background |
|---------------|------------|---------------------|
| SR-E-mll_1_3 | 1 < mll < 3 GeV, ee channel | ~15 events |
| SR-E-mll_3_5 | 3 < mll < 5 GeV, ee channel | ~20 events |
| SR-E-mll_5_10 | 5 < mll < 10 GeV, ee channel | ~30 events |
| SR-Mu-mll_1_3 | 1 < mll < 3 GeV, mumu channel | ~10 events |

**Run 3 advantage:** Improved low-pT electron reconstruction from ITk; L1 topological triggers for soft leptons; 300 fb^-1 statistics

### Benchmark Models and Yield Estimates

| Tag | scan_dir | model_id | m(LSP) | m(chi1+) | dm | sigma_13.6 [fb] | N_sig (300/fb) | ATLAS r |
|-----|----------|----------|--------|----------|----|----------------|----------------|----------|
| highest_xsec | scan_seed256 | 131 | 352 | 354 | 3.5 | 13.06 | 78.4 | 0.0000 |
| highest_xsec | scan_seed137 | 17 | 358 | 359 | 10.9 | 9.37 | 56.2 | 0.0000 |
| closest_exclusion | scan_seed137 | 76 | 298 | 301 | 2.5 | 0.13 | 0.8 | 0.0098 |
| lightest_lsp | scan_seed42 | 16 | 94 | 118 | 24.1 | 0.00 | 0.0 | 0.0000 |
| mass_grid_239 | scan_seed256 | 247 | 239 | 241 | 2.3 | 0.00 | 0.0 | 0.0000 |
| mass_grid_384 | scan_seed137 | 316 | 384 | 387 | 3.0 | 0.00 | 0.0 | 0.0000 |
| mass_grid_529 | scan_seed137 | 244 | 533 | 535 | 1.7 | 0.00 | 0.0 | 0.0000 |

### Plots

- `plots/gap_B_mass_splitting_dist.png`
- `plots/gap_B_xsec_vs_mass.png`
- `plots/gap_B_signal_yields.png`
- `plots/gap_B_kinematic_reach.png`

---

## 5. Gap C: Light Sleptons — Extended Dilepton + MET Search

**Models affected:** 497
**Reference analysis:** ATLAS-SUSY-2018-32

### Model Population

| Property | Value |
|----------|-------|
| LSP composition | Bino=32, Wino=245, Higgsino=220 |
| m(LSP) range | 94 - 565 GeV |
| Median dm(chi1+, chi10) | 3.4 GeV |
| Models with N_sig > 3 at 300/fb | 145 |
| Models with N_sig > 10 at 300/fb | 108 |

### Signal Topology

**Process:** pp -> slep slep -> l+ l- + chi10 chi10

### Proposed Signal Regions

**Trigger:** Dilepton trigger (pT > 25/15 GeV)

**Event selection:**
- Exactly 2 same-flavor opposite-sign leptons
- pT(l1) > 25 GeV, pT(l2) > 20 GeV
- MET > 110 GeV
- Jet veto: <= 1 jet with pT > 30 GeV
- mT2 > 100 GeV
- dphi(ll, MET) > 1.5

**Key discriminant:** mT2 binned: [100-120], [120-160], [160-inf] GeV

**Dominant backgrounds:** Diboson WW/ZZ (dominant), top-pair, Drell-Yan

| Signal Region | Definition | Expected Background |
|---------------|------------|---------------------|
| SR-mT2-100 | 100 < mT2 < 120 GeV | ~50 events |
| SR-mT2-120 | 120 < mT2 < 160 GeV | ~20 events |
| SR-mT2-160 | mT2 > 160 GeV | ~5 events |

**Run 3 advantage:** With 300 fb^-1, slepton reach extends from ~180 GeV to ~400-500 GeV; improved lepton efficiency at high pT

### Benchmark Models and Yield Estimates

| Tag | scan_dir | model_id | m(LSP) | m(chi1+) | dm | sigma_13.6 [fb] | N_sig (300/fb) | ATLAS r |
|-----|----------|----------|--------|----------|----|----------------|----------------|----------|
| highest_xsec | scan_seed137 | 13 | 224 | 224 | 2.5 | 47.75 | 2148.8 | 0.0475 |
| highest_xsec | scan_seed42 | 198 | 190 | 190 | 4.7 | 28.62 | 1287.7 | 0.0000 |
| closest_exclusion | scan_seed256 | 63 | 470 | 473 | 3.3 | 1.64 | 73.8 | 0.0983 |
| lightest_lsp | scan_seed42 | 16 | 94 | 118 | 24.1 | 0.00 | 0.0 | 0.0000 |
| mass_grid_212 | scan_seed42 | 104 | 212 | 212 | 5.6 | 0.23 | 10.3 | 0.0078 |
| mass_grid_329 | scan_seed42 | 41 | 330 | 330 | 2.9 | 0.06 | 2.8 | 0.0000 |
| mass_grid_447 | scan_seed42 | 177 | 447 | 447 | 0.2 | 0.00 | 0.0 | 0.0000 |

### Plots

- `plots/gap_C_mass_splitting_dist.png`
- `plots/gap_C_xsec_vs_mass.png`
- `plots/gap_C_signal_yields.png`
- `plots/gap_C_kinematic_reach.png`

---

## 6. Gap D: Compressed Stop — Displaced Vertex + b-jet Search

**Models affected:** 2
**Reference analysis:** Novel (combines ATLAS-SUSY-2018-07 + displaced-vertex)

### Model Population

| Property | Value |
|----------|-------|
| LSP composition | Wino=2 |
| m(LSP) range | 171 - 256 GeV |
| Median dm(chi1+, chi10) | 0.2 GeV |
| Models with N_sig > 3 at 300/fb | 2 |
| Models with N_sig > 10 at 300/fb | 2 |

### Signal Topology

**Process:** pp -> stop stop -> b chi1+ b chi1+ -> b (displaced pi) MET + b (displaced pi) MET

### Proposed Signal Regions

**Trigger:** MET > 250 GeV

**Event selection:**
- >= 1 b-jet (pT > 30 GeV, |eta| < 2.5)
- MET > 250 GeV
- Displaced vertex: transverse displacement 1-30 cm
- Vertex mass > 5 GeV
- OR prompt channel: >= 2 b-jets + MET > 300 GeV, mT(b,MET) < 200 GeV

**Key discriminant:** Displaced vertex displacement + vertex mass

**Dominant backgrounds:** Heavy-flavor jets with displaced vertices, beam halo, cosmic rays

| Signal Region | Definition | Expected Background |
|---------------|------------|---------------------|
| SR-DV-1cm | vertex displacement 1-5 cm | ~3 events |
| SR-DV-5cm | vertex displacement 5-30 cm | ~0.5 events |
| SR-Prompt | 2 b-jets + MET > 300 GeV (prompt) | ~100 events |

**Run 3 advantage:** Improved tracking for displaced vertices; dedicated displaced-vertex triggers in Run 3; b-tagging improvements from ITk

### Benchmark Models and Yield Estimates

| Tag | scan_dir | model_id | m(LSP) | m(chi1+) | dm | sigma_13.6 [fb] | N_sig (300/fb) | ATLAS r |
|-----|----------|----------|--------|----------|----|----------------|----------------|----------|
| highest_xsec | scan_seed314 | 82 | 256 | 256 | 0.2 | 9654.06 | 86886.6 | 2.4420 |
| highest_xsec | scan_seed314 | 32 | 171 | 171 | 0.2 | 4.60 | 41.4 | 0.0127 |

### Plots

- `plots/gap_D_mass_splitting_dist.png`
- `plots/gap_D_xsec_vs_mass.png`
- `plots/gap_D_signal_yields.png`
- `plots/gap_D_kinematic_reach.png`

---

## 7. Gap E: Complex EWKino — Multi-Lepton Cascade Search

**Models affected:** 80
**Reference analysis:** ATLAS-SUSY-2018-06 (extension)

### Model Population

| Property | Value |
|----------|-------|
| LSP composition | Bino=2, Wino=77, Higgsino=1 |
| m(LSP) range | 104 - 467 GeV |
| Median dm(chi1+, chi10) | 2.9 GeV |
| Models with N_sig > 3 at 300/fb | 21 |
| Models with N_sig > 10 at 300/fb | 12 |

### Signal Topology

**Process:** pp -> chi_i chi_j -> multi-body cascades with W/Z/h + MET

### Proposed Signal Regions

**Trigger:** Multi-lepton trigger (>= 2 leptons) or MET > 200 GeV

**Event selection:**
- >= 3 leptons (or 2 leptons + 1 b-jet) + MET > 100 GeV
- pT(l1) > 25 GeV, pT(l2) > 20 GeV, pT(l3) > 10 GeV
- Veto on Z-boson (|mll - mZ| > 15 GeV for OSSF pairs)
- OR: 2 leptons + >= 1 b-jet + MET > 150 GeV

**Key discriminant:** meff (scalar sum of lepton pT, jet pT, MET)

**Dominant backgrounds:** Diboson WZ/ZZ, ttbar+V, tribosons

| Signal Region | Definition | Expected Background |
|---------------|------------|---------------------|
| SR-3L-low | >= 3 leptons, meff < 400 GeV | ~20 events |
| SR-3L-high | >= 3 leptons, meff > 400 GeV | ~5 events |
| SR-2Lb | 2 leptons + b-jet + MET > 150 | ~30 events |

**Run 3 advantage:** Higher statistics for rare multi-lepton final states; improved lepton ID and b-tagging; dedicated asymmetric decay channel signal regions

### Benchmark Models and Yield Estimates

| Tag | scan_dir | model_id | m(LSP) | m(chi1+) | dm | sigma_13.6 [fb] | N_sig (300/fb) | ATLAS r |
|-----|----------|----------|--------|----------|----|----------------|----------------|----------|
| highest_xsec | scan_seed42 | 101 | 250 | 251 | 4.8 | 13.38 | 200.7 | 0.0081 |
| highest_xsec | scan_seed42 | 100 | 277 | 277 | 4.5 | 6.97 | 104.5 | 0.0092 |
| closest_exclusion | scan_seed137 | 122 | 199 | 199 | 28.8 | 0.00 | 0.0 | 0.0100 |
| lightest_lsp | scan_seed42 | 216 | 104 | 104 | 1.6 | 0.00 | 0.0 | 0.0087 |
| mass_grid_194 | scan_seed137 | 147 | 195 | 195 | 0.8 | 0.04 | 0.5 | 0.0000 |
| mass_grid_285 | scan_seed256 | 152 | 279 | 280 | 3.5 | 0.06 | 0.9 | 0.0085 |
| mass_grid_376 | scan_seed42 | 98 | 366 | 366 | 4.1 | 6.55 | 98.2 | 0.0037 |

### Plots

- `plots/gap_E_mass_splitting_dist.png`
- `plots/gap_E_xsec_vs_mass.png`
- `plots/gap_E_signal_yields.png`
- `plots/gap_E_kinematic_reach.png`

---

## 8. Direct Detection Complementarity

We compare the spin-independent (SI) proton-neutralino cross-section with projected sensitivities of XENON-nT, LZ, and DARWIN.

- **3 models** are below DARWIN sensitivity AND invisible to ATLAS
- These "truly dark" models can only be probed at the LHC with dedicated searches
- Plot: `plots/dd_complementarity.png`

---

## 9. Summary and Recommendations

### Priority Actions for ATLAS

1. **Encode existing searches in SModelS:** Disappearing tracks (SUSY-2018-19), direct sleptons (SUSY-2018-32), and compressed Higgsino (SUSY-2019-09) results should be added to the SModelS database. This alone would dramatically improve coverage assessment for Gaps A, B, and C.

2. **Extend disappearing-track search (Gap A):** With 300 fb$^{-1}$ and ITk, extend the Wino mass reach from ~460 GeV (Run 2) toward 800+ GeV. 103 models are potentially excludable.

3. **Lower soft-lepton thresholds (Gap B):** ISR-boosted topology with improved low-pT lepton reconstruction. Target dm < 10 GeV region with mll binning down to 1 GeV.

4. **Extend slepton reach (Gap C):** With 300 fb$^{-1}$, the mT2-based search should reach selectron/smuon masses up to 400-500 GeV.

5. **Novel displaced + b-jet search (Gap D):** Combine displaced-vertex reconstruction with b-tagging for compressed stop scenarios. Small model count but very large uncovered cross-sections.

6. **Multi-lepton cascade search (Gap E):** Extend existing multi-lepton searches with asymmetric final-state signal regions.

## 10. Appendix: Benchmark SLHA File Index

Benchmark SLHA files are stored in `results/atlas_proposals/benchmarks/gap_X/`.

### Gap A

| Tag | File | m(LSP) | m(chi1+) |
|-----|------|--------|----------|
| highest_xsec | gapA_highest_xsec_scan_seed137_m19.slha | 404 | 404 |
| highest_xsec | gapA_highest_xsec_scan_seed137_m13.slha | 227 | 228 |
| closest_exclusion | gapA_closest_exclusion_scan_seed42_m99.slha | 266 | 266 |
| lightest_lsp | gapA_lightest_lsp_scan_seed137_m219.slha | 103 | 103 |
| mass_grid_299 | gapA_mass_grid_299_scan_seed137_m179.slha | 300 | 300 |
| mass_grid_496 | gapA_mass_grid_496_scan_seed256_m128.slha | 496 | 496 |
| mass_grid_693 | gapA_mass_grid_693_scan_seed256_m64.slha | 693 | 693 |

### Gap B

| Tag | File | m(LSP) | m(chi1+) |
|-----|------|--------|----------|
| highest_xsec | gapB_highest_xsec_scan_seed256_m131.slha | 352 | 354 |
| highest_xsec | gapB_highest_xsec_scan_seed137_m17.slha | 358 | 359 |
| closest_exclusion | gapB_closest_exclusion_scan_seed137_m76.slha | 298 | 301 |
| lightest_lsp | gapB_lightest_lsp_scan_seed42_m16.slha | 94 | 118 |
| mass_grid_239 | gapB_mass_grid_239_scan_seed256_m247.slha | 239 | 241 |
| mass_grid_384 | gapB_mass_grid_384_scan_seed137_m316.slha | 384 | 387 |
| mass_grid_529 | gapB_mass_grid_529_scan_seed137_m244.slha | 533 | 535 |

### Gap C

| Tag | File | m(LSP) | m(chi1+) |
|-----|------|--------|----------|
| highest_xsec | gapC_highest_xsec_scan_seed137_m13.slha | 224 | 224 |
| highest_xsec | gapC_highest_xsec_scan_seed42_m198.slha | 190 | 190 |
| closest_exclusion | gapC_closest_exclusion_scan_seed256_m63.slha | 470 | 473 |
| lightest_lsp | gapC_lightest_lsp_scan_seed42_m16.slha | 94 | 118 |
| mass_grid_212 | gapC_mass_grid_212_scan_seed42_m104.slha | 212 | 212 |
| mass_grid_329 | gapC_mass_grid_329_scan_seed42_m41.slha | 330 | 330 |
| mass_grid_447 | gapC_mass_grid_447_scan_seed42_m177.slha | 447 | 447 |

### Gap D

| Tag | File | m(LSP) | m(chi1+) |
|-----|------|--------|----------|
| highest_xsec | gapD_highest_xsec_scan_seed314_m82.slha | 256 | 256 |
| highest_xsec | gapD_highest_xsec_scan_seed314_m32.slha | 171 | 171 |

### Gap E

| Tag | File | m(LSP) | m(chi1+) |
|-----|------|--------|----------|
| highest_xsec | gapE_highest_xsec_scan_seed42_m101.slha | 250 | 251 |
| highest_xsec | gapE_highest_xsec_scan_seed42_m100.slha | 277 | 277 |
| closest_exclusion | gapE_closest_exclusion_scan_seed137_m122.slha | 199 | 199 |
| lightest_lsp | gapE_lightest_lsp_scan_seed42_m216.slha | 104 | 104 |
| mass_grid_194 | gapE_mass_grid_194_scan_seed137_m147.slha | 195 | 195 |
| mass_grid_285 | gapE_mass_grid_285_scan_seed256_m152.slha | 279 | 280 |
| mass_grid_376 | gapE_mass_grid_376_scan_seed42_m98.slha | 366 | 366 |

