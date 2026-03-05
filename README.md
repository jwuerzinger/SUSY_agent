# SUSY_agent

**DISCLAIMER**: This repo is 100% generated with Claude code!

Systematic investigation of the pMSSM (phenomenological MSSM) parameter space to identify viable SUSY models and gaps in the ATLAS search programme at the LHC.

**[Comprehensive findings document](results/COMPLETE_FINDINGS.md)** — full summary of all results, ATLAS blind spots, Run 3 search proposals, and benchmark spectra.

## Overview

This project uses the [Run3ModelGen](Run3ModelGen/) framework to:
1. Generate pMSSM model points by sampling the 19-dimensional parameter space
2. Evaluate each model through a pipeline of physics tools (SPheno, Softsusy, FeynHiggs, micrOMEGAs, SuperISO, GM2Calc, SModelS)
3. Apply experimental constraints (Higgs mass, dark matter relic density, B-physics, LHC exclusions)
4. Classify surviving models into phenomenological categories relevant for LHC searches
5. Assess ATLAS/CMS coverage using SModelS and identify blind spots with concrete Run 3 search proposals

## Directory Structure

```
SUSY_agent/
  Run3ModelGen/          # Submodule: pMSSM model generation framework
  configs/               # YAML scan configurations (flat, MCMC, grid)
  analysis/              # Python analysis scripts (9 scripts)
  scans/                 # Scan output directories (48 ntuple files)
    phase1/              # Flat exploration scans (4 seeds)
    phase2a-d/           # Targeted MCMC scans (3-4 seeds each)
    phase3a-c/           # Refinement scans (co-annihilation, A-funnel, compressed stop)
    phase4a-e/           # ATLAS blind spot targeting (3 seeds each)
    phase4c_grid/        # Grid scan: slepton + Bino (3 seeds)
    phase4d_grid/        # Grid scan: compressed stop (3 seeds)
  results/
    COMPLETE_FINDINGS.md # Comprehensive findings summary (this is the main document)
    SUMMARY.md           # Physics summary (Phases 1-3)
    plots/               # Classification and summary figures (15 PNGs)
    benchmarks/          # Category benchmark SLHA files (9) + summary CSV
    atlas_coverage/      # SModelS coverage analysis (2 CSVs, 2 reports, 8 plots)
    atlas_proposals/     # Run 3 search proposals (2 reports, 35 benchmarks, 23 plots)
  docs/
    INVESTIGATION_PLAN.md # Full methodology and execution status
    FOLLOWUP_PLAN.md     # Follow-up work priorities and lessons learned
    SCAN_LOG.md          # Complete log of all scans
    ANALYSIS_NOTES.md    # Detailed physics observations per phase
    PHYSICS_CATEGORIES.md # Category definitions and cuts
    NTUPLE_VARIABLES.md  # Full ntuple variable reference
  run_scans.py           # Parallel scan launcher (flat, MCMC, grid)
  run_ntupling.py        # Post-hoc ntuple generation
```

## Setup

```bash
# Build the framework
cd Run3ModelGen
pixi shell
cmake -S source -B build
cmake --build build -j8
source build/setup.sh

# Run a scan
cd ..
genModels.py --config_file configs/phase1_flat_config.yaml --scan_dir scans/phase1/scan_seed42 --seed 42
```

## Running Scans

### Quick start (interactive)

```bash
cd Run3ModelGen && pixi shell && source build/setup.sh && cd ..
python run_scans.py --phase all --max-workers 10
```

### Running via `screen` (recommended for long scans)

Scans take 15+ minutes per phase. Use `screen` so they survive disconnects.

```bash
# 1. Start a named screen session
screen -S susy

# 2. Enter the pixi environment and run scans
cd /scratch/users/jwuerzin/pMSSM/SUSY_agent/Run3ModelGen
pixi shell
source build/setup.sh
cd ..

# 3a. Run scans directly
python run_scans.py --phase all --max-workers 10

# 3b. OR let Claude Code continue the full plan (scans + analysis)
CLAUDE=/u/jwuerzin/.vscode-server/extensions/anthropic.claude-code-2.1.56-linux-x64/resources/native-binary/claude
$CLAUDE --dangerously-skip-permissions -p "Continue with the investigation plan..."

# 4. Detach from screen: press Ctrl+A then D
# 5. Reconnect later:
screen -r susy
```

### Running Claude Code autonomously in `screen`

To have Claude Code execute the remaining investigation plan end-to-end:

```bash
screen -S susy-agent
cd /scratch/users/jwuerzin/pMSSM/SUSY_agent/Run3ModelGen
pixi shell
source build/setup.sh
cd ..
CLAUDE=/u/jwuerzin/.vscode-server/extensions/anthropic.claude-code-2.1.56-linux-x64/resources/native-binary/claude
$CLAUDE --dangerously-skip-permissions -p "Continue with the investigation plan in docs/INVESTIGATION_PLAN.md. Run the remaining Phase 1 scans (seeds 137, 256, 999) in parallel, then run the Phase 1 analysis, then run Phase 2 MCMC scans in parallel, then analyse. Use run_scans.py with --max-workers 10 for parallel execution. Document findings as you go."
```

Then detach with `Ctrl+A, D`. Reconnect anytime with `screen -r susy-agent`.

### Useful screen commands

| Command | Action |
|---------|--------|
| `screen -S name` | Start a named session |
| `Ctrl+A, D` | Detach (leave running) |
| `screen -r name` | Reattach to session |
| `screen -ls` | List all sessions |
| `screen -X -S name quit` | Kill a session |

## Physics Categories

Models are classified into categories based on their phenomenology (see [docs/PHYSICS_CATEGORIES.md](docs/PHYSICS_CATEGORIES.md)):
- Light electroweakinos (Bino/Wino/Higgsino LSP)
- Light stops/sbottoms
- Light sleptons
- Compressed spectra (small mass splittings)
- Heavy Higgs accessible

## Status: COMPLETE (2026-03-04)

All scan phases and ATLAS blind spot analysis finished. See **[results/COMPLETE_FINDINGS.md](results/COMPLETE_FINDINGS.md)** for the full findings.

- [x] Project setup and documentation
- [x] Framework build (pixi + cmake, all 6 physics tools + SModelS)
- [x] Phase 1: Flat exploration (4 x 500 models) — 5 pass all cuts
- [x] Phase 2: Targeted MCMC scans (4 types x 3-4 seeds each) — 451 pass all cuts
- [x] Phase 3: Refinement scans (A-funnel, co-annihilation, compressed stop) — 2 pass all cuts
- [x] Phase 4: ATLAS blind spot targeting (5 types x 3 seeds) — 1,605 new passing models
- [x] Phase 4 grid scans for narrow corridors — 0 new models (physics constraints too tight)
- [x] Final classification with all constraints (including LEP chargino limit)
- [x] Benchmark SLHA files extracted (9 categories + 35 gap-specific + 30 mass-grid)
- [x] ATLAS coverage assessment (SModelS reinterpretation)
- [x] Five ATLAS blind spots identified and characterised
- [x] Run 3 search proposals with signal regions, yield estimates, and benchmarks
- [x] Direct detection complementarity analysis

### Key Results

| Metric | Value |
|--------|-------|
| Total models evaluated | 24,188 |
| Passing all cuts | **2,063** |
| Physics categories populated | 9/9 |
| LSP composition | 49% Wino, 48% Higgsino, 3% Bino |
| Invisible to ATLAS (SModelS tier 0) | **66.5%** |
| ATLAS blind spots identified | 5 |
| Truly dark models (LHC + DD invisible) | 3 |
| Models excluded by current LHC limits | ~2% |

### ATLAS Blind Spots and Run 3 Search Priorities

| Gap | Description | Models | Priority | Proposed search |
|-----|-------------|:------:|----------|-----------------|
| A | Compressed Wino | 526 | HIGH | Disappearing tracks (pixel tracklets) |
| B | Compressed Higgsino | 737 | HIGH | ISR + soft dileptons (mll binning) |
| C | Light sleptons | 497 | MEDIUM | Extended dilepton + MET (mT2) |
| D | Compressed stop | 2 | MEDIUM | Novel displaced vertex + b-jet |
| E | Complex EWKino | 80 | LOW | Multi-lepton cascades |

Full signal region definitions, yield estimates, and benchmark SLHA files in [results/atlas_proposals/RUN3_SEARCH_PROPOSALS.md](results/atlas_proposals/RUN3_SEARCH_PROPOSALS.md).
