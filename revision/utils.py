"""
Shared utilities for all revision tasks.
- Load existing processed tensors (train/val/test X, y)
- De-normalize predictions to °C
- Compute RMSE, MAE, R2, Pearson r pooled over all grid cells and days
- Build date arrays for the test set (2025-01-01 to 2025-12-31, 358 sequences)
- Seed-setting helper
"""

import os
import sys
import json
import random
from datetime import date, timedelta

import numpy as np
import torch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TENSOR_DIR = os.path.join(PROJECT_ROOT, "data", "processed", "tensors")
STATS_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "mean_std.json")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "revision", "results")
FIGURES_DIR = os.path.join(PROJECT_ROOT, "revision", "figures")
PREDS_DIR = os.path.join(PROJECT_ROOT, "revision", "predictions")

# Grid info
LAT_MIN, LAT_MAX = 5.0, 35.0
LON_MIN, LON_MAX = 65.0, 100.0
NLAT, NLON = 121, 141
LATS = np.linspace(LAT_MAX, LAT_MIN, NLAT)   # 35 -> 5 (descending, north->south)
LONS = np.linspace(LON_MIN, LON_MAX, NLON)


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def load_norm_stats():
    """Load global mean/std from processed/mean_std.json.
    If file contains NaN (as it currently does), re-derive from train.nc."""
    with open(STATS_PATH) as f:
        stats = json.load(f)
    mean_val = stats.get("mean", float("nan"))
    std_val = stats.get("std", float("nan"))
    if np.isnan(mean_val) or np.isnan(std_val) or std_val == 0:
        # Fall back: compute from interim/train.nc using chunked reading
        try:
            import xarray as xr
            train_nc = os.path.join(PROJECT_ROOT, "data", "interim", "train.nc")
            # Use chunks to avoid OOM (2.79 GiB full load)
            with xr.open_dataset(train_nc, chunks={"time": 50}) as ds:
                arr_C = (ds["t2m"] - 273.15)
                mean_val = float(arr_C.mean().values)
                # Two-pass std via E[X^2] - E[X]^2
                mean2_val = float((arr_C ** 2).mean().values)
                std_val = float(np.sqrt(max(mean2_val - mean_val ** 2, 0)))
            print(f"[utils] Re-derived stats from train.nc (chunked): mean={mean_val:.4f} C, std={std_val:.4f} C")
        except Exception as e:
            print(f"[utils] WARNING could not re-derive stats: {e}")
            mean_val = 0.0
            std_val = 1.0
    return float(mean_val), float(std_val)


def denorm(arr_norm, mean, std):
    """De-normalize from z-score to degrees Celsius."""
    return arr_norm * std + mean


def load_split(split):
    """Load (X, y) numpy arrays for a split. Returns float32 arrays."""
    X = np.load(os.path.join(TENSOR_DIR, f"{split}_X.npy")).astype(np.float32)
    y = np.load(os.path.join(TENSOR_DIR, f"{split}_y.npy")).astype(np.float32)
    return X, y


def compute_metrics(pred_C, true_C):
    """
    Compute RMSE, MAE, R2, Pearson r.
    pred_C, true_C: arbitrary-shape numpy arrays, all values in deg C.
    Metrics are pooled over ALL elements.
    """
    p = pred_C.flatten()
    t = true_C.flatten()
    diff = p - t
    rmse = float(np.sqrt(np.mean(diff ** 2)))
    mae = float(np.mean(np.abs(diff)))
    # R-squared
    ss_res = float(np.sum(diff ** 2))
    ss_tot = float(np.sum((t - np.mean(t)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    # Pearson r
    if np.std(p) > 1e-8 and np.std(t) > 1e-8:
        corr = float(np.corrcoef(p, t)[0, 1])
    else:
        corr = float("nan")
    return {"RMSE": rmse, "MAE": mae, "R2": r2, "Corr": corr}


def get_test_dates():
    """
    Return the list of 358 target dates for the test set.
    Test split: 2025-01-01 to 2025-12-31 (365 days).
    With k=7 window, first target is 2025-01-08, last is 2025-12-31.
    -> 358 dates.
    """
    start = date(2025, 1, 8)   # day 8 = first target after 7-day window
    dates = [start + timedelta(days=i) for i in range(358)]
    return dates


def get_train_dates():
    """
    Return the list of 1819 target dates for the training set.
    Train: 2019-01-01 to 2023-12-31 (1826 days). First target: 2019-01-08.
    """
    start = date(2019, 1, 8)
    dates = [start + timedelta(days=i) for i in range(1819)]
    return dates


def get_val_dates():
    """
    Return the list of 359 target dates for the val set.
    Val: 2024-01-01 to 2024-12-31 (366 days). First target: 2024-01-08.
    """
    start = date(2024, 1, 8)
    dates = [start + timedelta(days=i) for i in range(359)]
    return dates


def make_config(hidden_dim=32, seq_len=7):
    return {
        "model": {
            "name": "convlstm",
            "hidden_dim": hidden_dim,
            "lstm_hidden_dim": hidden_dim,
        },
        "training": {
            "batch_size": 16,
            "epochs": 50,
            "learning_rate": 1e-3,
        },
        "sequence_length": seq_len,
    }
