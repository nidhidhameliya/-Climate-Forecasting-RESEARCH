"""Build global extreme thresholds from training daily maxima only."""

import json
import os
from pathlib import Path

import numpy as np
import xarray as xr


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DAILY = ROOT / "data/interim/train_daily.nc"
OUTPUT = ROOT / "data/processed/extreme_thresholds.json"

print(f"Computing exact global quantiles from training data only: {TRAIN_DAILY}", flush=True)
with xr.open_dataset(TRAIN_DAILY) as train_ds:
    if train_ds.t2m.attrs.get("units") != "K":
        raise ValueError(f"Expected training daily maxima in K, got {train_ds.t2m.attrs.get('units')!r}")
    values_k = train_ds.t2m.values
    if values_k.shape != (1826, 121, 141):
        raise ValueError(f"Unexpected training daily shape: {values_k.shape}")
    if not np.isfinite(values_k).all():
        raise ValueError("Training daily maxima contain non-finite values")
    values_c = values_k.astype(np.float64) - 273.15

# np.quantile's documented linear (Type 7) method is deterministic. It is
# computed over all training day/grid cells, never over validation or test.
threshold_95 = float(np.quantile(values_c, 0.95, method="linear"))
threshold_05 = float(np.quantile(values_c, 0.05, method="linear"))
if not np.isfinite(threshold_95) or not np.isfinite(threshold_05):
    raise ValueError("Computed a non-finite extreme threshold")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
payload = {
    "top_5_percent_celsius": threshold_95,
    "bottom_5_percent_celsius": threshold_05,
    "quantile_method": "NumPy linear quantile (Hyndman-Fan Type 7)",
    "scope": "training split only; daily maximum t2m over all grid cells and days",
    "training_daily_records": int(values_c.shape[0]),
    "training_grid_values": int(values_c.size),
    "training_date_range": ["2019-01-01", "2023-12-31"],
    "input": "data/interim/train_daily.nc (t2m in K)",
    "loss_weight": 5.0,
}
temp_path = OUTPUT.with_suffix(".json.tmp")
temp_path.write_text(json.dumps(payload, indent=2, allow_nan=False), encoding="utf-8")
os.replace(temp_path, OUTPUT)
print(json.dumps(payload, indent=2), flush=True)
print(f"Saved {OUTPUT.relative_to(ROOT)}", flush=True)
