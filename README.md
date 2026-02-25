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
  configs/               # YAML scan configurations (flat, MCMC)
  analysis/              # Python analysis scripts
  scans/                 # Scan output directories
    phase1/              # Flat exploration scans
    phase2a-d/           # Targeted MCMC scans
  results/
    plots/               # Generated figures
    selected_models/     # Extracted SLHA files by category
  docs/
    SCAN_LOG.md          # Running log of all scans
    PHYSICS_CATEGORIES.md # Category definitions and cuts
    NTUPLE_VARIABLES.md  # Full ntuple variable reference
    ANALYSIS_NOTES.md    # Physics observations per phase
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

## Physics Categories

Models are classified into categories based on their phenomenology (see [docs/PHYSICS_CATEGORIES.md](docs/PHYSICS_CATEGORIES.md)):
- Light electroweakinos (Bino/Wino/Higgsino LSP)
- Light stops/sbottoms
- Light sleptons
- Compressed spectra (small mass splittings)
- Heavy Higgs accessible

## Status

- [x] Project setup and documentation
- [ ] Framework build
- [ ] Phase 1: Flat exploration (4 x 500 models)
- [ ] Phase 2: Targeted MCMC scans (4 x 500 models)
- [ ] Classification and model extraction
