# Investigation Plan: Systematic pMSSM Exploration for LHC Run 3 Search Targets

## 1. Motivation and Physics Goals

The Large Hadron Collider (LHC) is entering Run 3 with significantly more integrated luminosity than previous runs. Supersymmetry (SUSY) remains one of the best-motivated extensions of the Standard Model, offering solutions to the hierarchy problem, gauge coupling unification, and a dark matter candidate (the lightest neutralino). However, the pMSSM parameter space is 19-dimensional, and it is far from obvious which regions remain experimentally viable and interesting.

**This investigation aims to:**
1. Systematically sample the pMSSM parameter space using both flat (uniform) and MCMC (physics-constrained) methods
2. Apply current experimental constraints (Higgs mass, dark matter relic density, B-physics observables, LHC exclusions via SModelS)
3. Identify and classify surviving models into phenomenological categories relevant for LHC Run 3 searches
4. Extract benchmark SLHA spectra for each category for use in ATLAS/CMS-style signal simulation

---

## 2. The pMSSM Framework

### 2.1 The 19 Parameters

The phenomenological MSSM (pMSSM) reduces the general MSSM's ~120 parameters to 19 by imposing:
- No new CP violation beyond CKM
- Minimal flavor violation (MFV)
- Degenerate 1st/2nd generation sfermion masses

The 19 free parameters and their physical roles:

| Parameter | EXTPAR key | Description | Flat range | Unit |
|-----------|-----------|-------------|------------|------|
| `tanb` | 25 | Ratio of Higgs VEVs (v_u/v_d) | [1, 60] | - |
| `M_1` | 1 | Bino soft mass (U(1) gaugino) | [-2000, 2000] | GeV |
| `M_2` | 2 | Wino soft mass (SU(2) gaugino) | [-2000, 2000] | GeV |
| `M_3` | 3 | Gluino soft mass (SU(3) gaugino) | [1000, 4000] | GeV |
| `AT` | 11 | Top trilinear coupling | [-8000, 8000] | GeV |
| `Ab` | 12 | Bottom trilinear coupling | [-2000, 2000] | GeV |
| `Atau` | 13 | Tau trilinear coupling | [-2000, 2000] | GeV |
| `mu` | 23 | Higgsino mass parameter | [-2000, 2000] | GeV |
| `mA` | 26 | Pseudoscalar Higgs pole mass | [0, 2000] | GeV |
| `meL` | 31 | Left selectron/smuon soft mass | [0, 2000] | GeV |
| `mtauL` | 33 | Left stau soft mass | fixed at 2000 | GeV |
| `meR` | 34 | Right selectron soft mass | [0, 2000] | GeV |
| `mtauR` | 36 | Right stau soft mass | fixed at 2000 | GeV |
| `mqL1` | 41 | 1st gen left squark soft mass | fixed at 4000 | GeV |
| `mqL3` | 43 | 3rd gen left squark soft mass | [0, 2000] | GeV |
| `muR` | 44 | Right up squark soft mass | fixed at 4000 | GeV |
| `mtR` | 46 | Right stop soft mass | [0, 2000] | GeV |
| `mdR` | 47 | Right down squark soft mass | fixed at 4000 | GeV |
| `mbR` | 49 | Right sbottom soft mass | [0, 2000] | GeV |

**Decoupled parameters:** 1st/2nd generation squarks (`mqL1`, `muR`, `mdR`) are fixed at 4 TeV and staus (`mtauL`, `mtauR`) at 2 TeV. These are already heavily constrained by LHC direct searches and would dominate the parameter space without adding interesting phenomenology. This focuses the scan on electroweakinos, 3rd-generation squarks, and sleptons — the sectors with the most discovery potential at Run 3.

### 2.2 Physics Pipeline

Each pMSSM parameter point is evaluated through an 8-step pipeline:

```
Input SLHA → SPheno → Softsusy → micrOMEGAs → SuperISO → GM2Calc → FeynHiggs → SModelS → Ntuple
```

| Step | Tool | What it computes | Runtime |
|------|------|-----------------|---------|
| 1. `prep_input` | Internal | Generate SLHA input file with EXTPAR block | instant |
| 2. `SPheno` | SPheno 4.x | Full SUSY mass spectrum, mixing matrices, decay tables, low-energy observables | ~1s (or fails instantly if no valid spectrum) |
| 3. `softsusy` | SOFTSUSY 4.x | Independent spectrum cross-check (same SLHA blocks) | ~1s |
| 4. `micromegas` | micrOMEGAs 6.x | Dark matter relic density (Omega h^2), direct detection cross sections, g-2 | ~2s |
| 5. `superiso` | SuperISO 4.x | Flavor physics: BR(b→sγ), BR(Bs→μμ), R(Bu→τν) | ~1s |
| 6. `gm2calc` | GM2Calc 2.x | Precision (g-2)_μ calculation | ~1s |
| 7. `feynhiggs` | FeynHiggs 2.x | Higher-order Higgs mass corrections | ~2s |
| 8. `SModelS` | SModelS 3.x | LHC exclusion check against all published simplified-model results | ~30-60s (uses Pythia for cross-section computation) |

**Critical observation:** The pipeline is serial and bottlenecked by SPheno. If SPheno cannot find a valid SUSY spectrum (common failure modes: tachyonic scalar masses, failure to achieve electroweak symmetry breaking), all downstream tools are skipped. For flat sampling, SPheno fails ~90-95% of the time. Once SPheno succeeds, downstream tools almost always succeed (>99% pass-through rate).

### 2.3 Output Format

All results are stored in ROOT ntuples (tree name: `susy`), readable with uproot/awkward. Each model is one entry with ~1131 branches. Variables are prefixed by their pipeline step (`IN_`, `SP_`, `SS_`, `MO_`, `SI_`, `GM2_`, `FH_`, `SModelS_`). A value of `-1` indicates the corresponding step failed. Full variable reference: [docs/NTUPLE_VARIABLES.md](NTUPLE_VARIABLES.md).

---

## 3. Experimental Constraints

Models must satisfy the following constraints to be considered viable. These are applied as offline cuts in the analysis (Phase 1 flat scans) or as MCMC likelihood terms (Phase 2 targeted scans).

### 3.1 Quality Cuts (prerequisites)
- `SP_m_h != -1` — SPheno converged to a valid spectrum
- `SS_m_h != -1` — Softsusy converged (independent cross-check)
- `SP_LSP_type` in {1, 2, 3} — the lightest SUSY particle is a neutralino (Bino-like=1, Wino-like=2, Higgsino-like=3). Models with charged or colored LSPs are unphysical (cosmologically unstable).

### 3.2 Higgs Mass
- **Observable:** Light CP-even Higgs mass, `FH_m_h` (FeynHiggs, preferred) or `SP_m_h` (SPheno, fallback)
- **Measured value:** 125.09 GeV (combined ATLAS + CMS, Run 1 + Run 2)
- **Cut window:** 122 – 128 GeV (±3 GeV to account for ~2-3 GeV theoretical uncertainty in spectrum generators)
- **MCMC constraint:** `gaussian(125.09, 3.0)` on SPheno MASS block entry 25

### 3.3 Dark Matter Relic Density
- **Observable:** `MO_Omega` (Ω_χ h²) from micrOMEGAs
- **Measured value:** 0.120 ± 0.001 (Planck 2018)
- **Cut:** ≤ 0.132 (allow under-abundance — the neutralino need not be all of dark matter)
- **MCMC constraint:** `upper_bound(0.120, 0.012)`
- **Physics note:** Bino-like LSPs tend to over-produce dark matter (Ω >> 0.12) unless there is co-annihilation, resonance enhancement, or mixed composition. This is the most powerful discriminant after the Higgs mass.

### 3.4 B-Physics Observables
- **BR(b → s γ):** `SI_BR_b_to_sgamma` from SuperISO
  - World average: (3.32 ± 0.33) × 10⁻⁴
  - Cut: within 2σ, i.e., [2.66, 3.98] × 10⁻⁴
  - MCMC constraint: `gaussian(3.32e-4, 0.33e-4)`
- **BR(Bs → μ⁺μ⁻):** `SI_BR_Bs_to_mumu` from SuperISO
  - LHCb+CMS: (3.09 ± 0.65) × 10⁻⁹
  - Cut: within 2σ, i.e., [1.79, 4.39] × 10⁻⁹
  - MCMC constraint: `gaussian(3.09e-9, 0.65e-9)`

### 3.5 LHC Direct Exclusions (SModelS)
- **Observable:** `SModelS_bestExpUL_TheoryPrediction` vs `SModelS_bestExpUL_UpperLimit`
- **Condition:** Model is excluded if theory prediction exceeds the observed upper limit (r > 1)
- **Note:** Models without SModelS results (value = -1) are treated as allowed (SModelS may have no applicable simplified-model topology)
- SModelS checks against all published ATLAS and CMS simplified-model results using the 3.1.1 database

---

## 4. Scan Strategy

The investigation uses a two-phase approach: broad exploration followed by targeted sampling.

### 4.1 Phase 1: Flat Exploration (4 × 500 models)

**Purpose:** Map the viable parameter space with uniform sampling. This provides unbiased coverage and reveals the natural landscape — what fraction of pMSSM space is viable, where the constraints bite hardest, and what phenomenological patterns emerge naturally.

**Configuration:** [configs/phase1_flat_config.yaml](../configs/phase1_flat_config.yaml)
- Prior: `flat` (uniform random sampling within parameter bounds)
- 500 models per scan × 4 seeds = 2000 total models
- Seeds: 42, 137, 256, 999 (different random sequences for statistical independence)
- All 19 parameters sampled within the ranges listed in Section 2.1

**Expected yields (based on seed42 results):**
- SPheno convergence: ~8% → ~160 valid spectra out of 2000
- After Higgs mass cut: ~40-50%  of valid spectra → ~65-80
- After all cuts: ~30-40% of Higgs-passing → ~20-50 models surviving

**Commands (parallel execution — 3 remaining seeds run simultaneously on 3 cores):**
```bash
# Enter the pixi environment
cd Run3ModelGen && pixi shell && source build/setup.sh && cd ..

# Run all remaining Phase 1 seeds in parallel (max 10 workers)
python run_scans.py --phase 1 --max-workers 10

# Or run individual seeds manually:
# genModels.py --config_file configs/phase1_flat_config.yaml --scan_dir scans/phase1/scan_seed137 --seed 137
# genModels.py --config_file configs/phase1_flat_config.yaml --scan_dir scans/phase1/scan_seed256 --seed 256
# genModels.py --config_file configs/phase1_flat_config.yaml --scan_dir scans/phase1/scan_seed999 --seed 999
```

**Runtime:** ~12-15 minutes total (3 scans in parallel), vs ~40-45 minutes sequential.

**Analysis:** Run `analysis/analyze_phase1.py` on the merged ntuples. Produces:
- Pipeline success rate table
- Cutflow table (quality → neutralino LSP → Higgs → relic density → B-physics → SModelS → all)
- 6 diagnostic plots: M1 vs M2, M1 vs mu, Higgs mass distribution, relic density distribution, LSP composition pie chart, mA vs tan(beta)

### 4.2 Phase 2: Targeted MCMC Scans (4 × 500 models)

**Purpose:** Use Markov Chain Monte Carlo sampling with physics constraints as the likelihood function. This concentrates sampling in physically viable regions, dramatically improving the yield of interesting models. Each scan targets a specific phenomenological region.

**MCMC algorithm:** Metropolis-Hastings with Gaussian proposals. At each step:
1. Propose new parameters by adding Gaussian noise (width = proposal_width) to current point
2. Run the full physics pipeline on the proposed point
3. Compute likelihood from constraints (gaussian or upper_bound types)
4. Accept with probability min(1, L_new / L_old)

All Phase 2 scans use the same 4 constraints (Higgs mass, relic density, BR(b→sγ), BR(Bs→μμ)) with `burn_in: 50` and `accept_invalid: false`.

#### Phase 2a: Light Electroweakinos
**Config:** [configs/phase2a_ewkino_config.yaml](../configs/phase2a_ewkino_config.yaml)

**Physics target:** Models with neutralinos and charginos within LHC Run 3 reach (<1 TeV). These are the most accessible SUSY particles at the LHC via electroweak pair production (pp → χ̃₂⁰χ̃₁± → WZ/Wh + MET).

**Key parameter choices:**
| Parameter | Range | Rationale |
|-----------|-------|-----------|
| M_1 | [-800, 800] | Narrowed to keep LSP light (<800 GeV) |
| M_2 | [-800, 800] | Keep wino states within reach |
| mu | [-1500, 1500] | Allow both Higgsino and mixed scenarios |
| M_3 | [2000, 4000] | Decouple gluino (not the target) |
| meL, meR | [200, 2000] | Allow sleptons to mediate decays |
| mqL3, mtR, mbR | [500, 2000] | Keep 3rd gen squarks moderate |

**Proposal widths:** M_1=40, M_2=40, mu=75 (tight for electroweakino masses to explore fine structure), tanb=3, AT=400, mA=100
**max_attempts:** 30000

#### Phase 2b: Light Stops and Sbottoms
**Config:** [configs/phase2b_stop_config.yaml](../configs/phase2b_stop_config.yaml)

**Physics target:** Models with stop_1 and/or sbottom_1 masses below ~1.2 TeV, exploiting the large top Yukawa coupling to achieve natural EWSB. Stop pair production is a flagship LHC search: pp → t̃₁t̃₁* → tt̄ + MET or bb̄ + MET.

**Key parameter choices:**
| Parameter | Range | Rationale |
|-----------|-------|-----------|
| mqL3 | [200, 1500] | Direct control of left-handed stop/sbottom mass |
| mtR | [200, 1500] | Right-handed stop mass |
| mbR | [200, 1500] | Right-handed sbottom mass |
| AT | [-6000, 6000] | Large |AT| drives stop mixing, lowers stop_1 mass |
| M_3 | [1000, 3000] | Allow lighter gluino for gluino→stop cascade searches |
| M_1, M_2 | [-1500, 1500] | Broader to allow various LSP configurations |
| meL, meR | [500, 2000] | Sleptons somewhat decoupled |

**Proposal widths:** mqL3=65, mtR=65, mbR=65 (fine-grained for 3rd gen masses), AT=300, M_1=75, M_2=75
**max_attempts:** 30000

#### Phase 2c: Light Sleptons
**Config:** [configs/phase2c_slepton_config.yaml](../configs/phase2c_slepton_config.yaml)

**Physics target:** Models with selectrons/smuons below ~600 GeV. Direct slepton pair production (pp → ẽ⁺ẽ⁻ → ℓ⁺ℓ⁻ + MET) is a clean signature at the LHC with low backgrounds.

**Key parameter choices:**
| Parameter | Range | Rationale |
|-----------|-------|-----------|
| meL | [100, 700] | Light left-handed sleptons |
| meR | [100, 700] | Light right-handed sleptons |
| M_1 | [-600, 600] | Bino LSP lighter than sleptons for decay chain |
| M_2 | [-1000, 1000] | Allow moderate wino for chargino-mediated decays |
| M_3 | [2000, 4000] | Decouple gluino |

**Proposal widths:** meL=30, meR=30, M_1=30 (very tight for precise slepton/LSP mass relationship), M_2=50
**max_attempts:** 30000

#### Phase 2d: Compressed Spectra
**Config:** [configs/phase2d_compressed_config.yaml](../configs/phase2d_compressed_config.yaml)

**Physics target:** Models with small mass splittings between the LSP and the next-lightest SUSY particle (NLSP). These are experimentally challenging (soft decay products, disappearing tracks, monojet signatures) but are theoretically well-motivated and represent a blind spot of current LHC searches.

**Key parameter choices:**
| Parameter | Range | Rationale |
|-----------|-------|-----------|
| M_1 | [-500, 500] | Light LSP |
| M_2 | [[-500,-80],[80,500]] | Gap around 0 avoids unphysical region; close to M_1 for compression |
| mu | [[-1000,-80],[80,1000]] | Gap around 0; near M_1/M_2 for Higgsino compression |
| M_3 | [2000, 4000] | Decouple gluino |
| mA | [300, 2000] | Moderate pseudoscalar Higgs |

**Proposal widths:** M_1=25, M_2=25, mu=25 (very tight — the physics lives in the 10-50 GeV mass splitting regime, so we need fine navigation)
**max_attempts:** 40000 (higher because compressed region is harder to find)

### 4.3 Phase 2 Commands (parallel — all 4 MCMC scans run simultaneously on 4 cores)
```bash
cd Run3ModelGen && pixi shell && source build/setup.sh && cd ..

# Run all Phase 2 MCMC scans in parallel (max 10 workers, uses 4)
python run_scans.py --phase 2 --max-workers 10

# Or run both phases sequentially (Phase 1 then Phase 2), each phase parallelized:
python run_scans.py --phase all --max-workers 10

# Or run individual scans manually:
# genModels.py --config_file configs/phase2a_ewkino_config.yaml --scan_dir scans/phase2a/scan --seed 42
# genModels.py --config_file configs/phase2b_stop_config.yaml --scan_dir scans/phase2b/scan --seed 42
# genModels.py --config_file configs/phase2c_slepton_config.yaml --scan_dir scans/phase2c/scan --seed 42
# genModels.py --config_file configs/phase2d_compressed_config.yaml --scan_dir scans/phase2d/scan --seed 42
```

### 4.4 Parallel Execution Strategy

Since `genModels.py` processes models sequentially (single-threaded), we parallelise at the **job level** using `run_scans.py`, which spawns up to 10 concurrent subprocesses via Python's `concurrent.futures.ProcessPoolExecutor`.

**Resource allocation (max 10 cores):**

| Phase | Jobs | Cores used | Wall-clock speedup |
|-------|------|------------|-------------------|
| Phase 1 (remaining) | 3 flat scans (seeds 137, 256, 999) | 3 | 3× (15 min vs 45 min) |
| Phase 2 | 4 MCMC scans (2a–2d) | 4 | 4× |
| Phase all | Phase 1 then Phase 2 | 3 then 4 | Sequential phases, parallel within |

**Key details:**
- Each `genModels.py` instance is a single-core process; no shared memory or file contention between jobs
- Each job writes to its own `scan_dir`, so there are no file-locking issues
- The `--max-workers 10` flag caps concurrency at 10 cores (default)
- Jobs have a 2-hour timeout as a safety net
- The runner prints real-time start/finish per job and a summary table at the end

**Script location:** [run_scans.py](../run_scans.py)

```bash
# Dry run — see what would be executed
python run_scans.py --phase all --max-workers 10 --dry-run

# Full execution
python run_scans.py --phase all --max-workers 10
```

---

## 5. Physics Categories

Models surviving all cuts are classified into 9 categories (non-mutually exclusive). Full definitions: [docs/PHYSICS_CATEGORIES.md](PHYSICS_CATEGORIES.md).

| # | Category | Selection criteria | LHC signatures |
|---|----------|-------------------|----------------|
| 1 | Bino LSP + light EWKinos | LSP_type==1, \|m_χ₂⁰\|<1 TeV, \|m_χ₁±\|<1 TeV | Multi-lepton + MET, WZ + MET, Wh + MET |
| 2 | Wino-like compressed | LSP_type==2, Δm(χ₁±,χ₁⁰)<20 GeV | Disappearing tracks, soft leptons + MET |
| 3 | Higgsino-like compressed | LSP_type==3, Δm(χ₂⁰,χ₁⁰)<30 GeV | Soft leptons + MET, VBF + MET |
| 4 | Light stop | \|m_t̃₁\|<1.2 TeV, Δm(t̃₁,χ₁⁰)>20 GeV | Top pairs + MET, single-lepton + jets + MET |
| 5 | Light sbottom | \|m_b̃₁\|<1.2 TeV, Δm(b̃₁,χ₁⁰)>20 GeV | b-jets + MET |
| 6 | Light sleptons | min(\|m_ẽ_L\|,\|m_ẽ_R\|)<600 GeV | Opposite-sign dileptons + MET |
| 7 | Compressed EWKino | Δm(χ₁±,χ₁⁰)<50 GeV | Soft leptons, disappearing tracks, monojet |
| 8 | Compressed stop | Δm(t̃₁,χ₁⁰)<200 GeV | Charm-tagged jets + MET, monojet |
| 9 | Heavy Higgs accessible | \|m_H\|<1 TeV or \|m_A\|<1 TeV | Ditau resonance, diboson, di-b-jet |

---

## 6. Analysis Plan

### 6.1 Phase 1 Analysis (after all 4 flat scans)

**Script:** [analysis/analyze_phase1.py](../analysis/analyze_phase1.py)

**Steps:**
1. Load and merge all 4 ntuple files
2. Compute pipeline success rates (SPheno, Softsusy, micrOMEGAs, SuperISO, GM2Calc, FeynHiggs, SModelS)
3. Apply sequential cuts and print cutflow table
4. Generate diagnostic plots:
   - M_1 vs M_2 scatter (pass/fail colored)
   - M_1 vs mu scatter (pass/fail colored)
   - Higgs mass distribution (all valid vs passing models)
   - Relic density distribution (log scale)
   - LSP composition pie chart (Bino/Wino/Higgsino)
   - mA vs tan(beta) scatter
5. Document findings in ANALYSIS_NOTES.md and SCAN_LOG.md

**Key questions Phase 1 should answer:**
- What fraction of the flat pMSSM space is experimentally viable?
- Which constraints are most restrictive? (Expected: relic density and Higgs mass)
- What is the natural distribution of LSP types?
- Are there visible correlations between parameters and constraint satisfaction?
- Do the Phase 2 target regions look reasonable, or should they be adjusted?

### 6.2 Phase 2 Analysis (after each MCMC scan)

**Script:** `analysis/analyze_phase2.py` (to be created)

**Steps:**
1. Load each Phase 2 ntuple separately (and also merged)
2. Check MCMC performance: acceptance rate, autocorrelation, chain convergence
3. Apply same quality + physics + SModelS cuts as Phase 1
4. Classify models into the 9 categories
5. Produce mass spectrum distributions and mass-splitting distributions for each category
6. Generate SModelS exclusion maps in relevant mass planes
7. Compare Phase 2 results to Phase 1: are there new regions not covered by flat sampling?

### 6.3 Final Classification and Model Extraction (Step 3-4)

1. Merge all Phase 1 + Phase 2 ntuples
2. Apply all cuts, classify into categories, report populations
3. Identify the "most interesting" models per category (e.g., lightest stop, most compressed spectrum, highest dark matter co-annihilation)
4. Extract SLHA files using `extractModels.py`:
   ```bash
   extractModels.py --scan_dir <scan_dir> --root_file <ntuple> \
     --selection "<awkward array cut string>"
   ```
5. Organize extracted models in `results/selected_models/` by category
6. Produce publication-quality summary plots

---

## 7. Execution Status

### Completed
- [x] Project directory structure and all documentation files
- [x] Run3ModelGen build (pixi + cmake, SPheno, Softsusy, micrOMEGAs, SuperISO, GM2Calc, FeynHiggs, SModelS all compiled)
- [x] Smoke test (5 flat models, verified full pipeline end-to-end, ntuple with 1131 branches)
- [x] All scan configs created (phase1 flat + phase2a-d MCMC)
- [x] Analysis script: analyze_phase1.py
- [x] Phase 1 scan seed42: **COMPLETE** — 500 models, 40 SPheno successes (8%), ntuple created

### In Progress
- [ ] Phase 1 scans: seeds 137, 256, 999 (pending execution)

### Pending
- [ ] Phase 1 analysis: run analyze_phase1.py on all 4 ntuples, document findings
- [ ] Phase 2a: Light electroweakino MCMC scan (500 models)
- [ ] Phase 2b: Light stop/sbottom MCMC scan (500 models)
- [ ] Phase 2c: Light slepton MCMC scan (500 models)
- [ ] Phase 2d: Compressed spectra MCMC scan (500 models)
- [ ] Phase 2 analysis per scan + combined
- [ ] Final classification and model extraction
- [ ] Summary document with conclusions

### Key Measurements from Seed42 Scan
- 500 models generated, 40 passed SPheno (8.0% spectrum convergence rate)
- 40 passed full pipeline (micrOMEGAs, SuperISO, GM2Calc, FeynHiggs, SModelS)
- Runtime: ~12 minutes
- Once SPheno succeeds, downstream tool failure rate is ~0%

---

## 8. Documentation Strategy

Documentation happens **continuously during execution**, not as a final step. After every action that produces results, findings are recorded before moving on.

| Document | Updated when | Content |
|----------|-------------|---------|
| [SCAN_LOG.md](SCAN_LOG.md) | After every scan completes | Config, seed, runtime, pass rates, observations, ntuple path |
| [ANALYSIS_NOTES.md](ANALYSIS_NOTES.md) | After every analysis run | Physics observations, constraint behavior, category populations |
| [PHYSICS_CATEGORIES.md](PHYSICS_CATEGORIES.md) | After Phase 1 analysis; after classification | Category definitions, cut thresholds, refinements from data |
| [NTUPLE_VARIABLES.md](NTUPLE_VARIABLES.md) | Once (Step 0); if new variables discovered | Full branch reference for ROOT ntuples |
| [README.md](../README.md) | After each major milestone | Project status, build instructions, key findings |
| `.claude/memory/MEMORY.md` | After each phase | Cross-session persistence: key paths, commands, observations |

**Rule:** No step is complete until its findings are documented.

---

## 9. Technical Reference

### 9.1 Build and Environment Setup
```bash
cd /scratch/users/jwuerzin/pMSSM/SUSY_agent/Run3ModelGen
export PATH="/u/jwuerzin/.pixi/bin:$PATH"
pixi shell          # Activates conda environment with all dependencies
cmake -S source -B build
cmake --build build -j8
source build/setup.sh   # Puts all tools on PATH
cd ..               # Return to SUSY_agent root
```

### 9.2 Running Scans from Outside pixi
```bash
export PATH="/u/jwuerzin/.pixi/bin:$PATH"
pixi run -e default bash -c "source build/setup.sh && cd /scratch/users/jwuerzin/pMSSM/SUSY_agent && <command>"
```

### 9.3 Monitoring Running Scans
```bash
ps aux | grep genModels                          # Is it running?
ls scans/phase1/scan_seedN/input/ | wc -l        # How many models processed?
ls scans/phase1/scan_seedN/SPheno/ | wc -l       # How many passed SPheno?
ls scans/phase1/scan_seedN/micromegas/ | wc -l   # How many passed full pipeline?
```

### 9.4 SModelS Database
- Cached at `Run3ModelGen/official311.pcl` (1.3 GB)
- Contains all published ATLAS + CMS simplified-model upper limits (database v3.1.1)
- First-time use per session compiles Pythia; subsequent models reuse the compilation

### 9.5 Ntuple Analysis (Python)
```python
import uproot
import awkward as ak

with uproot.open("scans/phase1/scan_seed42/ntuple.0.0.root:susy") as tree:
    data = tree.arrays(library="ak")

# Example: select models with valid spectrum and Higgs mass in window
valid = (data['SP_m_h'] != -1) & (data['FH_m_h'] > 122) & (data['FH_m_h'] < 128)
print(f"Models passing Higgs cut: {ak.sum(valid)}")
```
