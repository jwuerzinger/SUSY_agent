# Ntuple Variable Reference

This document lists all branches available in the ROOT ntuples produced by Run3ModelGen. The ntuple tree is named `susy` and is created by `ntupling.py`.

## Naming Convention

All variables are prefixed by their pipeline step:

| Prefix | Source | File Type |
|--------|--------|-----------|
| `IN_` | Input parameters (EXTPAR block) | `.slha` |
| `SP_` | SPheno spectrum output | `.slha` |
| `SS_` | Softsusy spectrum output | `.slha` |
| `MO_` | micrOMEGAs dark matter output | `.csv` |
| `SI_` | SuperISO flavor physics output | `.flha` |
| `GM2_` | GM2Calc muon g-2 output | `.slha` |
| `FH_` | FeynHiggs Higgs mass output | `.slha` |
| `SModelS_` | SModelS LHC exclusion output | `.slha.py` |

A value of `-1` indicates the corresponding pipeline step failed for that model.

---

## Input Parameters (`IN_`)

From the EXTPAR block of the input SLHA file.

| Variable | EXTPAR key | Description |
|----------|-----------|-------------|
| `IN_M_1` | 1 | Bino mass parameter [GeV] |
| `IN_M_2` | 2 | Wino mass parameter [GeV] |
| `IN_M_3` | 3 | Gluino mass parameter [GeV] |
| `IN_At` | 11 | Top trilinear coupling [GeV] |
| `IN_Ab` | 12 | Bottom trilinear coupling [GeV] |
| `IN_Atau` | 13 | Tau trilinear coupling [GeV] |
| `IN_mu` | 23 | Higgsino mass parameter [GeV] |
| `IN_tanb` | 25 | tan(beta) |
| `IN_mA` | 26 | Pseudoscalar Higgs mass [GeV] |
| `IN_meL` | 31 | Left selectron/smuon soft mass [GeV] |
| `IN_mmuL` | 32 | Left smuon soft mass [GeV] |
| `IN_mtauL` | 33 | Left stau soft mass [GeV] |
| `IN_meR` | 34 | Right selectron soft mass [GeV] |
| `IN_mmuR` | 35 | Right smuon soft mass [GeV] |
| `IN_mtauR` | 36 | Right stau soft mass [GeV] |
| `IN_mqL1` | 41 | 1st gen left squark soft mass [GeV] |
| `IN_mqL2` | 42 | 2nd gen left squark soft mass [GeV] |
| `IN_mqL3` | 43 | 3rd gen left squark soft mass [GeV] |
| `IN_muR` | 44 | Right up squark soft mass [GeV] |
| `IN_mcR` | 45 | Right charm squark soft mass [GeV] |
| `IN_mtR` | 46 | Right stop soft mass [GeV] |
| `IN_mdR` | 47 | Right down squark soft mass [GeV] |
| `IN_msR` | 48 | Right strange squark soft mass [GeV] |
| `IN_mbR` | 49 | Right sbottom soft mass [GeV] |

---

## SPheno / Softsusy Mass Spectrum (`SP_`, `SS_`)

Both SPheno and Softsusy share the same variable names (with their respective prefix). These come from reading the SLHA blocks: MINPAR, EXTPAR, MASS, NMIX, UMIX, VMIX, STOPMIX, SBOTMIX, STAUMIX. SPheno also reads SPHENOLOWENERGY.

### MASS block (physical pole masses)

| Variable | PDG ID | Description |
|----------|--------|-------------|
| `{prefix}m_W` | 24 | W boson mass [GeV] |
| `{prefix}m_h` | 25 | Light CP-even Higgs mass [GeV] |
| `{prefix}m_H` | 35 | Heavy CP-even Higgs mass [GeV] |
| `{prefix}m_A` | 36 | CP-odd Higgs mass [GeV] |
| `{prefix}m_Hp` | 37 | Charged Higgs mass [GeV] |
| `{prefix}m_d_L` | 1000001 | Left down squark mass [GeV] |
| `{prefix}m_d_R` | 2000001 | Right down squark mass [GeV] |
| `{prefix}m_u_L` | 1000002 | Left up squark mass [GeV] |
| `{prefix}m_u_R` | 2000002 | Right up squark mass [GeV] |
| `{prefix}m_s_L` | 1000003 | Left strange squark mass [GeV] |
| `{prefix}m_s_R` | 2000003 | Right strange squark mass [GeV] |
| `{prefix}m_c_L` | 1000004 | Left charm squark mass [GeV] |
| `{prefix}m_c_R` | 2000004 | Right charm squark mass [GeV] |
| `{prefix}m_b_1` | 1000005 | Lighter sbottom mass [GeV] |
| `{prefix}m_b_2` | 2000005 | Heavier sbottom mass [GeV] |
| `{prefix}m_t_1` | 1000006 | Lighter stop mass [GeV] |
| `{prefix}m_t_2` | 2000006 | Heavier stop mass [GeV] |
| `{prefix}m_e_L` | 1000011 | Left selectron mass [GeV] |
| `{prefix}m_e_R` | 2000011 | Right selectron mass [GeV] |
| `{prefix}m_nu_eL` | 1000012 | Electron sneutrino mass [GeV] |
| `{prefix}m_mu_L` | 1000013 | Left smuon mass [GeV] |
| `{prefix}m_mu_R` | 2000013 | Right smuon mass [GeV] |
| `{prefix}m_nu_muL` | 1000014 | Muon sneutrino mass [GeV] |
| `{prefix}m_tau_1` | 1000015 | Lighter stau mass [GeV] |
| `{prefix}m_tau_2` | 2000015 | Heavier stau mass [GeV] |
| `{prefix}m_nu_tauL` | 1000016 | Tau sneutrino mass [GeV] |
| `{prefix}m_gl` | 1000021 | Gluino mass [GeV] |
| `{prefix}m_chi_10` | 1000022 | Lightest neutralino mass [GeV] |
| `{prefix}m_chi_20` | 1000023 | 2nd neutralino mass [GeV] |
| `{prefix}m_chi_30` | 1000025 | 3rd neutralino mass [GeV] |
| `{prefix}m_chi_40` | 1000035 | 4th neutralino mass [GeV] |
| `{prefix}m_chi_1p` | 1000024 | Lighter chargino mass [GeV] |
| `{prefix}m_chi_2p` | 1000037 | Heavier chargino mass [GeV] |
| `{prefix}m_G` | 1000039 | Gravitino mass [GeV] |

### Neutralino mixing matrix (NMIX block)

| Variable | Entry | Description |
|----------|-------|-------------|
| `{prefix}N_11` to `{prefix}N_14` | (1,1)-(1,4) | chi_10 composition (Bino, Wino, Hd, Hu) |
| `{prefix}N_21` to `{prefix}N_24` | (2,1)-(2,4) | chi_20 composition |
| `{prefix}N_31` to `{prefix}N_34` | (3,1)-(3,4) | chi_30 composition |
| `{prefix}N_41` to `{prefix}N_44` | (4,1)-(4,4) | chi_40 composition |

### Chargino mixing matrices (UMIX, VMIX)

| Variable | Description |
|----------|-------------|
| `{prefix}U_11`, `{prefix}U_12`, `{prefix}U_21`, `{prefix}U_22` | Negative chargino mixing |
| `{prefix}V_11`, `{prefix}V_12`, `{prefix}V_21`, `{prefix}V_22` | Positive chargino mixing |

### Squark/slepton mixing

| Variable | Description |
|----------|-------------|
| `{prefix}cos_t` | STOPMIX(1,1) — stop mixing angle cosine |
| `{prefix}cos_b` | SBOTMIX(1,1) — sbottom mixing angle cosine |
| `{prefix}cos_tau` | STAUMIX(1,1) — stau mixing angle cosine |

### Computed variables (from ntupling post-processing)

| Variable | Description |
|----------|-------------|
| `{prefix}LSP_type` | 1=Bino, 2=Wino, 3=Higgsino (only if chi_10 is LSP) |
| `{prefix}LSP_Bino_frac` | N_11^2 (Bino fraction of LSP) |
| `{prefix}LSP_Wino_frac` | N_12^2 (Wino fraction of LSP) |
| `{prefix}LSP_Higgsino_frac` | N_13^2 + N_14^2 (Higgsino fraction of LSP) |
| `{prefix}chi_10_Bino_frac` | N_11^2 |
| `{prefix}chi_10_Wino_frac` | N_12^2 |
| `{prefix}chi_10_Higgsino_frac` | N_13^2 + N_14^2 |
| `{prefix}chi_20_Bino_frac` | N_21^2 |
| `{prefix}chi_20_Wino_frac` | N_22^2 |
| `{prefix}chi_20_Higgsino_frac` | N_23^2 + N_24^2 |
| (similar for chi_30, chi_40) | ... |
| `{prefix}chi_1p_Wino_frac` | V_11^2 |
| `{prefix}chi_1p_Higgsino_frac` | V_12^2 |
| `{prefix}chi_1m_Wino_frac` | U_11^2 |
| `{prefix}chi_1m_Higgsino_frac` | U_12^2 |

### Branching fractions (from decay tables)

Format: `{prefix}BF_{parent}_to_{daughters}` and `{prefix}BF_{parent}_other` for untracked modes.

Key examples for stop_1 (prefix `SP_` or `SS_`):
- `BF_t_1_to_chi_10_t` — stop_1 → chi_10 + top
- `BF_t_1_to_chi_10_b` — stop_1 → chi_10 + bottom (via W)
- `BF_t_1_to_chi_10_c` — stop_1 → chi_10 + charm (flavor-violating)
- `BF_t_1_to_chi_1p_b` — stop_1 → chi_1+ + bottom
- `BF_t_1_to_gl` — stop_1 → gluino

Tracked particles: gluino, stop_1/2, sbottom_1/2, d_L/R, u_L/R, selectrons, smuons, staus, sneutrinos, chi_10 through chi_40, chi_1p/2p.

### SPheno-only: SPHENOLOWENERGY block

| Variable | Entry | Description |
|----------|-------|-------------|
| `SP_BR_b_to_sgamma` | 1 | BR(b → s gamma) |
| `SP_BR_Bs_to_mumu` | 8 | BR(Bs → mu mu) |
| `SP_BR_Bu_to_taunu` | 10 | BR(Bu → tau nu) |
| `SP_BR_Bu_to_taunu_dev_by_SM` | 11 | R(Bu → tau nu) / SM |
| `SP_gmuon` | 21 | SUSY contribution to muon g-2 |
| `SP_BR_mu_to_egamma` | 26 | BR(mu → e gamma) |
| `SP_BR_tau_to_egamma` | 27 | BR(tau → e gamma) |
| `SP_BR_tau_to_mugamma` | 28 | BR(tau → mu gamma) |
| `SP_BR_mu_to_3e` | 29 | BR(mu → 3e) |
| `SP_BR_tau_to_3e` | 30 | BR(tau → 3e) |
| `SP_BR_tau_to_3mu` | 31 | BR(tau → 3mu) |
| `SP_deltarho` | 39 | Delta rho (electroweak precision) |

---

## micrOMEGAs (`MO_`)

From CSV output. Key variables:

| Variable | Description |
|----------|-------------|
| `MO_Omega` | Dark matter relic density (Omega * h^2) |
| `MO_deltarho` | Electroweak oblique parameter |
| `MO_gmuon` | SUSY contribution to muon g-2 |
| `MO_bsgnlo` | BR(b → s gamma) at NLO |
| `MO_bsmumu` | BR(Bs → mu mu) |
| `MO_btaunu` | BR(B → tau nu) |
| `MO_bmunu` | BR(B → mu nu) |
| `MO_proton_SI` | Spin-independent proton-neutralino cross section [pb] |
| `MO_proton_SD` | Spin-dependent proton-neutralino cross section [pb] |
| `MO_neutron_SI` | Spin-independent neutron-neutralino cross section [pb] |
| `MO_neutron_SD` | Spin-dependent neutron-neutralino cross section [pb] |

---

## SuperISO (`SI_`)

From FLHA (Flavor Les Houches Accord) file.

### FOBS block (SUSY predictions)

| Variable | Entry | Description |
|----------|-------|-------------|
| `SI_BR_b_to_sgamma` | (5,1) | BR(b → s gamma) |
| `SI_BR_Bs_to_mumu` | (531,1) | BR(Bs → mu mu) |
| `SI_Delta0_B_to_Kshgamma` | (521,4) | Isospin asymmetry Delta_0(B → K* gamma) |
| `SI_R_Bu_to_taunu` | (521,2) | R(Bu → tau nu) |
| `SI_BR_Bp_to_D0taunu_dev_by_BR_Bp_to_D0enu` | (521,11) | R(B+ → D0 tau nu / B+ → D0 e nu) |
| `SI_BR_K_to_munu_dev_by_BR_pi_to_munu` | (321,11) | R(K → mu nu / pi → mu nu) |
| `SI_R_mu23` | (321,12) | R_mu23 |

### FOBSSM block (SM predictions, same variables with `_SM` suffix)

---

## GM2Calc (`GM2_`)

| Variable | Entry | Description |
|----------|-------|-------------|
| `GM2_gmuon` | 0 | SUSY contribution to (g-2)_mu |
| `GM2_Delta_gmuon` | 1 | Uncertainty on (g-2)_mu |

---

## FeynHiggs (`FH_`)

| Variable | Block | Description |
|----------|-------|-------------|
| `FH_m_h` | MASS[25] | Light Higgs mass with higher-order corrections [GeV] |
| `FH_Delta_m_h` | DMASS[25] | Uncertainty on m_h [GeV] |

---

## SModelS (`SModelS_`)

From the SModelS Python output file (`.slha.py`).

### Per-analysis variables

For each experimental analysis that has a non-zero theory prediction:
- `SModelS_{AnalysisID}_TheoryPrediction` — predicted signal cross section [fb]
- `SModelS_{AnalysisID}_UpperLimit` — observed upper limit [fb]
- `SModelS_{AnalysisID}_ExpUpperLimit` — expected upper limit [fb]

### Best expected upper limit (most sensitive analysis)

| Variable | Description |
|----------|-------------|
| `SModelS_bestExpUL_TheoryPrediction` | Theory prediction for most sensitive analysis [fb] |
| `SModelS_bestExpUL_UpperLimit` | Observed upper limit for most sensitive analysis [fb] |
| `SModelS_bestExpUL_ExpUpperLimit` | Expected upper limit for most sensitive analysis [fb] |

A model is **excluded** if `TheoryPrediction > UpperLimit` (r-value > 1).

---

## Special Variables

| Variable | Description |
|----------|-------------|
| `model` | Model index number (0 to num_models-1) |
