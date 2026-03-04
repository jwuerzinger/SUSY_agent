# ATLAS Blind Spot Characterization Report

**Date:** 2026-03-03

## Executive Summary

Of 2087 surviving pMSSM models, **1372 (65.7%)** are completely invisible to ATLAS and **84** have only negligible ATLAS sensitivity (r < 0.01). We identify five specific gaps in the ATLAS search program:

---

## Gap A: Compressed Wino (dm ~ 0.2 GeV)

**616 models** with Wino LSP and zero ATLAS sensitivity.

- Mass splitting: 0.00 - 5.70 GeV
- m(LSP) range: 103 - 890 GeV
- Displaced missing xsec: 0.0 - 13.4 fb
- Signal: Wino pair production -> chi1+ with ctau ~ 5-20 cm -> displaced pion + MET
- Why ATLAS misses it: disappearing-track searches not in SModelS topology set
- Relevant ATLAS analysis: ATLAS-SUSY-2018-19 (disappearing tracks)

### Example models (top 5 by displaced xsec):

| scan_dir | model_id | m(LSP) | m(chi1+) | dm | displaced xsec [fb] | prompt xsec [fb] |
|----------|----------|--------|----------|----|---------------------|------------------|
| scan_seed256 | 200 | 722 | 722 | 0.20 | 13.4 | 0.7 |
| scan_seed256 | 164 | 640 | 640 | 0.20 | 8.2 | 0.2 |
| scan_seed256 | 62 | 185 | 186 | 0.20 | 2.9 | 0.1 |
| scan_seed256 | 81 | 258 | 258 | 0.20 | 2.6 | 0.2 |
| scan_seed137 | 58 | 116 | 116 | 0.20 | 2.0 | 0.0 |

---

## Gap B: Compressed Higgsino (dm ~ 1-20 GeV)

**737 models** with Higgsino LSP and ATLAS tier <= Negligible.

- Mass splitting: 0.5 - 33.9 GeV
- m(LSP) range: 94 - 675 GeV
- Signal: chi20 chi1+ -> chi10 + soft Z*/W* -> soft dileptons + MET
- Why ATLAS misses it: soft lepton pT below trigger/reconstruction thresholds
- Relevant analyses: ATLAS-SUSY-2019-09, ATLAS-SUSY-2021-01

### Example models:

| scan_dir | model_id | m(LSP) | m(chi1+) | dm | CMS r_max |
|----------|----------|--------|----------|----|----------|
| scan_seed137 | 202 | 482 | 482 | 0.5 | 0.0055 |
| scan_seed137 | 103 | 403 | 403 | 0.6 | 0.0129 |
| scan_seed137 | 134 | 494 | 495 | 0.6 | 0.0000 |
| scan_seed137 | 135 | 497 | 498 | 0.6 | 0.0000 |
| scan_seed137 | 155 | 494 | 494 | 0.6 | 0.0073 |

---

## Gap C: Light Sleptons 180-600 GeV

**509 models** with sleptons < 600 GeV and ATLAS tier <= Weak.

- Slepton mass range: 204 - 598 GeV
- LSP types: Bino=44, Wino=245, Higgsino=220
- Signal: slepton pair -> dilepton + MET (clean, low background)
- Why ATLAS misses it: no ATLAS slepton topology in SModelS v3.1.1
- ATLAS reach: ~180 GeV (ATLAS-SUSY-2018-32)


---

## Gap D: Compressed Stop with Displaced Chargino

**7 models** with compressed stop and > 1 fb displaced missing xsec.

- dm(stop,LSP) range: 97 - 199 GeV
- Displaced missing xsec: 2291.7 - 14362.4 fb
- Signal: stop pair -> b + chi1+ (displaced) -> b + soft-pion + chi10

### Example models (top 5 by displaced xsec):

| scan_dir | model_id | m(stop) | m(LSP) | dm | displaced [fb] | ATLAS r_max |
|----------|----------|---------|--------|----|----------------|-------------|
| scan_seed314 | 32 | 268 | 171 | 97 | 14362.4 | 0.0127 |
| scan_seed256 | 38 | 337 | 143 | 194 | 6235.5 | 1.2551 |
| scan_seed256 | 20 | 345 | 197 | 148 | 4997.2 | 1.7016 |
| scan_seed137 | 78 | 368 | 258 | 110 | 3413.9 | 0.2783 |
| scan_seed314 | 82 | 369 | 256 | 114 | 2637.9 | 2.4420 |

---

## Gap E: Complex EWKino Cascade Topologies

**41 models** with ATLAS tier <= Negligible and > 0.5 fb prompt missing xsec.

- These represent multi-body final states from chargino/neutralino cascades
- No ATLAS simplified model covers these topologies

### Most common missing topologies in these models:

| SMS | Count |
|-----|-------|
| `PV > (W,b,jet,MET),(W,b,jet,MET)` | 9 |
| `PV > (W,t,MET),(W,b,jet,MET)` | 8 |
| `PV > (t,jet,MET),(W,t,MET)` | 5 |
| `PV > (W,b,MET),(W,t,jet,MET)` | 4 |
| `PV > (W,b,jet,MET),(b,l,l,MET)` | 3 |
| `PV > (t,jet,jet,MET),(b,jet,jet,MET)` | 2 |
| `PV > (b,jet,jet,MET),(W,t,jet,jet,MET)` | 2 |
| `PV > (t,jet,MET),(W,b,jet,MET)` | 2 |
| `PV > (b,MET),(t,jet,jet,MET)` | 2 |
| `PV > (b,l,l,MET),(b,l,l,MET)` | 1 |

---

## Summary Table

| Gap | Description | Models | Key signal | Max missing xsec [fb] |
|-----|-------------|--------|------------|----------------------|
| A | Compressed Wino | 616 | Displaced pion + MET | 12.1 |
| B | Compressed Higgsino | 737 | Soft dileptons + MET | 0.6 |
| C | Light sleptons | 509 | Dilepton + MET | 14418.8 |
| D | Compressed stop + displaced | 7 | b + displaced pion + MET | 14418.8 |
| E | Complex EWKino cascades | 41 | Multi-body finals | 12.1 |
