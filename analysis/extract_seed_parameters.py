#!/usr/bin/env python3
"""Extract pMSSM input parameters from known viable models for importance sampling.

Reads model_atlas_coverage.csv to identify seed models, then extracts EXTPAR
entries from their SLHA input files.

Output:
  results/seeds_phase5a.csv  — Bino-LSP seeds (for slepton co-annihilation)
  results/seeds_phase5b.csv  — Compressed-stop seeds (m_t1 - m_lsp < 300 GeV)
"""

import csv
import os
import sys
import pyslha

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COVERAGE_CSV = os.path.join(PROJECT_ROOT, "results", "atlas_coverage", "model_atlas_coverage.csv")

# EXTPAR indices → parameter names (matching YAML config keys)
EXTPAR_MAP = {
    1: "M_1",
    2: "M_2",
    3: "M_3",
    11: "AT",
    12: "Ab",
    13: "Atau",
    23: "mu",
    25: "tanb",
    26: "mA",
    31: "meL",
    33: "mtauL",
    34: "meR",
    36: "mtauR",
    41: "mqL1",
    43: "mqL3",
    44: "muR",
    46: "mtR",
    47: "mdR",
    49: "mbR",
}

PARAM_NAMES = [EXTPAR_MAP[k] for k in sorted(EXTPAR_MAP.keys())]


def extract_params(slha_path):
    """Read EXTPAR block from an SLHA input file, return dict of parameter values."""
    try:
        with open(slha_path) as f:
            doc = pyslha.readSLHA(f.read(), ignorenomass=True)
    except Exception as e:
        print(f"  WARNING: could not parse {slha_path}: {e}")
        return None

    if "EXTPAR" not in doc.blocks:
        print(f"  WARNING: no EXTPAR block in {slha_path}")
        return None

    extpar = doc.blocks["EXTPAR"]
    params = {}
    for idx, name in EXTPAR_MAP.items():
        if idx in extpar:
            params[name] = float(extpar[idx])
        else:
            print(f"  WARNING: missing EXTPAR[{idx}] ({name}) in {slha_path}")
            return None
    return params


def select_seeds(coverage_csv):
    """Read coverage CSV and return two lists of (scan_dir, model_id) tuples."""
    seeds_5a = []  # Bino LSP
    seeds_5b = []  # Compressed stop

    with open(coverage_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            scan_dir = row["scan_dir"]
            model_id = row["model_id"]
            lsp_type = int(row["lsp_type"])
            m_t1 = float(row["m_t1"])
            m_lsp = float(row["m_lsp"])

            if lsp_type == 1:  # Bino LSP
                seeds_5a.append((scan_dir, model_id))
            if m_t1 - m_lsp < 300:
                seeds_5b.append((scan_dir, model_id))

    return seeds_5a, seeds_5b


def write_seed_csv(seeds, output_path):
    """Extract parameters for each seed and write to CSV."""
    rows = []
    for scan_dir, model_id in seeds:
        # Find the SLHA input file — scan_dir is like "scan_seed137",
        # need to locate it under scans/phase*/
        slha_path = None
        for phase_dir in sorted(os.listdir(os.path.join(PROJECT_ROOT, "scans"))):
            candidate = os.path.join(PROJECT_ROOT, "scans", phase_dir, scan_dir, "input", f"{model_id}.slha")
            if os.path.isfile(candidate):
                slha_path = candidate
                break

        if slha_path is None:
            print(f"  WARNING: SLHA file not found for {scan_dir}/{model_id}")
            continue

        params = extract_params(slha_path)
        if params is None:
            continue

        params["scan_dir"] = scan_dir
        params["model_id"] = model_id
        rows.append(params)

    # Write CSV
    fieldnames = ["scan_dir", "model_id"] + PARAM_NAMES
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Wrote {len(rows)} seeds to {output_path}")
    return len(rows)


def main():
    print("Extracting seed parameters for importance sampling...")
    print(f"  Coverage CSV: {COVERAGE_CSV}")

    if not os.path.isfile(COVERAGE_CSV):
        print(f"ERROR: {COVERAGE_CSV} not found. Run atlas_coverage.py first.")
        sys.exit(1)

    seeds_5a, seeds_5b = select_seeds(COVERAGE_CSV)
    print(f"  Phase5a seeds (Bino LSP): {len(seeds_5a)}")
    print(f"  Phase5b seeds (compressed stop): {len(seeds_5b)}")

    out_5a = os.path.join(PROJECT_ROOT, "results", "seeds_phase5a.csv")
    out_5b = os.path.join(PROJECT_ROOT, "results", "seeds_phase5b.csv")

    n_5a = write_seed_csv(seeds_5a, out_5a)
    n_5b = write_seed_csv(seeds_5b, out_5b)

    print(f"\nDone. Extracted {n_5a} phase5a seeds, {n_5b} phase5b seeds.")


if __name__ == "__main__":
    main()
