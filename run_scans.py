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

PHASE2_JOBS = [
    {
        "name": "phase2a_ewkino",
        "config": "configs/phase2a_ewkino_config.yaml",
        "scan_dir": "scans/phase2a/scan",
        "seed": 42,
    },
    {
        "name": "phase2b_stop",
        "config": "configs/phase2b_stop_config.yaml",
        "scan_dir": "scans/phase2b/scan",
        "seed": 42,
    },
    {
        "name": "phase2c_slepton",
        "config": "configs/phase2c_slepton_config.yaml",
        "scan_dir": "scans/phase2c/scan",
        "seed": 42,
    },
    {
        "name": "phase2d_compressed",
        "config": "configs/phase2d_compressed_config.yaml",
        "scan_dir": "scans/phase2d/scan",
        "seed": 42,
    },
]

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

    try:
        result = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=7200,  # 2 hour timeout per scan
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
        print(f"[TIMEOUT] {job['name']}: exceeded 2h limit after {elapsed:.1f}s")
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
    n_jobs = len(jobs)
    n_workers = min(max_workers, n_jobs)
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
        choices=["1", "2", "all"],
        help="Which phase to run: 1 (flat), 2 (MCMC), or all (1 then 2)",
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
    elif args.phase == "all":
        # Phase 1 first, then Phase 2
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
            print("Phase 1 jobs:")
            for j in PHASE1_JOBS:
                print(f"  genModels.py --config_file {j['config']} --scan_dir {j['scan_dir']} --seed {j['seed']}")
            print("\nPhase 2 jobs (after Phase 1 completes):")
            for j in PHASE2_JOBS:
                print(f"  genModels.py --config_file {j['config']} --scan_dir {j['scan_dir']} --seed {j['seed']}")
        else:
            for j in jobs:
                print(f"  genModels.py --config_file {j['config']} --scan_dir {j['scan_dir']} --seed {j['seed']}")
        print(f"\nMax workers: {args.max_workers}")
        return

    if args.phase == "all":
        print("Phase 1: Flat scans")
        results1 = run_jobs_parallel(PHASE1_JOBS, args.max_workers, args.project_root)

        n_failed = sum(1 for r in results1 if r["status"] != "SUCCESS")
        if n_failed > 0:
            print(f"WARNING: {n_failed} Phase 1 jobs failed. Continuing to Phase 2 anyway.")

        print("\nPhase 2: MCMC scans")
        results2 = run_jobs_parallel(PHASE2_JOBS, args.max_workers, args.project_root)
    else:
        run_jobs_parallel(jobs, args.max_workers, args.project_root)


if __name__ == "__main__":
    main()
