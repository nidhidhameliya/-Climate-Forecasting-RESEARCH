"""
Master entry point for all revision experiments.

Usage (from project root):
    python revision/run_all.py                # run everything
    python revision/run_all.py --task 1       # run only Task 1
    python revision/run_all.py --task 1 2     # run Tasks 1 and 2
    python revision/run_all.py --skip 2 3     # skip Tasks 2 and 3

Tasks:
  1 - Data facts audit (fast, reads raw ERA5)
  2 - Extra baselines (medium, trains U-Net + ConvLSTM x5 seeds)
  3 - Ablation study (slow, trains ~20 configs x5 seeds)
  4 - Spatial/seasonal analysis (fast, needs task2 preds)
  5 - Paper-ready SUMMARY.md (fast, needs tasks 1-4)

Speed notes:
  - Task 1 scans 7 x ~12 GB ERA5 files. Expect ~5-15 min on HDD.
  - Tasks 2 and 3 train neural nets. On CPU expect several hours.
    Consider --task 1 first, then run 2-3 overnight.
"""

import argparse
import logging
import os
import subprocess
import sys
import time
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVISION_DIR = os.path.join(PROJECT_ROOT, "revision")
LOG_DIR = os.path.join(REVISION_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, f"run_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("run_all")

TASKS = {
    1: "revision/task1_data_facts.py",
    2: "revision/task2_baselines.py",
    3: "revision/task3_ablation.py",
    4: "revision/task4_analysis.py",
    5: "revision/task5_summary.py",
}

TASK_DESCRIPTIONS = {
    1: "Data facts audit (NaN stats, param counts, discrepancies)",
    2: "Extra baselines (climatology, persistence, ridge, U-Net, ConvLSTM)",
    3: "Ablation study (window k, channels, depth, kernel)",
    4: "Spatial/seasonal/extreme analysis",
    5: "Paper-ready SUMMARY.md",
}


def run_task(task_id):
    script = TASKS[task_id]
    desc = TASK_DESCRIPTIONS[task_id]
    log.info(f"{'='*60}")
    log.info(f"STARTING Task {task_id}: {desc}")
    log.info(f"Script: {script}")
    log.info(f"{'='*60}")
    t0 = time.time()
    result = subprocess.run(
        [sys.executable, script],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    elapsed = time.time() - t0
    output = result.stdout or ""
    for line in output.splitlines():
        log.info(f"  [T{task_id}] {line}")
    if result.returncode == 0:
        log.info(f"Task {task_id} COMPLETED in {elapsed:.1f}s")
        return True
    else:
        log.error(f"Task {task_id} FAILED (exit code {result.returncode}) after {elapsed:.1f}s")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run all revision experiments")
    parser.add_argument("--task", nargs="+", type=int, choices=list(TASKS.keys()),
                        help="Run only these task IDs (default: all)")
    parser.add_argument("--skip", nargs="+", type=int, choices=list(TASKS.keys()),
                        help="Skip these task IDs")
    args = parser.parse_args()

    if args.task:
        tasks_to_run = sorted(args.task)
    else:
        tasks_to_run = sorted(TASKS.keys())

    if args.skip:
        tasks_to_run = [t for t in tasks_to_run if t not in args.skip]

    log.info("=" * 60)
    log.info("REVISION EXPERIMENT RUNNER")
    log.info(f"Log file: {log_file}")
    log.info(f"Tasks to run: {tasks_to_run}")
    log.info("=" * 60)

    overall_t0 = time.time()
    results = {}
    for t in tasks_to_run:
        ok = run_task(t)
        results[t] = ok
        if not ok and t in (1,):
            log.error(f"Task {t} failed — subsequent tasks may not have required data. Continuing anyway.")

    total = time.time() - overall_t0
    log.info("\n" + "=" * 60)
    log.info("FINAL RESULTS")
    log.info("=" * 60)
    for t, ok in results.items():
        status = "OK" if ok else "FAILED"
        log.info(f"  Task {t} ({TASK_DESCRIPTIONS[t]}): {status}")
    log.info(f"Total time: {total:.1f}s ({total/60:.1f} min)")
    log.info(f"Log saved: {log_file}")
    log.info("=" * 60)

    # Print output file locations
    log.info("\nOutput files:")
    output_files = [
        "revision/results/data_facts.json",
        "revision/results/table2_baselines.csv",
        "revision/results/table3_ablation.csv",
        "revision/results/table4_seasonal.csv",
        "revision/results/table5_regional.csv",
        "revision/results/table5_extremes.csv",
        "revision/SUMMARY.md",
        "revision/figures/fig_monthly_rmse.png",
        "revision/figures/fig_rmse_map_conv3d.png",
        "revision/figures/fig_bias_map_conv3d.png",
        "revision/figures/fig_rmse_latlon.png",
    ]
    for f in output_files:
        full = os.path.join(PROJECT_ROOT, f)
        exists = "EXISTS" if os.path.exists(full) else "MISSING"
        log.info(f"  {f}: {exists}")


if __name__ == "__main__":
    main()
