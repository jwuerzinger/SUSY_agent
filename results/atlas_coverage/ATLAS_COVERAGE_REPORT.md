# ATLAS Coverage Analysis Report

**Date:** 2026-03-03
**Models analyzed:** 2087
**SModelS files parsed:** 2084 (missing: 3)

## Summary

Of 2087 pMSSM models surviving all experimental constraints:

- **1372 models (65.7%)** have zero ATLAS sensitivity (no ATLAS analysis provides any constraint)
- **981 models (47.0%)** have zero CMS sensitivity
- **959 models** have zero sensitivity from either experiment
- Maximum uncovered displaced cross-section: 14362.4 fb
- Maximum uncovered prompt cross-section: 4557.2 fb

## ATLAS Coverage Tiers

| Tier | Label | Count | Fraction |
|------|-------|-------|----------|
| 0 | Invisible | 1372 | 65.7% |
| 1 | Negligible | 84 | 4.0% |
| 2 | Weak | 301 | 14.4% |
| 3 | Moderate | 227 | 10.9% |
| 4 | Near-exclusion | 58 | 2.8% |
| 5 | Excluded | 45 | 2.2% |

## Coverage by LSP Type

| LSP | Total | Invisible | Negligible | Weak | Moderate | Near-excl. | Excluded |
|-----|-------|-----------|------------|------|----------|------------|----------|
| Bino | 80 | 39 | 4 | 15 | 16 | 5 | 1 |
| Wino | 1009 | 616 | 60 | 156 | 96 | 40 | 41 |
| Higgsino | 998 | 717 | 20 | 130 | 115 | 13 | 3 |

## Coverage by Physics Category

| Category | Total | Invisible | Negligible | Weak | Moderate | Near-excl. | Excluded |
|----------|-------|-----------|------------|------|----------|------------|----------|
| Bino+lightEWK | 80 | 39 | 4 | 15 | 16 | 5 | 1 |
| Compressed_EWK | 2077 | 1371 | 84 | 301 | 222 | 54 | 45 |
| Compressed_stop | 7 | 0 | 0 | 1 | 1 | 0 | 5 |
| Heavy_Higgs | 308 | 225 | 7 | 37 | 33 | 5 | 1 |
| Higgsino_compressed | 863 | 622 | 15 | 109 | 105 | 11 | 1 |
| Light_sbottom | 405 | 18 | 31 | 126 | 129 | 56 | 45 |
| Light_slepton | 653 | 335 | 39 | 135 | 101 | 29 | 14 |
| Light_stop | 293 | 10 | 7 | 88 | 120 | 37 | 31 |
| Wino_compressed | 1009 | 616 | 60 | 156 | 96 | 40 | 41 |

## ATLAS Analyses Providing Constraints

| Analysis | Models constrained |
|----------|-------------------|
| ATLAS-SUSY-2018-12 | 1105 |
| ATLAS-SUSY-2018-08 | 1086 |
| ATLAS-SUSY-2016-16 | 737 |
| ATLAS-SUSY-2016-28 | 571 |
| ATLAS-SUSY-2016-15 | 443 |
| ATLAS-SUSY-2015-01 | 222 |
| ATLAS-SUSY-2018-31 | 148 |
| ATLAS-SUSY-2015-02 | 122 |
| ATLAS-SUSY-2016-17 | 91 |
| ATLAS-SUSY-2016-07 | 79 |
| ATLAS-SUSY-2018-22 | 78 |
| ATLAS-SUSY-2016-32 | 56 |
| ATLAS-SUSY-2015-06 | 42 |
| ATLAS-SUSY-2016-26 | 29 |
| ATLAS-SUSY-2018-40 | 7 |
| ATLAS-SUSY-2016-14 | 3 |

## CMS Analyses Providing Constraints

| Analysis | Models constrained |
|----------|-------------------|
| CMS-SUS-16-033 | 2049 |
| CMS-SUS-19-006 | 1927 |
| CMS-SUS-16-036 | 1139 |
| CMS-SUS-19-006-agg | 1045 |
| CMS-SUS-19-010 | 1022 |
| CMS-SUS-16-050 | 779 |
| CMS-SUS-20-002 | 630 |
| CMS-SUS-19-009 | 612 |
| CMS-SUS-16-032 | 530 |
| CMS-SUS-16-050-agg | 501 |
| CMS-SUS-19-008 | 370 |
| CMS-SUS-17-010 | 324 |
| CMS-SUS-16-051 | 312 |
| CMS-SUS-19-011 | 307 |
| CMS-SUS-16-009 | 90 |
| CMS-SUS-18-002 | 12 |
| CMS-SUS-16-045 | 3 |
| CMS-SUS-21-007 | 2 |
| CMS-SUS-16-041 | 1 |
| CMS-SUS-16-035 | 1 |

## ATLAS TxNames (Simplified Model Topologies)

| TxName | Occurrences |
|--------|-------------|
| T2tt | 3584 |
| T2bb | 793 |
| T2 | 199 |
| T6bbHH | 155 |
| THSCPM3 | 55 |
| THSCPM4 | 37 |
| T2cc | 29 |
| THSCPM9 | 2 |
| T1tttt | 2 |
| T6ttWW | 1 |
| THSCPM5 | 1 |

## Missing Topologies (Prompt)

Top SMS strings not covered by any analysis, by number of models affected:

| SMS | Models |
|-----|--------|
| `PV > (b,MET),(W,t,MET)` | 313 |
| `PV > (b,MET),(t,jet,MET)` | 284 |
| `PV > (t,MET),(b,jet,MET)` | 271 |
| `PV > (t,MET),(W,b,MET)` | 224 |
| `PV > (b,MET),(t,jet,jet,MET)` | 188 |
| `PV > (b,MET),(t,nu,l,MET)` | 183 |
| `PV > (t,MET),(b,jet,jet,MET)` | 145 |
| `PV > (b,jet,MET),(b,jet,MET)` | 129 |
| `PV > (t,MET),(Z,t,MET)` | 126 |
| `PV > (t,jet,MET),(W,t,MET)` | 122 |
| `PV > (b,MET),(Z,b,MET)` | 118 |
| `PV > (b,MET),(b,jet,jet,MET)` | 113 |
| `PV > (t,MET),(t,jet,jet,MET)` | 102 |
| `PV > (t,MET),(b,nu,l,MET)` | 97 |
| `PV > (b,MET),(b,higgs,MET)` | 91 |
| `PV > (t,MET),(t,higgs,MET)` | 88 |
| `PV > (b,MET),(b,l,l,MET)` | 85 |
| `PV > (W,t,MET),(Z,b,MET)` | 82 |
| `PV > (t,MET),(W,t,MET)` | 80 |
| `PV > (jet,MET),(t,MET)` | 78 |

## Missing Topologies (Displaced)

| SMS | Models |
|-----|--------|
| `PV > (b,jet,MET),(b,jet,MET)` | 365 |
| `PV > (t,jet,MET),(t,jet,MET)` | 362 |
| `PV > (b,MET),(t,jet,MET)` | 343 |
| `PV > (t,MET),(b,jet,MET)` | 312 |
| `PV > (t,jet,MET),(W,b,jet,MET)` | 181 |
| `PV > (b,jet,MET),(W,t,jet,MET)` | 150 |
| `PV > (t,jet,MET),(W,t,MET)` | 141 |
| `PV > (W,b,jet,MET),(W,b,jet,MET)` | 139 |
| `PV > (t,jet,MET),(Z,t,jet,MET)` | 128 |
| `PV > (t,jet,MET),(t,nu,l,MET)` | 111 |
| `PV > (b,MET),(t,nu,l,MET)` | 98 |
| `PV > (b,MET),(W,b,jet,MET)` | 94 |
| `PV > (W,t,MET),(W,b,jet,MET)` | 92 |
| `PV > (t,jet,MET),(t,higgs,jet,MET)` | 91 |
| `PV > (W,t,MET),(Z,t,jet,MET)` | 87 |
| `PV > (b,jet,MET),(b,nu,l,MET)` | 86 |
| `PV > (Z,t,jet,MET),(W,b,jet,MET)` | 79 |
| `PV > (t,higgs,jet,MET),(Z,t,jet,MET)` | 74 |
| `PV > (b,jet,MET),(W,b,MET)` | 67 |
| `PV > (t,higgs,jet,MET),(W,b,jet,MET)` | 66 |

## Topologies Outside Grid

| SMS | Models |
|-----|--------|
| `PV > (W,t,MET),(W,t,MET)` | 283 |
| `PV > (t,MET),(b,MET)` | 267 |
| `PV > (t,jet,jet,MET),(t,jet,jet,MET)` | 168 |
| `PV > (t,nu,l,MET),(t,nu,l,MET)` | 121 |
| `PV > (t,jet,jet,MET),(t,nu,l,MET)` | 96 |
| `PV > (b,nu,l,MET),(b,nu,l,MET)` | 92 |
| `PV > (Z,t,MET),(Z,t,MET)` | 91 |
| `PV > (b,jet,jet,MET),(b,jet,jet,MET)` | 69 |
| `PV > (t,jet,jet,MET),(t,nu,ta,MET)` | 68 |
| `PV > (t,jet,MET),(t,jet,MET)` | 53 |
| `PV > (b,jet,jet,MET),(b,nu,l,MET)` | 42 |
| `PV > (b,jet,jet,MET),(b,nu,ta,MET)` | 35 |
| `PV > (b,b,MET),(b,b,MET)` | 32 |
| `PV > (b,nu,l,MET),(b,nu,ta,MET)` | 28 |
| `PV > (photon,t,MET),(photon,t,MET)` | 21 |
| `PV > (b,nu,ta,MET),(b,nu,ta,MET)` | 13 |
| `PV > (b,higgs,MET),(b,higgs,MET)` | 11 |
| `PV > (b,MET),(b,MET)` | 7 |
| `PV > (W,b,MET),(W,b,MET)` | 7 |
| `PV > (t,t,MET),(t,t,MET)` | 2 |
