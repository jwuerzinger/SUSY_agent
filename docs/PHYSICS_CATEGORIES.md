# Physics Categories for LHC Search Targets

This document defines the phenomenological categories used to classify pMSSM models as interesting targets for LHC Run 3 searches. Categories are **not mutually exclusive** — a model can belong to multiple categories.

## Prerequisites (applied before categorization)

All models must pass these quality and physics cuts:

### Quality cuts
- `SP_m_h != -1` — SPheno converged
- `SS_m_h != -1` — Softsusy converged
- `SP_LSP_type` in {1, 2, 3} — neutralino is the LSP (Bino/Wino/Higgsino-like)

### Physics constraints
| Constraint | Variable | Requirement | Source |
|-----------|----------|-------------|--------|
| Higgs mass | `FH_m_h` (or `SP_m_h` if FH unavailable) | 122 – 128 GeV | Combined ATLAS+CMS, 125.09 +/- ~3 GeV (incl. theory uncertainty) |
| Relic density | `MO_Omega` | <= 0.132 | Planck 2018: 0.120 +/- 0.012 (upper bound, allow under-abundance) |
| BR(b -> s gamma) | `SI_BR_b_to_sgamma` | 2.66e-4 – 3.98e-4 | World average 3.32e-4 +/- 0.33e-4 (2 sigma) |
| BR(Bs -> mu mu) | `SI_BR_Bs_to_mumu` | 1.79e-9 – 4.39e-9 | LHCb+CMS 3.09e-9 +/- 0.65e-9 (2 sigma) |

### SModelS exclusion
- Not excluded: `SModelS_bestExpUL_TheoryPrediction < SModelS_bestExpUL_UpperLimit`
- Models without SModelS results (`== -1`) are treated as allowed

---

## Category Definitions

### 1. Bino LSP with Light Electroweakinos
- **Selection:** `SP_LSP_type == 1` AND `|SP_m_chi_20| < 1000` AND `|SP_m_chi_1p| < 1000`
- **Physics:** Classic electroweakino production via chi_20 chi_1+ pairs, decaying to LSP + W/Z/h
- **LHC signatures:** Multi-lepton + MET, WZ + MET, Wh + MET

### 2. Wino-like Compressed
- **Selection:** `SP_LSP_type == 2` AND `|SP_m_chi_1p| - |SP_m_chi_10| < 20 GeV`
- **Physics:** Nearly degenerate Wino triplet; chi_1+ has macroscopic lifetime
- **LHC signatures:** Disappearing tracks, soft leptons + MET, monojet + MET

### 3. Higgsino-like Compressed
- **Selection:** `SP_LSP_type == 3` AND `|SP_m_chi_20| - |SP_m_chi_10| < 30 GeV`
- **Physics:** Nearly degenerate Higgsino doublet (chi_10, chi_20, chi_1+)
- **LHC signatures:** Soft leptons + MET, monojet + MET, VBF + MET

### 4. Light Stop
- **Selection:** `|SP_m_t_1| < 1200` AND `|SP_m_t_1| - |SP_m_chi_10| > 20`
- **Physics:** Pair-produced stops decaying to top + chi_10 or bottom + chi_1+
- **LHC signatures:** Top pairs + MET, 1-lepton + jets + MET

### 5. Light Sbottom
- **Selection:** `|SP_m_b_1| < 1200` AND `|SP_m_b_1| - |SP_m_chi_10| > 20`
- **Physics:** Pair-produced sbottoms decaying to bottom + chi_10
- **LHC signatures:** b-jets + MET

### 6. Light Sleptons
- **Selection:** `min(|SP_m_e_L|, |SP_m_e_R|) < 600`
- **Physics:** Direct slepton pair production, decaying to lepton + chi_10
- **LHC signatures:** Opposite-sign dileptons + MET

### 7. Compressed Electroweakino (general)
- **Selection:** `|SP_m_chi_1p| - |SP_m_chi_10| < 50 GeV`
- **Physics:** Small chi_1+ — chi_10 splitting regardless of LSP composition
- **LHC signatures:** Soft leptons, disappearing tracks, monojet

### 8. Compressed Stop
- **Selection:** `|SP_m_t_1| - |SP_m_chi_10| < 200 GeV`
- **Physics:** Stop close to LSP — 4-body decay, charm + chi_10, or monojet-like
- **LHC signatures:** Charm-tagged jets + MET, monojet, soft b-jets

### 9. Heavy Higgs Accessible
- **Selection:** `|SP_m_H| < 1000` OR `|SP_m_A| < 1000`
- **Physics:** H/A within reach of direct searches (H/A -> tau tau, H/A -> bb, H -> WW/ZZ)
- **LHC signatures:** Ditau resonance, diboson, di-b-jet

---

## Notes

- Mass thresholds are initial estimates and may be refined based on scan results
- All masses are physical pole masses from SPheno (signed for neutralinos/charginos)
- Categories should be reviewed after Phase 1 flat scan to assess population statistics
