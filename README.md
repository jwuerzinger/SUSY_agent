# SUSY_agent

Systematic investigation of the pMSSM (phenomenological MSSM) parameter space to identify interesting SUSY models as targets for LHC Run 3 searches.

## Overview

This project uses the [Run3ModelGen](Run3ModelGen/) framework to:
1. Generate pMSSM model points by sampling the 19-dimensional parameter space
2. Evaluate each model through a pipeline of physics tools (SPheno, Softsusy, FeynHiggs, micrOMEGAs, SuperISO, GM2Calc, SModelS)
3. Apply experimental constraints (Higgs mass, dark matter relic density, B-physics, LHC exclusions)
4. Classify surviving models into phenomenological categories relevant for LHC searches

## Directory Structure

```
SUSY_agent/
  Run3ModelGen/          # Submodule: pMSSM model generation framework
  configs/               # YAML scan configurations (flat, MCMC, refinement)
  analysis/              # Python analysis scripts
  scans/                 # Scan output directories
    phase1/              # Flat exploration scans (4 seeds)
    phase2a-d/           # Targeted MCMC scans (3-4 seeds each)
    phase3a-c/           # Refinement scans (co-annihilation, A-funnel, compressed stop)
  results/
    SUMMARY.md           # Full physics summary and conclusions
    plots/               # Generated figures
    benchmarks/          # Extracted SLHA files (1 per category) + summary CSV
  docs/
    INVESTIGATION_PLAN.md # Full methodology and execution status
    SCAN_LOG.md          # Running log of all scans
    PHYSICS_CATEGORIES.md # Category definitions and cuts
    NTUPLE_VARIABLES.md  # Full ntuple variable reference
    ANALYSIS_NOTES.md    # Physics observations per phase
  run_scans.py           # Parallel scan launcher
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

## Status: COMPLETE (2026-03-03)

All scan phases finished. Full results in [results/SUMMARY.md](results/SUMMARY.md).

- [x] Project setup and documentation
- [x] Framework build (pixi + cmake, all 6 physics tools + SModelS)
- [x] Phase 1: Flat exploration (4 x 500 models) — 5 pass all cuts
- [x] Phase 2: Targeted MCMC scans (4 types x 3 seeds each) — 451 pass all cuts
- [x] Phase 3: Refinement scans (A-funnel, co-annihilation, compressed stop) — 2 pass all cuts
- [x] Final classification with all constraints (including LEP chargino limit)
- [x] Benchmark SLHA files extracted (9 categories)

### Key Results

| Metric | Value |
|--------|-------|
| Total models evaluated | 13,523 |
| Passing all cuts | **458** |
| Physics categories populated | 9/9 |
| LSP composition | 78% Wino, 15% Higgsino, 6% Bino |
| Models excluded by current LHC limits | ~2% |

### Top Run 3 Search Priorities
1. **Disappearing tracks** — 359 Wino-compressed models with dm(chi1+, LSP) < 20 GeV
2. **Slepton pair production** — 259 models with m(slepton) < 600 GeV
3. **Light stop/sbottom** — 198 stop, 290 sbottom models below 1.2 TeV
4. **Heavy Higgs ditau** — 60 models with mH/mA < 1 TeV
5. **Compressed stop** — 7 stealth stop models (dm < 200 GeV)
