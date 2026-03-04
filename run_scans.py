#!/usr/bin/env python3
"""
Parallel scan runner for pMSSM model generation.

Runs multiple genModels.py instances in parallel using subprocess,
with a configurable maximum number of concurrent workers (cores).

Usage:
    python run_scans.py --phase 1          # Run all Phase 1 flat scans
    python run_scans.py --phase 2          # Run all Phase 2 MCMC scans
    python run_scans.py --phase all        # Run Phase 1, then Phase 2
    python run_scans.py --jobs jobs.json   # Run custom job list
    python run_scans.py --max-workers 5    # Limit to 5 parallel processes

Requires: must be run inside the pixi environment with build/setup.sh sourced.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

# ── Job definitions ──────────────────────────────────────────────────────────

PHASE1_JOBS = [
    {
        "name": "phase1_seed137",
        "config": "configs/phase1_flat_config.yaml",
        "scan_dir": "scans/phase1/scan_seed137",
        "seed": 137,
    },
    {
        "name": "phase1_seed256",
        "config": "configs/phase1_flat_config.yaml",
        "scan_dir": "scans/phase1/scan_seed256",
        "seed": 256,
    },
    {
        "name": "phase1_seed999",
        "config": "configs/phase1_flat_config.yaml",
        "scan_dir": "scans/phase1/scan_seed999",
        "seed": 999,
    },
]

# Phase 2: split each MCMC scan into multiple seeds to fill 10 workers.
# 3 seeds per scan type × 4 types = 12 jobs, capped to 10 concurrent.
# Each sub-scan produces 500 models; merging later gives 1500 per type.
PHASE2_SEEDS = [42, 137, 256]

PHASE2_JOBS = []
for _seed in PHASE2_SEEDS:
    PHASE2_JOBS.extend([
        {
            "name": f"phase2a_ewkino_s{_seed}",
            "config": "configs/phase2a_ewkino_config.yaml",
            "scan_dir": f"scans/phase2a/scan_seed{_seed}",
            "seed": _seed,
        },
        {
            "name": f"phase2b_stop_s{_seed}",
            "config": "configs/phase2b_stop_config.yaml",
            "scan_dir": f"scans/phase2b/scan_seed{_seed}",
            "seed": _seed,
        },
        {
            "name": f"phase2c_slepton_s{_seed}",
            "config": "configs/phase2c_slepton_config.yaml",
            "scan_dir": f"scans/phase2c/scan_seed{_seed}",
            "seed": _seed,
        },
        {
            "name": f"phase2d_compressed_s{_seed}",
            "config": "configs/phase2d_compressed_config.yaml",
            "scan_dir": f"scans/phase2d/scan_seed{_seed}",
            "seed": _seed,
        },
    ])

# Phase 3: Refinement scans targeting specific gaps identified in Phase 2 analysis.
# 3a: Bino co-annihilation with sleptons
# 3b: A-funnel resonance (mA ~ 2*m_Bino)
# 3c: Compressed stop corridor (dm(stop1, LSP) < 200 GeV)
# Also reruns for failed Phase 2 seeds (phase2c_s314, phase2d_s314)
PHASE3_SEEDS = [42, 137, 256]
PHASE2_RERUN_SEED = 314  # Replace failed seed 256 for phase2c and phase2d

PHASE3_JOBS = [
    # Rerun failed Phase 2 seeds
    {
        "name": f"phase2c_slepton_s{PHASE2_RERUN_SEED}",
        "config": "configs/phase2c_slepton_config.yaml",
        "scan_dir": f"scans/phase2c/scan_seed{PHASE2_RERUN_SEED}",
        "seed": PHASE2_RERUN_SEED,
    },
    {
        "name": f"phase2d_compressed_s{PHASE2_RERUN_SEED}",
        "config": "configs/phase2d_compressed_config.yaml",
        "scan_dir": f"scans/phase2d/scan_seed{PHASE2_RERUN_SEED}",
        "seed": PHASE2_RERUN_SEED,
    },
]
for _seed in PHASE3_SEEDS:
    PHASE3_JOBS.extend([
        {
            "name": f"phase3a_bino_coann_s{_seed}",
            "config": "configs/phase3a_bino_coannihilation_config.yaml",
            "scan_dir": f"scans/phase3a/scan_seed{_seed}",
            "seed": _seed,
        },
        {
            "name": f"phase3b_afunnel_s{_seed}",
            "config": "configs/phase3b_afunnel_config.yaml",
            "scan_dir": f"scans/phase3b/scan_seed{_seed}",
            "seed": _seed,
        },
        {
            "name": f"phase3c_comp_stop_s{_seed}",
            "config": "configs/phase3c_compressed_stop_config.yaml",
            "scan_dir": f"scans/phase3c/scan_seed{_seed}",
            "seed": _seed,
        },
    ])

# Phase 4: Targeted blind-spot scans to densely populate ATLAS gaps.
# 5 scan types × 3 seeds = 15 jobs.
PHASE4_SEEDS = [42, 137, 256]

PHASE4_JOBS = []
for _seed in PHASE4_SEEDS:
    PHASE4_JOBS.extend([
        {
            "name": f"phase4a_wino_s{_seed}",
            "config": "configs/phase4a_wino_mapping.yaml",
            "scan_dir": f"scans/phase4a/scan_seed{_seed}",
            "seed": _seed,
        },
        {
            "name": f"phase4b_higgsino_s{_seed}",
            "config": "configs/phase4b_higgsino_soft.yaml",
            "scan_dir": f"scans/phase4b/scan_seed{_seed}",
            "seed": _seed,
        },
        {
            "name": f"phase4c_slepton_s{_seed}",
            "config": "configs/phase4c_slepton_bino.yaml",
            "scan_dir": f"scans/phase4c/scan_seed{_seed}",
            "seed": _seed,
        },
        {
            "name": f"phase4d_comp_stop_s{_seed}",
            "config": "configs/phase4d_compressed_stop_wino.yaml",
            "scan_dir": f"scans/phase4d/scan_seed{_seed}",
            "seed": _seed,
        },
        {
            "name": f"phase4e_mixed_ewk_s{_seed}",
            "config": "configs/phase4e_mixed_ewkino.yaml",
            "scan_dir": f"scans/phase4e/scan_seed{_seed}",
            "seed": _seed,
        },
    ])

# Phase 4 Grid: Grid-based rescans for corridors where MCMC failed.
# phase4c_grid: slepton+Bino (600 grid points per seed)
# phase4d_grid: compressed stop+Wino (450 grid points per seed)
PHASE4_GRID_SEEDS = [42, 137, 256]

PHASE4_GRID_JOBS = []
for _seed in PHASE4_GRID_SEEDS:
    PHASE4_GRID_JOBS.extend([
        {
            "name": f"phase4c_grid_s{_seed}",
            "config": "configs/phase4c_slepton_bino_grid.yaml",
            "scan_dir": f"scans/phase4c_grid/scan_seed{_seed}",
            "seed": _seed,
            "timeout": 14400,  # 4 hours for grid scans
        },
        {
            "name": f"phase4d_grid_s{_seed}",
            "config": "configs/phase4d_compressed_stop_grid.yaml",
            "scan_dir": f"scans/phase4d_grid/scan_seed{_seed}",
            "seed": _seed,
            "timeout": 14400,  # 4 hours for grid scans
        },
    ])

# ── Worker function ──────────────────────────────────────────────────────────


def run_scan(job: dict, project_root: str) -> dict:
    """Run a single genModels.py scan as a subprocess.

    Args:
        job: Dict with keys: name, config, scan_dir, seed
        project_root: Absolute path to SUSY_agent directory

    Returns:
        Dict with job name, return code, runtime, and output summary.
    """
    cmd = [
        "genModels.py",
        "--config_file", job["config"],
        "--scan_dir", job["scan_dir"],
        "--seed", str(job["seed"]),
    ]

    print(f"[START] {job['name']}: {' '.join(cmd)}")
    t0 = time.time()

    job_timeout = job.get("timeout", 7200)  # default 2h, grid scans use 4h

    try:
        result = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=job_timeout,
        )
        elapsed = time.time() - t0
        status = "SUCCESS" if result.returncode == 0 else "FAILED"

        # Extract last 20 lines of stdout for summary
        stdout_tail = "\n".join(result.stdout.strip().split("\n")[-20:])
        stderr_tail = "\n".join(result.stderr.strip().split("\n")[-10:]) if result.stderr else ""

        print(f"[{status}] {job['name']}: {elapsed:.1f}s (rc={result.returncode})")

        return {
            "name": job["name"],
            "returncode": result.returncode,
            "elapsed_s": round(elapsed, 1),
            "status": status,
            "stdout_tail": stdout_tail,
            "stderr_tail": stderr_tail,
        }

    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        print(f"[TIMEOUT] {job['name']}: exceeded {job_timeout}s limit after {elapsed:.1f}s")
        return {
            "name": job["name"],
            "returncode": -1,
            "elapsed_s": round(elapsed, 1),
            "status": "TIMEOUT",
            "stdout_tail": "",
            "stderr_tail": "Process timed out after 2 hours",
        }
    except Exception as e:
        elapsed = time.time() - t0
        print(f"[ERROR] {job['name']}: {e}")
        return {
            "name": job["name"],
            "returncode": -1,
            "elapsed_s": round(elapsed, 1),
            "status": "ERROR",
            "stdout_tail": "",
            "stderr_tail": str(e),
        }


def run_jobs_parallel(jobs: list, max_workers: int, project_root: str) -> list:
    """Run a list of scan jobs in parallel.

    Args:
        jobs: List of job dicts
        max_workers: Maximum number of concurrent processes
        project_root: Absolute path to SUSY_agent directory

    Returns:
        List of result dicts
    """
    MAX_CORES = 10  # hard cap: never exceed 10 workers
    n_jobs = len(jobs)
    n_workers = min(max_workers, n_jobs, MAX_CORES)
    print(f"\n{'='*60}")
    print(f"Running {n_jobs} scan jobs with {n_workers} parallel workers")
    print(f"{'='*60}\n")

    results = []
    t0 = time.time()

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        future_to_job = {
            executor.submit(run_scan, job, project_root): job
            for job in jobs
        }

        for future in as_completed(future_to_job):
            job = future_to_job[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"[FATAL] {job['name']}: executor error: {e}")
                results.append({
                    "name": job["name"],
                    "returncode": -1,
                    "elapsed_s": 0,
                    "status": "FATAL",
                    "stdout_tail": "",
                    "stderr_tail": str(e),
                })

    total_time = time.time() - t0

    # Print summary
    print(f"\n{'='*60}")
    print(f"SUMMARY — {n_jobs} jobs completed in {total_time:.1f}s")
    print(f"{'='*60}")
    for r in sorted(results, key=lambda x: x["name"]):
        print(f"  {r['name']:25s}  {r['status']:8s}  {r['elapsed_s']:8.1f}s")
    print()

    n_success = sum(1 for r in results if r["status"] == "SUCCESS")
    n_failed = n_jobs - n_success
    print(f"  Succeeded: {n_success}/{n_jobs}")
    if n_failed > 0:
        print(f"  Failed:    {n_failed}/{n_jobs}")
        for r in results:
            if r["status"] != "SUCCESS" and r["stderr_tail"]:
                print(f"    {r['name']}: {r['stderr_tail'][:200]}")
    print()

    return results


# ── CLI ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Run pMSSM scans in parallel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--phase",
        choices=["1", "2", "3", "4", "4grid", "all"],
        help="Which phase to run: 1 (flat), 2 (MCMC), 3 (refinement), 4 (blind-spot), 4grid (grid rescans), or all",
    )
    parser.add_argument(
        "--jobs",
        type=str,
        help="Path to JSON file with custom job list",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=10,
        help="Maximum number of parallel processes (default: 10)",
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default=os.path.dirname(os.path.abspath(__file__)),
        help="Path to SUSY_agent project root",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print jobs that would be run without executing them",
    )

    args = parser.parse_args()

    if not args.phase and not args.jobs:
        parser.error("Must specify --phase or --jobs")

    # Build job list
    jobs = []
    if args.jobs:
        with open(args.jobs) as f:
            jobs = json.load(f)
    elif args.phase == "1":
        jobs = PHASE1_JOBS
    elif args.phase == "2":
        jobs = PHASE2_JOBS
    elif args.phase == "3":
        jobs = PHASE3_JOBS
    elif args.phase == "4":
        jobs = PHASE4_JOBS
    elif args.phase == "4grid":
        jobs = PHASE4_GRID_JOBS
    elif args.phase == "all":
        # Phase 1 first, then Phase 2, then Phase 3, then Phase 4
        pass  # handled below

    # Verify environment
    if not args.dry_run:
        try:
            subprocess.run(
                ["which", "genModels.py"],
                check=True, capture_output=True, text=True,
            )
        except subprocess.CalledProcessError:
            print("ERROR: genModels.py not found on PATH.")
            print("Make sure you are in the pixi environment with build/setup.sh sourced:")
            print("  cd Run3ModelGen && pixi shell && source build/setup.sh && cd ..")
            sys.exit(1)

    if args.dry_run:
        if args.phase == "all":
            for phase_name, phase_jobs in [("Phase 1", PHASE1_JOBS), ("Phase 2", PHASE2_JOBS), ("Phase 3", PHASE3_JOBS), ("Phase 4", PHASE4_JOBS), ("Phase 4 Grid", PHASE4_GRID_JOBS)]:
                print(f"{phase_name} jobs:")
                for j in phase_jobs:
                    print(f"  genModels.py --config_file {j['config']} --scan_dir {j['scan_dir']} --seed {j['seed']}")
                print()
        else:
            for j in jobs:
                print(f"  genModels.py --config_file {j['config']} --scan_dir {j['scan_dir']} --seed {j['seed']}")
        print(f"\nMax workers: {args.max_workers}")
        return

    if args.phase == "all":
        for phase_name, phase_jobs in [("Phase 1: Flat scans", PHASE1_JOBS),
                                        ("Phase 2: MCMC scans", PHASE2_JOBS),
                                        ("Phase 3: Refinement scans", PHASE3_JOBS),
                                        ("Phase 4: Blind-spot scans", PHASE4_JOBS),
                                        ("Phase 4 Grid: Grid rescans", PHASE4_GRID_JOBS)]:
            print(f"\n{phase_name}")
            results = run_jobs_parallel(phase_jobs, args.max_workers, args.project_root)
            n_failed = sum(1 for r in results if r["status"] != "SUCCESS")
            if n_failed > 0:
                print(f"WARNING: {n_failed} {phase_name} jobs failed. Continuing anyway.")
    else:
        run_jobs_parallel(jobs, args.max_workers, args.project_root)


if __name__ == "__main__":
    main()
