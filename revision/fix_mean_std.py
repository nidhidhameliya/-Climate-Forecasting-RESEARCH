"""
Fix the mean_std.json which currently contains NaN values.
Reads from data/interim/train.nc (chunked) and re-saves correct stats.

Run from project root:
    python revision/fix_mean_std.py
"""

import os
import sys
import json
import numpy as np
import xarray as xr

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)

train_nc = os.path.join(PROJECT_ROOT, "data", "interim", "train.nc")
stats_path = os.path.join(PROJECT_ROOT, "data", "processed", "mean_std.json")

print(f"Reading {train_nc} using chunked xarray...")
with xr.open_dataset(train_nc, chunks={"time": 50}) as ds:
    arr_C = (ds["t2m"] - 273.15)  # Kelvin -> Celsius
    mean_C = float(arr_C.mean().values)
    mean2_C = float((arr_C ** 2).mean().values)
    std_C = float(np.sqrt(max(mean2_C - mean_C ** 2, 0.0)))

print(f"Computed: mean={mean_C:.6f} C, std={std_C:.6f} C")

# Backup old file
backup_path = stats_path + ".bak"
if os.path.exists(stats_path):
    with open(stats_path) as f:
        old = f.read()
    with open(backup_path, "w") as f:
        f.write(old)
    print(f"Old mean_std.json backed up to {backup_path}: {old.strip()}")

# Write corrected stats
with open(stats_path, "w") as f:
    json.dump({"mean": mean_C, "std": std_C}, f)

print(f"Saved corrected mean_std.json: mean={mean_C:.6f}, std={std_C:.6f}")
print("IMPORTANT: With NaN stats, the existing evaluate_model.py used fallback values:")
print("   mean=288.15 (Kelvin), std=10.0")
print("   The denormalize_celsius() function subtracts 273.15 AGAIN after de-normalizing,")
print("   which means the reported RMSE in Kelvin == RMSE in Celsius in that code.")
print("   This is a BUG: the preprocessing saved Celsius data but evaluate_model.py")
print("   treats the fallback mean as Kelvin then subtracts 273.15 again.")
