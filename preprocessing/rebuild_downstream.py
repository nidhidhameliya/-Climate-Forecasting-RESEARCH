"""Chunked rebuild from hourly splits already checked against the source."""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import xarray as xr
import yaml

ROOT = Path(__file__).resolve().parents[1]
SPLITS = {
    "train": ("2019-01-01", "2023-12-31 23:00", 43824, 1826),
    "val": ("2024-01-01", "2024-12-31 23:00", 8784, 366),
    "test": ("2025-01-01", "2025-12-31 23:00", 8760, 365),
}
SPATIAL = (121, 141)
DAILY_CHUNK_DAYS = 31
STATS_CHUNK_DAYS = 31


def validate_hourly(split: str, start: str, end: str, expected_hours: int, scan_finite: bool) -> None:
    path = ROOT / f"data/interim/{split}.nc"
    with xr.open_dataset(path) as ds:
        if ds.sizes != {"time": expected_hours, "latitude": 121, "longitude": 141}:
            raise ValueError(f"{split}: unexpected dimensions {dict(ds.sizes)}")
        times = ds.time.values
        expected = np.arange(np.datetime64(start), np.datetime64(end) + np.timedelta64(1, "h"), np.timedelta64(1, "h"))
        if not np.array_equal(times, expected):
            raise ValueError(f"{split}: timestamps do not match expected continuous hourly range")
        if scan_finite:
            time_chunk = int(ds.t2m.encoding.get("chunksizes", (24 * DAILY_CHUNK_DAYS,))[0])
            for offset in range(0, expected_hours, time_chunk):
                block = ds.t2m.isel(time=slice(offset, offset + time_chunk)).values
                if not np.isfinite(block).all():
                    raise ValueError(f"{split}: non-finite hourly temperature in block at index {offset}")
        if ds.t2m.attrs.get("units") != "K":
            raise ValueError(f"{split}: expected Kelvin units, got {ds.t2m.attrs.get('units')!r}")
    finite_note = " and chunked finite values" if scan_finite else "; temperature finiteness checked during daily aggregation"
    print(f"{split}: validated {expected_hours} hourly records, bounds, cadence, dimensions, Kelvin units{finite_note}.", flush=True)


def build_daily(split: str, expected_days: int) -> None:
    hourly_path = ROOT / f"data/interim/{split}.nc"
    output_path = ROOT / f"data/interim/{split}_daily.nc"
    temp_path = output_path.with_name(output_path.name + ".tmp.nc")
    daily_parts: list[np.ndarray] = []
    day_offset = 0
    carry = np.empty((0, *SPATIAL), dtype=np.float32)
    with xr.open_dataset(hourly_path) as hourly:
        time_chunk = int(hourly.t2m.encoding.get("chunksizes", (24 * DAILY_CHUNK_DAYS,))[0])
        print(f"{split}: reading NetCDF time chunks of {time_chunk} hours.", flush=True)
        for start in range(0, hourly.sizes["time"], time_chunk):
            block = hourly.t2m.isel(time=slice(start, start + time_chunk)).values.astype(np.float32, copy=False)
            if not np.isfinite(block).all():
                raise ValueError(f"{split}: non-finite hourly value in storage chunk beginning at {start}")
            cursor = 0
            if len(carry):
                needed = 24 - len(carry)
                if len(block) < needed:
                    carry = np.concatenate((carry, block), axis=0)
                    continue
                full_day = np.concatenate((carry, block[:needed]), axis=0)
                daily_parts.append(full_day.max(axis=0, keepdims=True))
                day_offset += 1
                cursor = needed
                carry = np.empty((0, *SPATIAL), dtype=np.float32)
            usable = ((len(block) - cursor) // 24) * 24
            full_count = usable // 24
            if full_count:
                grouped = block[cursor:cursor + usable].reshape(full_count, 24, *SPATIAL)
                daily_parts.append(grouped.max(axis=1))
                day_offset += full_count
            carry = block[cursor + usable:].copy()
            print(f"{split}: aggregated storage chunk {start}:{min(start + time_chunk, hourly.sizes['time'])}; days={day_offset}; carry_hours={len(carry)}.", flush=True)
        lat = hourly.latitude.values
        lon = hourly.longitude.values
        times = hourly.time.values[::24]
    if len(carry) != 0 or day_offset != expected_days:
        raise ValueError(f"{split}: hourly-to-daily chunk boundary error; days={day_offset}, carry_hours={len(carry)}")
    all_values = np.concatenate(daily_parts, axis=0)
    if all_values.shape != (expected_days, *SPATIAL) or not np.isfinite(all_values).all():
        raise ValueError(f"{split}: invalid/non-finite daily aggregation")
    if all_values.min() < 180 or all_values.max() > 340:
        raise ValueError(f"{split}: implausible daily Kelvin range {all_values.min()}..{all_values.max()}")
    result = xr.Dataset(
        {"t2m": (("time", "latitude", "longitude"), all_values)},
        coords={"time": times, "latitude": lat, "longitude": lon},
    )
    result.t2m.attrs.update(units="K", long_name="daily maximum 2 metre temperature", aggregation="maximum over exactly 24 hourly observations")
    try:
        result.to_netcdf(temp_path, engine="netcdf4")
        # Validate the serialized temporary artifact before replacing its destination.
        with xr.open_dataset(temp_path) as check:
            if check.sizes.get("time") != expected_days or not np.array_equal(check.time.values, times):
                raise ValueError(f"{split}: serialized daily dimensions or timestamps failed")
            if check.t2m.attrs.get("units") != "K":
                raise ValueError(f"{split}: serialized daily units failed")
            for offset in range(0, expected_days, DAILY_CHUNK_DAYS):
                values = check.t2m.isel(time=slice(offset, offset + DAILY_CHUNK_DAYS)).values
                if not np.isfinite(values).all():
                    raise ValueError(f"{split}: serialized daily values non-finite in block {offset}")
        os.replace(temp_path, output_path)
    finally:
        temp_path.unlink(missing_ok=True)
    print(f"{split}: wrote validated daily maximum file ({day_offset} days) to {output_path.relative_to(ROOT)}.", flush=True)


def training_stats(path: Path) -> tuple[float, float, int]:
    count = 0
    mean = 0.0
    m2 = 0.0
    with xr.open_dataset(path) as ds:
        for start in range(0, ds.sizes["time"], STATS_CHUNK_DAYS):
            values = ds.t2m.isel(time=slice(start, start + STATS_CHUNK_DAYS)).values.astype(np.float64) - 273.15
            if not np.isfinite(values).all():
                raise ValueError(f"Non-finite training daily value in block {start}")
            block_count = values.size
            block_mean = float(values.mean())
            block_m2 = float(np.square(values - block_mean).sum())
            if count == 0:
                mean, m2, count = block_mean, block_m2, block_count
            else:
                delta = block_mean - mean
                total = count + block_count
                m2 += block_m2 + delta * delta * count * block_count / total
                mean += delta * block_count / total
                count = total
    std = float(np.sqrt(m2 / count)) if count else float("nan")
    if not np.isfinite(mean) or not np.isfinite(std) or std <= 0:
        raise ValueError(f"Invalid training statistics: mean={mean}, std={std}")
    return mean, std, count


def write_normalized(split: str, mean: float, std: float, days: int) -> Path:
    processed = ROOT / "data/processed"
    source_path = ROOT / f"data/interim/{split}_daily.nc"
    output_path = processed / f"{split}.npy"
    temp_path = output_path.with_name(output_path.name + ".tmp")
    out = np.lib.format.open_memmap(temp_path, mode="w+", dtype=np.float32, shape=(days, *SPATIAL))
    try:
        with xr.open_dataset(source_path) as ds:
            for start in range(0, days, DAILY_CHUNK_DAYS):
                values = ds.t2m.isel(time=slice(start, start + DAILY_CHUNK_DAYS)).values.astype(np.float32)
                if not np.isfinite(values).all():
                    raise ValueError(f"{split}: daily values are non-finite in block {start}")
                out[start:start + len(values)] = (values - np.float32(273.15) - np.float32(mean)) / np.float32(std)
        out.flush()
    finally:
        del out
    os.replace(temp_path, output_path)
    return output_path


def write_sequences(split: str, normalized_path: Path, days: int, seq_len: int) -> None:
    array = np.load(normalized_path, mmap_mode="r", allow_pickle=False)
    for start in range(0, days, DAILY_CHUNK_DAYS):
        if not np.isfinite(array[start:start + DAILY_CHUNK_DAYS]).all():
            raise ValueError(f"{split}: normalized array contains non-finite values in block {start}")
    count = days - seq_len
    out_dir = ROOT / "data/processed/tensors"
    out_dir.mkdir(parents=True, exist_ok=True)
    for kind, shape in (("X", (count, seq_len, 1, *SPATIAL)), ("y", (count, 1, *SPATIAL))):
        target = out_dir / f"{split}_{kind}.npy"
        temp = target.with_name(target.name + ".tmp")
        mapped = np.lib.format.open_memmap(temp, mode="w+", dtype=np.float32, shape=shape)
        try:
            for batch_start in range(0, count, 8):
                batch_end = min(batch_start + 8, count)
                if kind == "X":
                    for i in range(batch_start, batch_end):
                        mapped[i, :, 0] = array[i:i + seq_len]
                else:
                    for i in range(batch_start, batch_end):
                        mapped[i, 0] = array[i + seq_len]
            mapped.flush()
        finally:
            del mapped
        os.replace(temp, target)
    print(f"{split}: normalized days={days}; sequence samples={count}; length={seq_len}.", flush=True)


def main() -> None:
    for split, (start, end, hours, days) in SPLITS.items():
        # train.nc was already matched value-for-value to the verified source;
        # its values are checked as aggregation proceeds, avoiding a redundant full read.
        validate_hourly(split, start, end, hours, scan_finite=(split != "train"))
        build_daily(split, days)

    mean, std, count = training_stats(ROOT / "data/interim/train_daily.nc")
    stats = {
        "mean": mean,
        "std": std,
        "unit": "degrees_Celsius",
        "input_unit": "kelvin",
        "method": "global scalar population mean/std (ddof=0), training split only, Welford block aggregation",
        "training_value_count": count,
        "normalized_array": "(daily_max_K - 273.15 - mean) / std",
        "daily_aggregation": "maximum of exactly 24 hourly observations; reads aligned to each NetCDF time chunk and carries partial days across chunk boundaries",
        "source": "data/interim/region_subset_raw_verified.nc",
        "hourly_source_equality": {
            "train": "verified value-for-value against source in prior rebuild run",
            "val": "unverified; bounds/cadence/dimensions/finite values validated",
            "test": "unverified; bounds/cadence/dimensions/finite values validated",
        },
    }
    stats_path = ROOT / "data/processed/mean_std.json"
    stats_temp = stats_path.with_name(stats_path.name + ".tmp")
    stats_temp.write_text(json.dumps(stats, indent=2, allow_nan=False), encoding="utf-8")
    os.replace(stats_temp, stats_path)
    print(f"Training-only normalization: mean={mean:.8f} C, std={std:.8f} C, values={count}.", flush=True)

    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    seq_len = int(config["sequence_length"])
    for split, (_, _, _, days) in SPLITS.items():
        npy_path = write_normalized(split, mean, std, days)
        write_sequences(split, npy_path, days, seq_len)


if __name__ == "__main__":
    main()
