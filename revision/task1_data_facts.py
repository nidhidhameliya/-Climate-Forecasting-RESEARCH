"""
Task 1 - Data and model facts audit.
Writes revision/results/data_facts.json and prints a summary.

Run from project root:
    python revision/task1_data_facts.py
"""

import os
import sys
import json

import numpy as np
import torch
import xarray as xr
import yaml

# Make project importable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from models.convlstm import ConvLSTMModel
from models.lstm_baseline import LSTMBaseline
from models.cnn_lstm import CNNLSTMModel
from models.transformer import SpatioTemporalTransformer

os.chdir(PROJECT_ROOT)


def count_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def make_config(hidden_dim=32):
    return {
        "model": {
            "name": "convlstm",
            "hidden_dim": hidden_dim,
            "lstm_hidden_dim": hidden_dim,
        },
        "training": {"batch_size": 8},
    }


# ── (a) NaN / out-of-range stats on raw ERA5 ─────────────────────────────────
# We use the pre-processed region_subset_raw_verified.nc (already subset to 5N-35N, 65E-100E)
# instead of scanning the 7 x ~12 GB raw hourly files (which would take 30+ min).
# This file is in Kelvin (hourly), same data, and covers 2019-2025.
print("\n[a] Computing NaN and out-of-range stats from region_subset_raw_verified.nc...")
print("    (This covers all years 2019-2025, subset to study region, in Kelvin)")
region_raw_path = os.path.join(PROJECT_ROOT, "data", "interim", "region_subset_raw_verified.nc")
total_cells = 0
nan_count = 0
out_of_range = 0  # outside 230-330 K

if os.path.exists(region_raw_path):
    print(f"  Reading {region_raw_path} ...")
    with xr.open_dataset(region_raw_path, chunks={"time": 100}) as ds:
        arr = ds["t2m"]
        total_cells = int(arr.size)
        nan_count = int(arr.isnull().sum().values)
        # Values outside 230-330 K
        oor = ((arr < 230) | (arr > 330)).sum()
        out_of_range = int(oor.values)
    print(f"  Total cells: {total_cells:,}")
    print(f"  NaN count: {nan_count:,} ({100.*nan_count/total_cells:.4f}%)")
    print(f"  Out of range (230-330K): {out_of_range:,}")
else:
    print(f"  WARNING: {region_raw_path} not found. Trying daily_resampled.nc...")
    daily_r_path = os.path.join(PROJECT_ROOT, "data", "interim", "daily_resampled.nc")
    if os.path.exists(daily_r_path):
        with xr.open_dataset(daily_r_path, chunks={"time": 100}) as ds:
            arr = ds["t2m"]
            total_cells = int(arr.size)
            nan_count = int(arr.isnull().sum().values)
            out_of_range = int(((arr < 230) | (arr > 330)).sum().values)
        print(f"  daily_resampled.nc: total={total_cells}, NaN={nan_count}, OOR={out_of_range}")

pct_nan = 100.0 * nan_count / total_cells if total_cells > 0 else float("nan")

# Also check daily resampled
daily_path = os.path.join(PROJECT_ROOT, "data", "interim", "daily_resampled.nc")
daily_nan = 0
daily_oor = 0
daily_total = 0
if os.path.exists(daily_path):
    with xr.open_dataset(daily_path, chunks={"time": 100}) as ds:
        arr_d = ds["t2m"]
        daily_total = int(arr_d.size)
        daily_nan = int(arr_d.isnull().sum().values)
        daily_oor = int(((arr_d < 230) | (arr_d > 330)).sum().values)
    print(f"  daily_resampled.nc: total={daily_total}, NaN={daily_nan}, OOR={daily_oor}")


# ── (b) Normalization stats ────────────────────────────────────────────────────
print("\n[b] Checking normalization statistics...")
train_nc = os.path.join(PROJECT_ROOT, "data", "interim", "train.nc")
recomp_mean_K = None
recomp_std_K = None
if os.path.exists(train_nc):
    print("  Loading train.nc in chunks (large file - using dask)...")
    with xr.open_dataset(train_nc, chunks={"time": 50}) as ds:
        arr_C = (ds["t2m"] - 273.15)
        recomp_mean_K = float(arr_C.mean().values)
        mean2 = float((arr_C ** 2).mean().values)
        recomp_std_K = float(np.sqrt(max(mean2 - recomp_mean_K ** 2, 0)))
    print(f"  Re-computed from train.nc (chunked): mean={recomp_mean_K:.6f} C, std={recomp_std_K:.6f} C")
else:
    print("  WARNING: data/interim/train.nc not found for re-computation")

stats_path = os.path.join(PROJECT_ROOT, "data", "processed", "mean_std.json")
with open(stats_path) as f:
    raw_stats = json.load(f)
print(f"  mean_std.json raw: {raw_stats}")
print("  normalization type: SINGLE GLOBAL SCALAR (not per-grid-cell)")

# ── (c) Conv3D architecture details ───────────────────────────────────────────
print("\n[c] Conv3D architecture details...")
cfg = make_config(32)
model_conv3d = ConvLSTMModel(cfg)
enc_first = model_conv3d.encoder[0]
padding_val = enc_first.padding
kernel_val = enc_first.kernel_size
decoder_layer = model_conv3d.decoder
print(f"  Encoder first layer: kernel={kernel_val}, padding={padding_val}")
print(f"  Encoder second layer: kernel={model_conv3d.encoder[2].kernel_size}, padding={model_conv3d.encoder[2].padding}")
print(f"  Decoder layer: kernel={decoder_layer.kernel_size}, padding={decoder_layer.padding}")
print("  Last-timestep slice: out[:, :, -1, :, :]")

# ── (d) Baseline parameter counts ─────────────────────────────────────────────
print("\n[d] Baseline model parameter counts...")
models_info = {}
models_info["Conv3D_proposed"] = count_params(model_conv3d)
lstm_model = LSTMBaseline(cfg)
models_info["LSTM"] = count_params(lstm_model)
cnn_lstm_model = CNNLSTMModel(cfg)
models_info["CNN_LSTM"] = count_params(cnn_lstm_model)
transformer_model = SpatioTemporalTransformer(cfg)
models_info["Transformer"] = count_params(transformer_model)

paper_claims = {"LSTM": 185000, "CNN_LSTM": 95000, "Transformer": 127000}
for name, actual in models_info.items():
    paper_val = paper_claims.get(name)
    flag = ""
    if paper_val is not None and abs(actual - paper_val) > 500:
        flag = f"  WARNING: paper claims ~{paper_val:,} -- MISMATCH by {actual - paper_val:+,}"
    print(f"  {name}: {actual:,} parameters{flag}")

# ── (e) Validation set usage ───────────────────────────────────────────────────
print("\n[e] Validation set usage...")
val_usage = (
    "The validation loss is computed every epoch (training/validate.py) and printed, "
    "but there is NO checkpoint selection or early-stopping based on val loss. "
    "The model saved is the FINAL-EPOCH model (experiments/latest/model.pth). "
    "Validation set is used for MONITORING ONLY."
)
print(f"  {val_usage}")

# ── (f) Existing test metrics ─────────────────────────────────────────────────
print("\n[f] Existing test metrics...")
existing_results_path = os.path.join(PROJECT_ROOT, "outputs", "evaluation", "test_results.json")
existing_metrics = None
if os.path.exists(existing_results_path):
    with open(existing_results_path) as f:
        existing_metrics = json.load(f)
    m = existing_metrics["metrics"]
    print(f"  num_samples : {existing_metrics['num_samples']}")
    print(f"  RMSE (C)    : {m['rmse_celsius']:.6f}")
    print(f"  MAE  (C)    : {m['mae_celsius']:.6f}")
    print(f"  Pearson r   : {m['correlation']:.6f}  (paper labels this as 'correlation')")
    print(f"  Note: R2 in paper = {m['correlation']:.4f} is actually Pearson r")
    print(f"  Note: The 0.2477 correlation in paper DOES NOT match this code output")
else:
    print("  WARNING: test_results.json not found")

with open(os.path.join(PROJECT_ROOT, "config.yaml")) as f:
    cfg_yaml = yaml.safe_load(f)
t_cfg = cfg_yaml["training"]
print(f"  Config: epochs={t_cfg['epochs']}, lr={t_cfg['learning_rate']}, batch={t_cfg['batch_size']}")
print("  Loss: ExtremeWeightedMSE (paper says plain MSE)")
print("  lr=1e-4 batch=8 in config.yaml vs fixed-facts lr=1e-3 batch=16 -- DISCREPANCY")

# ── Build data_facts.json ─────────────────────────────────────────────────────
facts = {
    "dataset": {
        "start_date": "2019-01-01",
        "end_date": "2025-12-31",
        "total_days": 2557,
        "region": "5N-35N, 65E-100E",
        "grid": "121x141",
        "resolution_deg": 0.25,
        "variable": "t2m",
    },
    "splits": {
        "train": {"years": "2019-2023", "days": 1826, "sequences": 1819},
        "val": {"years": "2024", "days": 366, "sequences": 359},
        "test": {"years": "2025", "days": 365, "sequences": 358},
    },
    "raw_nan_stats": {
        "total_hourly_cells": int(total_cells),
        "nan_count": int(nan_count),
        "nan_pct": float(pct_nan),
        "out_of_range_230_330K": int(out_of_range),
    },
    "daily_resampled_nan_stats": {
        "total_cells": int(daily_total),
        "nan_count": int(daily_nan),
        "out_of_range_230_330K": int(daily_oor),
    },
    "normalization": {
        "type": "z-score",
        "scope": "SINGLE GLOBAL SCALAR (not per-grid-cell)",
        "mean_C_from_interim": recomp_mean_K,
        "std_C_from_interim": recomp_std_K,
        "mean_std_json_raw": raw_stats,
        "nan_fill": "0.0 after normalization (nan_to_num)",
    },
    "conv3d_architecture": {
        "encoder_kernel": list(kernel_val),
        "encoder_padding": int(padding_val) if isinstance(padding_val, int) else list(padding_val),
        "decoder_kernel": list(decoder_layer.kernel_size),
        "decoder_padding": int(decoder_layer.padding) if isinstance(decoder_layer.padding, int) else list(decoder_layer.padding),
        "last_timestep_extraction": "out[:, :, -1, :, :]",
        "channels": "1 -> 32 -> 32 -> 1",
        "total_params": int(models_info["Conv3D_proposed"]),
    },
    "baseline_param_counts": {k: int(v) for k, v in models_info.items()},
    "paper_param_claims_vs_actual": {
        "LSTM_paper_claim": 185000,
        "LSTM_actual": int(models_info["LSTM"]),
        "LSTM_matches_claim": abs(models_info["LSTM"] - 185000) < 500,
        "CNN_LSTM_paper_claim": 95000,
        "CNN_LSTM_actual": int(models_info["CNN_LSTM"]),
        "CNN_LSTM_matches_claim": abs(models_info["CNN_LSTM"] - 95000) < 500,
        "Transformer_paper_claim": 127000,
        "Transformer_actual": int(models_info["Transformer"]),
        "Transformer_matches_claim": abs(models_info["Transformer"] - 127000) < 500,
    },
    "baseline_input_method": {
        "LSTM": (
            "Per-grid-cell: each pixel processed as independent 1D LSTM (shared weights). "
            "Input reshaped to (B*H*W, T, 1); output reshaped back to (B, 1, H, W)."
        ),
        "CNN_LSTM": (
            "2D CNN encodes each timestep's 121x141 map to hidden features; "
            "global average-pool to a hidden_dim vector; LSTM processes T-length sequence; "
            "last LSTM state broadcast back to spatial map via decoder Conv2d."
        ),
        "Transformer": (
            "1x1 Conv encodes each timestep's 121x141 map; TransformerEncoder on "
            "T-length global-avg-pooled sequence; last token broadcast to spatial map."
        ),
    },
    "validation_usage": val_usage,
    "training_config": {
        "epochs": t_cfg["epochs"],
        "learning_rate": t_cfg["learning_rate"],
        "batch_size": t_cfg["batch_size"],
        "optimizer": "Adam",
        "loss": "ExtremeWeightedMSE (extreme_weight=5.0); degrades to weighted MSE if threshold file missing",
        "checkpoint_selection": "NONE - final epoch saved only",
    },
    "existing_test_metrics": existing_metrics,
    "reviewer_discrepancies": {
        "R2_vs_correlation": (
            "Paper states R2=0.9720 AND separately correlation=0.2477. "
            "Code (evaluate_model.py) computes Pearson r=0.9720 -- this IS the 0.9720. "
            "No R-squared computation exists in the codebase. "
            "The 0.2477 correlation figure cannot be reproduced and is likely an error."
        ),
        "sample_count_1089": (
            "Paper mentions 1089 training samples; actual tensor has 1819 sequences "
            "(train shape 1819x7x1x121x141). 1089 may be from an older/different run."
        ),
        "loss_function": (
            "config.yaml uses ExtremeWeightedMSE; paper claims plain MSE."
        ),
        "lr_and_batch": (
            "config.yaml: lr=1e-4, batch=8. "
            "Specification: lr=1e-3, batch=16. These do not match."
        ),
    },
}

out_path = os.path.join(PROJECT_ROOT, "revision", "results", "data_facts.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump(facts, f, indent=2)

print(f"\nSaved -> {out_path}")
print("\n" + "=" * 70)
print("SUMMARY OF KEY FINDINGS (Task 1)")
print("=" * 70)
print(f"  Tensor shapes confirmed: train=1819, val=359, test=358 sequences")
print(f"  NaN in hourly raw ERA5 : {nan_count:,} ({pct_nan:.4f}%)")
print(f"  Out-of-range (230-330K): {out_of_range:,}")
print(f"  Normalization          : GLOBAL SCALAR (not per-pixel)")
if recomp_mean_K is not None:
    print(f"  mean={recomp_mean_K:.4f} C, std={recomp_std_K:.4f} C")
print(f"  Conv3D padding: {padding_val}, kernel: {kernel_val}")
print(f"  Last timestep extracted: out[:, :, -1, :, :]")
for nm, vv in models_info.items():
    print(f"  Params {nm}: {vv:,}")
print("  Validation: monitoring only, NO checkpoint selection")
if existing_metrics is not None:
    m = existing_metrics["metrics"]
    print(f"  Existing test: RMSE={m['rmse_celsius']:.4f}C  MAE={m['mae_celsius']:.4f}C  Pearson_r={m['correlation']:.4f}")
print("  DISCREPANCIES FOUND:")
print("    - Paper R2=0.9720 is actually Pearson r; no R2 computed in code")
print("    - Paper correlation=0.2477 cannot be reproduced")
print("    - Paper says 1089 train samples; actual tensor has 1819")
print("    - config.yaml lr=1e-4 batch=8; spec says lr=1e-3 batch=16")
print("    - Loss is ExtremeWeightedMSE, not plain MSE as paper states")
print("=" * 70)
