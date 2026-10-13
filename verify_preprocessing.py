"""Fail-fast verification of ERA5 preprocessing artifacts."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import xarray as xr
import yaml


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data/interim/region_subset_raw_verified.nc"
SPLITS = {
    "train": (43824, 1826, "2019-01-01", "2023-12-31"),
    "val": (8784, 366, "2024-01-01", "2024-12-31"),
    "test": (8760, 365, "2025-01-01", "2025-12-31"),
}


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS {message}")


def finite_file(path: Path, key: str | None = None) -> None:
    array = np.load(path, mmap_mode="r", allow_pickle=False)
    for start in range(0, array.shape[0], 64):
        check(np.isfinite(array[start:start + 64]).all(), f"{path.relative_to(ROOT)} finite block {start}")


def aggregate_hourly_once(variable: xr.DataArray) -> np.ndarray:
    """Reproduce daily maxima while reading aligned NetCDF time chunks once."""
    spatial = (int(variable.sizes["latitude"]), int(variable.sizes["longitude"]))
    chunk_hours = int(variable.encoding.get("chunksizes", (24 * 31,))[0])
    carry = np.empty((0, *spatial), dtype=np.float32)
    pieces: list[np.ndarray] = []
    n_days = 0
    for start in range(0, variable.sizes["time"], chunk_hours):
        block = variable.isel(time=slice(start, start + chunk_hours)).values.astype(np.float32, copy=False)
        check(np.isfinite(block).all(), f"hourly storage chunk at {start} finite")
        cursor = 0
        if len(carry):
            needed = 24 - len(carry)
            full_day = np.concatenate((carry, block[:needed]), axis=0)
            pieces.append(full_day.max(axis=0, keepdims=True))
            n_days += 1
            cursor = needed
            carry = np.empty((0, *spatial), dtype=np.float32)
        usable = ((len(block) - cursor) // 24) * 24
        if usable:
            grouped = block[cursor:cursor + usable].reshape(-1, 24, *spatial)
            pieces.append(grouped.max(axis=1))
            n_days += len(grouped)
        carry = block[cursor + usable:].copy()
    check(len(carry) == 0, "hourly chunk boundaries end on a full day")
    result = np.concatenate(pieces, axis=0)
    check(n_days == len(result), "daily sample reconstruction count")
    return result


def main() -> None:
    check(SOURCE.is_file(), "verified source exists")
    with xr.open_dataset(SOURCE) as source:
        check(source.sizes == {"time": 61368, "latitude": 121, "longitude": 141}, "source dimensions")
        source_times = source.time.values
        check(source_times[0] == np.datetime64("2019-01-01T00:00:00") and source_times[-1] == np.datetime64("2025-12-31T23:00:00"), "source timestamp endpoints")
        check(len(np.unique(source_times)) == len(source_times), "source timestamps unique")
        check(np.all(np.diff(source_times).astype("timedelta64[h]") == np.timedelta64(1, "h")), "source has continuous hourly cadence")
        check(source.t2m.attrs.get("units") == "K", "source temperature units are Kelvin")

        target_sets = []
        config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
        seq_len = int(config["sequence_length"])
        with (ROOT / "data/processed/mean_std.json").open(encoding="utf-8") as handle:
            stats = json.load(handle)
        mean, std = float(stats["mean"]), float(stats["std"])
        check(np.isfinite(mean) and np.isfinite(std) and std > 0, "normalization mean/std finite and std positive")
        check(stats.get("unit") == "degrees_Celsius" and stats.get("input_unit") == "kelvin", "normalization units documented")

        for split, (hours, days, first, last) in SPLITS.items():
            hourly_path = ROOT / f"data/interim/{split}.nc"
            daily_path = ROOT / f"data/interim/{split}_daily.nc"
            with xr.open_dataset(hourly_path) as hourly:
                times = hourly.time.values
                expected_h = np.arange(np.datetime64(first), np.datetime64(last) + np.timedelta64(1, "D"), np.timedelta64(1, "h"))
                check(len(times) == hours and np.array_equal(times, expected_h), f"{split} hourly count and bounds")
                check(np.all(np.diff(times).astype("timedelta64[h]") == np.timedelta64(1, "h")), f"{split} hourly cadence continuous")
                with xr.open_dataset(daily_path) as daily:
                    dtime = daily.time.values
                    expected_d = np.arange(np.datetime64(first), np.datetime64(last) + np.timedelta64(1, "D"), np.timedelta64(1, "D"))
                    check(len(dtime) == days and np.array_equal(dtime, expected_d), f"{split} daily count and dates")
                    actual = daily.t2m.values
                    check(actual.shape == (days, 121, 141), f"{split} daily dimensions")
                    check(np.isfinite(actual).all(), f"{split} daily values finite")
                    check(180 <= float(actual.min()) <= float(actual.max()) <= 340, f"{split} daily Kelvin range plausible")
                    check(daily.t2m.attrs.get("units") == "K", f"{split} daily units Kelvin")
                    reference = aggregate_hourly_once(hourly.t2m)
                    check(reference.shape == actual.shape and np.array_equal(actual, reference), f"{split} daily max and 24-hour grouping reproducible")
                    data = np.load(ROOT / f"data/processed/{split}.npy", mmap_mode="r", allow_pickle=False)
                    check(data.shape == (days, 121, 141), f"{split} processed daily shape")
                    finite_file(ROOT / f"data/processed/{split}.npy")
                    check(np.allclose(data[::max(1, days // 17)], (actual[::max(1, days // 17)] - 273.15 - mean) / std, rtol=2e-5, atol=2e-5), f"{split} inverse normalization reconstructs sampled Celsius values")

                    x_path = ROOT / f"data/processed/tensors/{split}_X.npy"
                    y_path = ROOT / f"data/processed/tensors/{split}_y.npy"
                    x = np.load(x_path, mmap_mode="r", allow_pickle=False)
                    y = np.load(y_path, mmap_mode="r", allow_pickle=False)
                    samples = days - seq_len
                    check(x.shape == (samples, seq_len, 1, 121, 141), f"{split} X sequence shape")
                    check(y.shape == (samples, 1, 121, 141), f"{split} y sequence shape")
                    finite_file(x_path)
                    finite_file(y_path)
                    # Exact local reconstruction proves deterministic sliding-window construction.
                    for index in (0, samples // 2, samples - 1):
                        check(np.array_equal(x[index, :, 0], data[index:index + seq_len]), f"{split} X sample {index} reproducible")
                        check(np.array_equal(y[index, 0], data[index + seq_len]), f"{split} y sample {index} reproducible")
                    targets = np.arange(seq_len, days, dtype=np.int32) + np.datetime64(first).astype("datetime64[D]").astype(np.int32)
                    target_sets.append((split, targets))
                    check(np.datetime64(first) + np.timedelta64(seq_len, "D") == dtime[seq_len], f"{split} first target follows {seq_len} inputs")
                    check(dtime[-1] == np.datetime64(last), f"{split} last target date")

        for index in range(len(target_sets) - 1):
            left_name, left = target_sets[index]
            right_name, right = target_sets[index + 1]
            check(np.intersect1d(left, right).size == 0, f"{left_name}/{right_name} targets do not overlap")
        print("All preprocessing checks passed.")


if __name__ == "__main__":
    main()
