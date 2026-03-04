# ATLAS Coverage Analysis Report

**Date:** 2026-03-03
**Models analyzed:** 2063
**SModelS files parsed:** 2060 (missing: 3)

## Summary

Of 2063 pMSSM models surviving all experimental constraints:

- **1372 models (66.5%)** have zero ATLAS sensitivity (no ATLAS analysis provides any constraint)
- **981 models (47.6%)** have zero CMS sensitivity
- **959 models** have zero sensitivity from either experiment
- Maximum uncovered displaced cross-section: 14362.4 fb
- Maximum uncovered prompt cross-section: 4557.2 fb

## ATLAS Coverage Tiers

| Tier | Label | Count | Fraction |
|------|-------|-------|----------|
| 0 | Invisible | 1372 | 66.5% |
| 1 | Negligible | 84 | 4.1% |
| 2 | Weak | 289 | 14.0% |
| 3 | Moderate | 215 | 10.4% |
| 4 | Near-exclusion | 58 | 2.8% |
| 5 | Excluded | 45 | 2.2% |

## Coverage by LSP Type

| LSP | Total | Invisible | Negligible | Weak | Moderate | Near-excl. | Excluded |
|-----|-------|-----------|------------|------|----------|------------|----------|
| Bino | 62 | 39 | 4 | 3 | 10 | 5 | 1 |
| Wino | 1003 | 616 | 60 | 156 | 90 | 40 | 41 |
| Higgsino | 998 | 717 | 20 | 130 | 115 | 13 | 3 |

## Coverage by Physics Category

| Category | Total | Invisible | Negligible | Weak | Moderate | Near-excl. | Excluded |
|----------|-------|-----------|------------|------|----------|------------|----------|
| Bino+lightEWK | 62 | 39 | 4 | 3 | 10 | 5 | 1 |
| Compressed_EWK | 2053 | 1371 | 84 | 289 | 210 | 54 | 45 |
| Compressed_stop | 7 | 0 | 0 | 1 | 1 | 0 | 5 |
| Heavy_Higgs | 308 | 225 | 7 | 37 | 33 | 5 | 1 |
| Higgsino_compressed | 863 | 622 | 15 | 109 | 105 | 11 | 1 |
| Light_sbottom | 381 | 18 | 31 | 114 | 117 | 56 | 45 |
| Light_slepton | 629 | 335 | 39 | 123 | 89 | 29 | 14 |
| Light_stop | 269 | 10 | 7 | 76 | 108 | 37 | 31 |
| Wino_compressed | 1003 | 616 | 60 | 156 | 90 | 40 | 41 |

## ATLAS Analyses Providing Constraints

| Analysis | Models constrained |
|----------|-------------------|
| ATLAS-SUSY-2018-12 | 1059 |
| ATLAS-SUSY-2018-08 | 1040 |
| ATLAS-SUSY-2016-16 | 691 |
| ATLAS-SUSY-2016-28 | 547 |
| ATLAS-SUSY-2016-15 | 420 |
| ATLAS-SUSY-2015-01 | 215 |
| ATLAS-SUSY-2018-31 | 148 |
| ATLAS-SUSY-2015-02 | 116 |
| ATLAS-SUSY-2016-17 | 85 |
| ATLAS-SUSY-2016-07 | 69 |
| ATLAS-SUSY-2018-22 | 68 |
| ATLAS-SUSY-2016-32 | 56 |
| ATLAS-SUSY-2015-06 | 37 |
| ATLAS-SUSY-2016-26 | 25 |
| ATLAS-SUSY-2018-40 | 7 |
| ATLAS-SUSY-2016-14 | 3 |

## CMS Analyses Providing Constraints

| Analysis | Models constrained |
|----------|-------------------|
| CMS-SUS-16-033 | 1973 |
| CMS-SUS-19-006 | 1874 |
| CMS-SUS-16-036 | 1087 |
| CMS-SUS-19-006-agg | 1021 |
| CMS-SUS-19-010 | 997 |
| CMS-SUS-16-050 | 752 |
| CMS-SUS-20-002 | 607 |
| CMS-SUS-19-009 | 589 |
| CMS-SUS-16-032 | 506 |
| CMS-SUS-16-050-agg | 478 |
| CMS-SUS-19-008 | 364 |
| CMS-SUS-17-010 | 301 |
| CMS-SUS-16-051 | 289 |
| CMS-SUS-19-011 | 284 |
| CMS-SUS-16-009 | 84 |
| CMS-SUS-18-002 | 12 |
| CMS-SUS-16-045 | 3 |
| CMS-SUS-21-007 | 2 |
| CMS-SUS-16-041 | 1 |
| CMS-SUS-16-035 | 1 |

## ATLAS TxNames (Simplified Model Topologies)

| TxName | Occurrences |
|--------|-------------|
| T2tt | 3411 |
| T2bb | 762 |
| T2 | 174 |
| T6bbHH | 155 |
| THSCPM3 | 55 |
| THSCPM4 | 37 |
| T2cc | 25 |
| THSCPM9 | 2 |
| T1tttt | 2 |
| T6ttWW | 1 |
| THSCPM5 | 1 |

## Missing Topologies (Prompt)

Top SMS strings not covered by any analysis, by number of models affected:

| SMS | Models |
|-----|--------|
| `PV > (b,MET),(W,t,MET)` | 313 |
| `PV > (b,MET),(t,jet,MET)` | 278 |
| `PV > (t,MET),(b,jet,MET)` | 265 |
| `PV > (t,MET),(W,b,MET)` | 218 |
| `PV > (b,MET),(t,jet,jet,MET)` | 170 |
| `PV > (b,MET),(t,nu,l,MET)` | 162 |
| `PV > (t,MET),(b,jet,jet,MET)` | 128 |
| `PV > (t,MET),(Z,t,MET)` | 126 |
| `PV > (b,jet,MET),(b,jet,MET)` | 124 |
| `PV > (t,jet,MET),(W,t,MET)` | 122 |
| `PV > (b,MET),(Z,b,MET)` | 118 |
| `PV > (b,MET),(b,jet,jet,MET)` | 113 |
| `PV > (t,MET),(t,jet,jet,MET)` | 102 |
| `PV > (b,MET),(b,higgs,MET)` | 91 |
| `PV > (t,MET),(t,higgs,MET)` | 88 |
| `PV > (W,t,MET),(Z,b,MET)` | 82 |
| `PV > (t,MET),(W,t,MET)` | 80 |
| `PV > (t,MET),(b,nu,l,MET)` | 79 |
| `PV > (jet,MET),(t,MET)` | 73 |
| `PV > (b,MET),(W,b,jet,MET)` | 72 |

## Missing Topologies (Displaced)

| SMS | Models |
|-----|--------|
| `PV > (b,jet,MET),(b,jet,MET)` | 359 |
| `PV > (t,jet,MET),(t,jet,MET)` | 356 |
| `PV > (b,MET),(t,jet,MET)` | 337 |
| `PV > (t,MET),(b,jet,MET)` | 306 |
| `PV > (t,jet,MET),(W,b,jet,MET)` | 181 |
| `PV > (b,jet,MET),(W,t,jet,MET)` | 150 |
| `PV > (t,jet,MET),(W,t,MET)` | 141 |
| `PV > (W,b,jet,MET),(W,b,jet,MET)` | 139 |
| `PV > (t,jet,MET),(Z,t,jet,MET)` | 128 |
| `PV > (t,jet,MET),(t,nu,l,MET)` | 105 |
| `PV > (b,MET),(W,b,jet,MET)` | 94 |
| `PV > (b,MET),(t,nu,l,MET)` | 94 |
| `PV > (W,t,MET),(W,b,jet,MET)` | 92 |
| `PV > (t,jet,MET),(t,higgs,jet,MET)` | 91 |
| `PV > (W,t,MET),(Z,t,jet,MET)` | 87 |
| `PV > (b,jet,MET),(b,nu,l,MET)` | 80 |
| `PV > (Z,t,jet,MET),(W,b,jet,MET)` | 79 |
| `PV > (t,higgs,jet,MET),(Z,t,jet,MET)` | 74 |
| `PV > (t,higgs,jet,MET),(W,b,jet,MET)` | 66 |
| `PV > (b,jet,MET),(W,b,MET)` | 65 |

## Topologies Outside Grid

| SMS | Models |
|-----|--------|
| `PV > (W,t,MET),(W,t,MET)` | 283 |
| `PV > (t,MET),(b,MET)` | 267 |
| `PV > (t,jet,jet,MET),(t,jet,jet,MET)` | 152 |
| `PV > (t,nu,l,MET),(t,nu,l,MET)` | 103 |
| `PV > (Z,t,MET),(Z,t,MET)` | 90 |
| `PV > (t,jet,jet,MET),(t,nu,l,MET)` | 78 |
| `PV > (b,nu,l,MET),(b,nu,l,MET)` | 75 |
| `PV > (t,jet,jet,MET),(t,nu,ta,MET)` | 56 |
| `PV > (b,jet,jet,MET),(b,jet,jet,MET)` | 56 |
| `PV > (t,jet,MET),(t,jet,MET)` | 53 |
| `PV > (b,b,MET),(b,b,MET)` | 32 |
| `PV > (b,jet,jet,MET),(b,nu,ta,MET)` | 25 |
| `PV > (b,jet,jet,MET),(b,nu,l,MET)` | 25 |
| `PV > (photon,t,MET),(photon,t,MET)` | 20 |
| `PV > (b,nu,ta,MET),(b,nu,ta,MET)` | 12 |
| `PV > (b,nu,l,MET),(b,nu,ta,MET)` | 12 |
| `PV > (b,higgs,MET),(b,higgs,MET)` | 11 |
| `PV > (b,MET),(b,MET)` | 7 |
| `PV > (W,b,MET),(W,b,MET)` | 7 |
| `PV > (t,t,MET),(t,t,MET)` | 2 |
