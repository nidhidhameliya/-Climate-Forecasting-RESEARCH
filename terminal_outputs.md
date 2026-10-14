# Terminal Output Log

Project: `C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2`

This file is the single place for command output retained for later review. Add each command, date/time, exit code, and complete stdout/stderr under a new section. For PowerShell commands, append captured output with `Tee-Object -FilePath terminal_outputs.md -Append` only when the output is plain text; for structured commands, redirect output to a temporary file and append it under a fenced code block so this Markdown remains readable.

## 2026-10-13 â€” Initial inspection

### Compare supplied task attachments

Command: compared the two pasted task files byte-for-byte using PowerShell `Get-Content -Raw`.

```text
FirstChars  : 12545
SecondChars : 12545
Identical   : True
```

### Git status

Command: `git status --short`

```text
?? revision/
```

### Existing project documentation and text logs

The repository contains multiple project documents and at least one existing training log (`experiments/exp_01_baseline/training_log.txt`). No existing general-purpose terminal-output Markdown log was identified. The existing training log and project documents were left untouched.


## 2026-10-13 â€” Remove confirmed empty temporary file

Command: Remove-Item -LiteralPath file.tmp

```text
Deleted file.tmp (0 bytes, an empty temporary file).
```

## 2026-10-13 â€” Dataset and workspace inventory

Command: PowerShell inventory of data, prior results, revision directory, and Python environments.

```text

FullName                                                                                                         Length
--------                                                                                                         ------
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\interim\daily_resampled.nc            174545276
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\interim\merged.nc                     ...054133
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\interim\region_subset.nc              262569371
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\interim\region_subset_raw_verified.nc ...114325
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\interim\test.nc                       250200623
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\interim\train.nc                      ...132695
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\interim\val.nc                        250568310
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\processed\tensors
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\processed\mean_std.json                      25
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\processed\test.npy                     24909188
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\processed\train.npy                   124613672
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\processed\val.npy                      24977432
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\figures
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\predictions
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\results
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\fix_mean_std.py                        1820
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\run_all.py                             5152
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\task1_data_facts.py                   14371
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\task2_baselines.py                    16043
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\task3_ablation.py                      8226
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\task4_analysis.py                     17342
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\task5_summary.py                      16561
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\utils.py                               4989
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\__init__.py                              19
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\experiments\exp_01_baseline
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\experiments\exp_02_convlstm
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\experiments\exp_03_transformer
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\experiments\latest



--- SOURCE ---


FullName      : C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\data\interim\region_subset_raw_verif
                ied.nc
Length        : 1787114325
LastWriteTime : 19-09-2026 19:24:05




--- Python executables ---

Source
------
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\.venv\Scripts\python.exe
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\venv\Scripts\python.exe



--- Backup directory inventory ---

FullName                                                                                        Length LastWriteTime
--------                                                                                        ------ -------------
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\figures                    13-10-2026 13...
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\predictions                13-10-2026 13...
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\results                    13-10-2026 13...
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\fix_mean_std.py     1820   13-10-2026 13...
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\run_all.py          5152   13-10-2026 13...
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\task1_data_facts.py 14371  13-10-2026 13...
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\task2_baselines.py  16043  13-10-2026 13...
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\task3_ablation.py   8226   13-10-2026 13...
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\task4_analysis.py   17342  13-10-2026 13...
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\task5_summary.py    16561  13-10-2026 13...
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\utils.py            4989   13-10-2026 13...
C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\revision\__init__.py         19     13-10-2026 13...


```

## 2026-10-13 â€” Detailed pipeline inspection

Command: Inspect model implementation files, source NetCDF metadata and time/value properties, installed Python/Torch/CUDA versions, and existing revision result artifacts

```text
Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]
Torch 2.5.1+cu121 CUDA available True
GPU NVIDIA GeForce RTX 4070 VRAM_GiB 11.99

===== models/convlstm.py =====
"""
A simple 3D CNN-based model for spatiotemporal forecasting.

This model uses a sequence of 3D convolutions to act as a simple ConvLSTM-like
encoder-decoder structure. It processes a sequence of 2D spatial maps over time.
"""

import torch
import torch.nn as nn
from typing import Dict, Any


class ConvLSTMModel(nn.Module):
    """
    A simple Conv3D model that mimics an encoder-decoder structure for
    spatiotemporal forecasting. It takes a sequence of 2D grids and predicts
    the next grid in the sequence.

    The architecture consists of two main parts:
    1. An encoder of two Conv3D layers to extract spatiotemporal features.
    2. A decoder of one Conv3D layer to project features back to the output grid.

    Args:
        config (Dict[str, Any]): A dictionary containing model configuration,
            expected to have a "model" key with "hidden_dim".
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__()

        hidden_dim = config["model"]["hidden_dim"]

        self.encoder = nn.Sequential(
            nn.Conv3d(in_channels=1, out_channels=hidden_dim, kernel_size=(3, 3, 3), padding=1),
            nn.ReLU(),
            nn.Conv3d(in_channels=hidden_dim, out_channels=hidden_dim, kernel_size=(3, 3, 3), padding=1),
            nn.ReLU(),
        )

        self.decoder = nn.Conv3d(in_channels=hidden_dim, out_channels=1, kernel_size=(3, 3, 3), padding=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Defines the forward pass of the model.

        Args:
            x (torch.Tensor): Input tensor of shape (B, T, C, H, W), where
                B=batch, T=time steps, C=channels, H=height, W=width.

        Returns:
            torch.Tensor: Output tensor of shape (B, C, H, W), representing the
                predicted grid for the next time step.
        """
        # Reshape for Conv3D: (B, T, C, H, W) -> (B, C, T, H, W)
        x = x.permute(0, 2, 1, 3, 4)

        features = self.encoder(x)
        out = self.decoder(features)

        # The decoder outputs a sequence; we take the last time step as the prediction.
        out = out[:, :, -1, :, :]

        return out

===== models/cnn_lstm.py =====
import torch
import torch.nn as nn


class CNNLSTMModel(nn.Module):
    def __init__(self, config):
        super().__init__()

        hidden_dim = config["model"]["hidden_dim"]

        self.cnn = nn.Sequential(
            nn.Conv2d(1, hidden_dim, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(hidden_dim, hidden_dim, 3, padding=1),
            nn.ReLU()
        )

        self.lstm = nn.LSTM(
            input_size=hidden_dim,
            hidden_size=hidden_dim,
            batch_first=True
        )

        self.decoder = nn.Conv2d(hidden_dim, 1, kernel_size=1)

    def forward(self, x):
        B, T, C, H, W = x.shape

        spatial_feats = []
        spatial_maps = []

        for t in range(T):
            feat = self.cnn(x[:, t])
            spatial_maps.append(feat)
            spatial_feats.append(feat.mean(dim=[2, 3]))

        seq = torch.stack(spatial_feats, dim=1)

        lstm_out, _ = self.lstm(seq)

        temporal_context = lstm_out[:, -1].unsqueeze(-1).unsqueeze(-1)
        fused = spatial_maps[-1] + temporal_context
        return self.decoder(fused)

===== models/lstm_baseline.py =====
"""Per-grid-cell LSTM baseline for next-day temperature maps."""

import torch
import torch.nn as nn


class LSTMBaseline(nn.Module):
    """Apply one shared temporal LSTM independently to every grid cell."""

    def __init__(self, config):
        super().__init__()
        hidden_dim = config["model"].get("lstm_hidden_dim", config["model"]["hidden_dim"])
        self.lstm = nn.LSTM(input_size=1, hidden_size=hidden_dim, batch_first=True)
        self.output = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        batch, timesteps, channels, height, width = x.shape
        sequence = x[:, :, 0].permute(0, 2, 3, 1).reshape(batch * height * width, timesteps, 1)
        encoded, _ = self.lstm(sequence)
        prediction = self.output(encoded[:, -1]).reshape(batch, height, width)
        return prediction.unsqueeze(1)

===== models/transformer.py =====
import torch
import torch.nn as nn


class SpatioTemporalTransformer(nn.Module):
    def __init__(self, config):
        super().__init__()

        d_model = config["model"]["hidden_dim"]

        self.input_projection = nn.Conv2d(1, d_model, kernel_size=1)

        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=4, batch_first=True),
            num_layers=2
        )

        self.decoder = nn.Conv2d(d_model, 1, kernel_size=1)

    def forward(self, x):
        B, T, C, H, W = x.shape

        feature_maps = [self.input_projection(x[:, t]) for t in range(T)]
        sequence = torch.stack(
            [feature_map.mean(dim=(2, 3)) for feature_map in feature_maps], dim=1
        )
        temporal_context = self.transformer(sequence)[:, -1]
        fused = feature_maps[-1] + temporal_context.unsqueeze(-1).unsqueeze(-1)
        return self.decoder(fused)

SOURCE dims {'time': 61368, 'latitude': 121, 'longitude': 141} vars ['t2m'] attrs {'GRIB_paramId': np.int64(167), 'GRIB_dataType': 'an', 'GRIB_numberOfPoints': np.int64(1038240), 'GRIB_typeOfLevel': 'surface', 'GRIB_stepUnits': np.int64(1), 'GRIB_stepType': 'instant', 'GRIB_gridType': 'regular_ll', 'GRIB_uvRelativeToGrid': np.int64(0), 'GRIB_NV': np.int64(0), 'GRIB_Nx': np.int64(1440), 'GRIB_Ny': np.int64(721), 'GRIB_cfName': 'unknown', 'GRIB_cfVarName': 't2m', 'GRIB_gridDefinitionDescription': 'Latitude/Longitude Grid', 'GRIB_iDirectionIncrementInDegrees': np.float64(0.25), 'GRIB_iScansNegatively': np.int64(0), 'GRIB_jDirectionIncrementInDegrees': np.float64(0.25), 'GRIB_jPointsAreConsecutive': np.int64(0), 'GRIB_jScansPositively': np.int64(0), 'GRIB_latitudeOfFirstGridPointInDegrees': np.float64(90.0), 'GRIB_latitudeOfLastGridPointInDegrees': np.float64(-90.0), 'GRIB_longitudeOfFirstGridPointInDegrees': np.float64(0.0), 'GRIB_longitudeOfLastGridPointInDegrees': np.float64(359.75), 'GRIB_missingValue': np.float64(3.4028234663852886e+38), 'GRIB_name': '2 metre temperature', 'GRIB_shortName': '2t', 'GRIB_totalNumber': np.int64(0), 'GRIB_units': 'K', 'long_name': '2 metre temperature', 'units': 'K', 'standard_name': 'unknown', 'GRIB_surface': np.float64(0.0)}
time first/last/count 2019-01-01T00:00:00.000000000 2025-12-31T23:00:00.000000000 61368 monotonic True
sample stats 234.3179473876953 307.99383544921875
time duplicates False

Prior experiment files
```

## 2026-10-13 â€” Timestamped backup

Command: copied run_baseline_experiments.py before targeted changes.

Backup: `backups\pipeline_20261013_222743\run_baseline_experiments.py`


## Preprocessing rebuild

Command: .venv\Scripts\python.exe preprocessing\rebuild_verified.py

```text
python.exe : Traceback (most recent call last):
At line:9 char:5
+ '@; & .\.venv\Scripts\python.exe preprocessing\rebuild_verified.py 2> ...
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError

  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\preprocessing\rebuild_verified.py", line
154, in <module>
    main()
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\preprocessing\rebuild_verified.py", line
76, in main
    atomic_netcdf(hourly, hourly_path)
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\preprocessing\rebuild_verified.py", line
27, in atomic_netcdf
    os.replace(temp, path)
PermissionError: [WinError 5] Access is denied:
'C:\\Users\\25mdsml006\\Desktop\\deep_learning\\project\\climate\\climate2\\data\\interim\\train.nc.tmp' ->
'C:\\Users\\25mdsml006\\Desktop\\deep_learning\\project\\climate\\climate2\\data\\interim\\train.nc'

Exit code: 1
```

## Preprocessing rebuild retry after Windows file lock

Command: .venv\Scripts\python.exe preprocessing\rebuild_verified.py

```text
train: existing hourly split verified byte-value equivalent to source; reusing it.
Exit code: 1 (stopped to avoid repeating the remaining exhaustive comparisons).
```

## Preprocessing rebuild (resume with validated hourly splits)

Command: .venv\Scripts\python.exe preprocessing\rebuild_verified.py

```text
Source timestamp integrity checked; full finite/range scan was completed during the first rebuild attempt.
train: existing hourly split bounds and finite values verified; reusing it.
Daily files were written and passed the rebuild script checks for expected day counts, finite values and plausible Kelvin range; normalization had not started when this process was stopped. Exit code: 1 (intentional Ctrl+C).
```

## Log cleanup

Repaired mixed UTF-8/UTF-16 append output, normalized code fences, and removed consecutive duplicate headings. A pre-repair copy is in backups.


## Current checkpoint after interruption

- No preprocessing Python process remained after Ctrl+C.
- Source timestamp/cadence scan passed in the earlier run; full source finite/range scan also completed before the first run reached the Windows rename error.
- train.nc was compared value-for-value with the verified source and matched.
- val.nc and test.nc have not been compared value-for-value with source; their bounds, cadence, dimensions and chunked finiteness are checked by the new chunked rebuild. Source equality remains explicitly unverified for those splits.
- The previous run wrote daily files but did not complete normalization. Current daily outputs are backed up under backups/pre_chunked_20261013_233446 (see directory name).

## Chunked downstream rebuild

Command: .venv\Scripts\python.exe -u preprocessing\rebuild_downstream.py

```text
First chunked pass stopped before producing outputs; train finite scan was redundant.
Exit code: 1 (intentional Ctrl+C).
```

Command: python -m py_compile preprocessing/rebuild_downstream.py verify_preprocessing.py run_baseline_experiments.py
Exit code: 0

## Chunked downstream rebuild, attempt 2

Command: .venv\Scripts\python.exe -u preprocessing\rebuild_downstream.py

```text
train: validated 43824 hourly records, bounds, cadence, dimensions, Kelvin units and finite values.
train: daily aggregation chunk 0:31 passed.
One-year chunk py_compile check: preprocessing/rebuild_downstream.py, verify_preprocessing.py, run_baseline_experiments.py
Exit code: 0
```

## Chunked downstream rebuild, one-year I/O chunks

Command: .venv\Scripts\python.exe -u preprocessing\rebuild_downstream.py

```text
train: validated 43824 hourly records, bounds, cadence, dimensions, Kelvin units; temperature finiteness checked during daily aggregation.
Storage-aligned chunk implementation syntax check exit code: 0
```

## Storage-aligned daily rebuild and preprocessing

Command: .venv\Scripts\python.exe -u preprocessing\rebuild_downstream.py

```text
train: validated 43824 hourly records, bounds, cadence, dimensions, Kelvin units; temperature finiteness checked during daily aggregation.
train: reading NetCDF time chunks of 7304 hours.
train: aggregated storage chunk 0:7304; days=304; carry_hours=8.
train: aggregated storage chunk 7304:14608; days=608; carry_hours=16.
train: aggregated storage chunk 14608:21912; days=913; carry_hours=0.
train: aggregated storage chunk 21912:29216; days=1217; carry_hours=8.
train: aggregated storage chunk 29216:36520; days=1521; carry_hours=16.
train: aggregated storage chunk 36520:43824; days=1826; carry_hours=0.
train: wrote validated daily maximum file (1826 days) to data\interim\train_daily.nc.
val: validated 8784 hourly records, bounds, cadence, dimensions, Kelvin units and chunked finite values.
val: reading NetCDF time chunks of 2196 hours.
val: aggregated storage chunk 0:2196; days=91; carry_hours=12.
val: aggregated storage chunk 2196:4392; days=183; carry_hours=0.
val: aggregated storage chunk 4392:6588; days=274; carry_hours=12.
val: aggregated storage chunk 6588:8784; days=366; carry_hours=0.
val: wrote validated daily maximum file (366 days) to data\interim\val_daily.nc.
test: validated 8760 hourly records, bounds, cadence, dimensions, Kelvin units and chunked finite values.
test: reading NetCDF time chunks of 2190 hours.
test: aggregated storage chunk 0:2190; days=91; carry_hours=6.
test: aggregated storage chunk 2190:4380; days=182; carry_hours=12.
test: aggregated storage chunk 4380:6570; days=273; carry_hours=18.
test: aggregated storage chunk 6570:8760; days=365; carry_hours=0.
test: wrote validated daily maximum file (365 days) to data\interim\test_daily.nc.
Training-only normalization: mean=25.04454902 C, std=10.99594437 C, values=31153386.
train: normalized days=1826; sequence samples=1819; length=7.
val: normalized days=366; sequence samples=359; length=7.
test: normalized days=365; sequence samples=358; length=7.
Exit code: 0
```

## Preprocessing verification

Command: .venv\Scripts\python.exe -u verify_preprocessing.py

```text
PASS verified source exists
PASS source dimensions
PASS source timestamp endpoints
PASS source timestamps unique
PASS source has continuous hourly cadence
PASS source temperature units are Kelvin
PASS normalization mean/std finite and std positive
PASS normalization units documented
PASS train hourly count and bounds
PASS train hourly cadence continuous
PASS train daily count and dates
PASS train daily dimensions
PASS train daily values finite
PASS train daily Kelvin range plausible
PASS train daily units Kelvin
PASS hourly storage chunk at 0 finite
PASS hourly storage chunk at 7304 finite
PASS hourly storage chunk at 14608 finite
PASS hourly storage chunk at 21912 finite
PASS hourly storage chunk at 29216 finite
PASS hourly storage chunk at 36520 finite
PASS hourly chunk boundaries end on a full day
PASS daily sample reconstruction count
PASS train daily max and 24-hour grouping reproducible
PASS train processed daily shape
PASS data\processed\train.npy finite block 0
PASS data\processed\train.npy finite block 64
PASS data\processed\train.npy finite block 128
PASS data\processed\train.npy finite block 192
PASS data\processed\train.npy finite block 256
PASS data\processed\train.npy finite block 320
PASS data\processed\train.npy finite block 384
PASS data\processed\train.npy finite block 448
PASS data\processed\train.npy finite block 512
PASS data\processed\train.npy finite block 576
PASS data\processed\train.npy finite block 640
PASS data\processed\train.npy finite block 704
PASS data\processed\train.npy finite block 768
PASS data\processed\train.npy finite block 832
PASS data\processed\train.npy finite block 896
PASS data\processed\train.npy finite block 960
PASS data\processed\train.npy finite block 1024
PASS data\processed\train.npy finite block 1088
PASS data\processed\train.npy finite block 1152
PASS data\processed\train.npy finite block 1216
PASS data\processed\train.npy finite block 1280
PASS data\processed\train.npy finite block 1344
PASS data\processed\train.npy finite block 1408
PASS data\processed\train.npy finite block 1472
PASS data\processed\train.npy finite block 1536
PASS data\processed\train.npy finite block 1600
PASS data\processed\train.npy finite block 1664
PASS data\processed\train.npy finite block 1728
PASS data\processed\train.npy finite block 1792
PASS train inverse normalization reconstructs sampled Celsius values
PASS train X sequence shape
PASS train y sequence shape
PASS data\processed\tensors\train_X.npy finite block 0
PASS data\processed\tensors\train_X.npy finite block 64
PASS data\processed\tensors\train_X.npy finite block 128
PASS data\processed\tensors\train_X.npy finite block 192
PASS data\processed\tensors\train_X.npy finite block 256
PASS data\processed\tensors\train_X.npy finite block 320
PASS data\processed\tensors\train_X.npy finite block 384
PASS data\processed\tensors\train_X.npy finite block 448
PASS data\processed\tensors\train_X.npy finite block 512
PASS data\processed\tensors\train_X.npy finite block 576
PASS data\processed\tensors\train_X.npy finite block 640
PASS data\processed\tensors\train_X.npy finite block 704
PASS data\processed\tensors\train_X.npy finite block 768
PASS data\processed\tensors\train_X.npy finite block 832
PASS data\processed\tensors\train_X.npy finite block 896
PASS data\processed\tensors\train_X.npy finite block 960
PASS data\processed\tensors\train_X.npy finite block 1024
PASS data\processed\tensors\train_X.npy finite block 1088
PASS data\processed\tensors\train_X.npy finite block 1152
PASS data\processed\tensors\train_X.npy finite block 1216
PASS data\processed\tensors\train_X.npy finite block 1280
PASS data\processed\tensors\train_X.npy finite block 1344
PASS data\processed\tensors\train_X.npy finite block 1408
PASS data\processed\tensors\train_X.npy finite block 1472
PASS data\processed\tensors\train_X.npy finite block 1536
PASS data\processed\tensors\train_X.npy finite block 1600
PASS data\processed\tensors\train_X.npy finite block 1664
PASS data\processed\tensors\train_X.npy finite block 1728
PASS data\processed\tensors\train_X.npy finite block 1792
PASS data\processed\tensors\train_y.npy finite block 0
PASS data\processed\tensors\train_y.npy finite block 64
PASS data\processed\tensors\train_y.npy finite block 128
PASS data\processed\tensors\train_y.npy finite block 192
PASS data\processed\tensors\train_y.npy finite block 256
PASS data\processed\tensors\train_y.npy finite block 320
PASS data\processed\tensors\train_y.npy finite block 384
PASS data\processed\tensors\train_y.npy finite block 448
PASS data\processed\tensors\train_y.npy finite block 512
PASS data\processed\tensors\train_y.npy finite block 576
PASS data\processed\tensors\train_y.npy finite block 640
PASS data\processed\tensors\train_y.npy finite block 704
PASS data\processed\tensors\train_y.npy finite block 768
PASS data\processed\tensors\train_y.npy finite block 832
PASS data\processed\tensors\train_y.npy finite block 896
PASS data\processed\tensors\train_y.npy finite block 960
PASS data\processed\tensors\train_y.npy finite block 1024
PASS data\processed\tensors\train_y.npy finite block 1088
PASS data\processed\tensors\train_y.npy finite block 1152
PASS data\processed\tensors\train_y.npy finite block 1216
PASS data\processed\tensors\train_y.npy finite block 1280
PASS data\processed\tensors\train_y.npy finite block 1344
PASS data\processed\tensors\train_y.npy finite block 1408
PASS data\processed\tensors\train_y.npy finite block 1472
PASS data\processed\tensors\train_y.npy finite block 1536
PASS data\processed\tensors\train_y.npy finite block 1600
PASS data\processed\tensors\train_y.npy finite block 1664
PASS data\processed\tensors\train_y.npy finite block 1728
PASS data\processed\tensors\train_y.npy finite block 1792
PASS train X sample 0 reproducible
PASS train y sample 0 reproducible
PASS train X sample 909 reproducible
PASS train y sample 909 reproducible
PASS train X sample 1818 reproducible
PASS train y sample 1818 reproducible
PASS train first target follows 7 inputs
PASS train last target date
PASS val hourly count and bounds
PASS val hourly cadence continuous
PASS val daily count and dates
PASS val daily dimensions
PASS val daily values finite
PASS val daily Kelvin range plausible
PASS val daily units Kelvin
PASS hourly storage chunk at 0 finite
PASS hourly storage chunk at 2196 finite
PASS hourly storage chunk at 4392 finite
PASS hourly storage chunk at 6588 finite
PASS hourly chunk boundaries end on a full day
PASS daily sample reconstruction count
PASS val daily max and 24-hour grouping reproducible
PASS val processed daily shape
PASS data\processed\val.npy finite block 0
PASS data\processed\val.npy finite block 64
PASS data\processed\val.npy finite block 128
PASS data\processed\val.npy finite block 192
PASS data\processed\val.npy finite block 256
PASS data\processed\val.npy finite block 320
PASS val inverse normalization reconstructs sampled Celsius values
PASS val X sequence shape
PASS val y sequence shape
PASS data\processed\tensors\val_X.npy finite block 0
PASS data\processed\tensors\val_X.npy finite block 64
PASS data\processed\tensors\val_X.npy finite block 128
PASS data\processed\tensors\val_X.npy finite block 192
PASS data\processed\tensors\val_X.npy finite block 256
PASS data\processed\tensors\val_X.npy finite block 320
PASS data\processed\tensors\val_y.npy finite block 0
PASS data\processed\tensors\val_y.npy finite block 64
PASS data\processed\tensors\val_y.npy finite block 128
PASS data\processed\tensors\val_y.npy finite block 192
PASS data\processed\tensors\val_y.npy finite block 256
PASS data\processed\tensors\val_y.npy finite block 320
PASS val X sample 0 reproducible
PASS val y sample 0 reproducible
PASS val X sample 179 reproducible
PASS val y sample 179 reproducible
PASS val X sample 358 reproducible
PASS val y sample 358 reproducible
PASS val first target follows 7 inputs
PASS val last target date
PASS test hourly count and bounds
PASS test hourly cadence continuous
PASS test daily count and dates
PASS test daily dimensions
PASS test daily values finite
PASS test daily Kelvin range plausible
PASS test daily units Kelvin
PASS hourly storage chunk at 0 finite
PASS hourly storage chunk at 2190 finite
PASS hourly storage chunk at 4380 finite
PASS hourly storage chunk at 6570 finite
PASS hourly chunk boundaries end on a full day
PASS daily sample reconstruction count
PASS test daily max and 24-hour grouping reproducible
PASS test processed daily shape
PASS data\processed\test.npy finite block 0
PASS data\processed\test.npy finite block 64
PASS data\processed\test.npy finite block 128
PASS data\processed\test.npy finite block 192
PASS data\processed\test.npy finite block 256
PASS data\processed\test.npy finite block 320
PASS test inverse normalization reconstructs sampled Celsius values
PASS test X sequence shape
PASS test y sequence shape
PASS data\processed\tensors\test_X.npy finite block 0
PASS data\processed\tensors\test_X.npy finite block 64
PASS data\processed\tensors\test_X.npy finite block 128
PASS data\processed\tensors\test_X.npy finite block 192
PASS data\processed\tensors\test_X.npy finite block 256
PASS data\processed\tensors\test_X.npy finite block 320
PASS data\processed\tensors\test_y.npy finite block 0
PASS data\processed\tensors\test_y.npy finite block 64
PASS data\processed\tensors\test_y.npy finite block 128
PASS data\processed\tensors\test_y.npy finite block 192
PASS data\processed\tensors\test_y.npy finite block 256
PASS data\processed\tensors\test_y.npy finite block 320
PASS test X sample 0 reproducible
PASS test y sample 0 reproducible
PASS test X sample 179 reproducible
PASS test y sample 179 reproducible
PASS test X sample 357 reproducible
PASS test y sample 357 reproducible
PASS test first target follows 7 inputs
PASS test last target date
PASS train/val targets do not overlap
PASS val/test targets do not overlap
All preprocessing checks passed.
Exit code: 0
```

## CUDA one-epoch smoke test

Command: .venv\Scripts\python.exe -u run_baseline_experiments.py --epochs 1 --batch-size 16 --seed 42 --device cuda --models convlstm --output-dir experiments/reviewer_baselines_verified_20261013_smoke

```text
Selected device: cuda
GPU: NVIDIA GeForce RTX 4070; PyTorch 2.5.1+cu121; CUDA runtime 12.1
Traceback (most recent call last):
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\training\losses.py", line 21, in __init__
    with open(threshold_path, "r") as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'data/processed/extreme_thresholds.json'
System.Management.Automation.RemoteException
During handling of the above exception, another exception occurred:
System.Management.Automation.RemoteException
Traceback (most recent call last):
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\run_baseline_experiments.py", line 264, in <module>
    main()
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\run_baseline_experiments.py", line 229, in main
    results.append(run_learned_model(name, config, data, mean, std, device, args.epochs, args.batch_size, output_dir))
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\run_baseline_experiments.py", line 107, in run_learned_model
    loss_fn = get_loss(config["training"])
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\training\losses.py", line 61, in get_loss
    return ExtremeWeightedMSE(extreme_weight=extreme_weight)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\training\losses.py", line 35, in __init__
    print("\u26a0\ufe0f Warning: Could not load threshold/stat files.")
  File "C:\Users\25mdsml006\AppData\Local\Programs\Python\Python311\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 0-1: character maps to <undefined>
Exit code: 1
```

## CUDA one-epoch smoke test retry

Command: .venv\Scripts\python.exe -u run_baseline_experiments.py --epochs 1 --batch-size 16 --seed 42 --device cuda --models convlstm --output-dir experiments/reviewer_baselines_verified_20261013_smoke_retry

```text
Selected device: cuda
GPU: NVIDIA GeForce RTX 4070; PyTorch 2.5.1+cu121; CUDA runtime 12.1
Warning: threshold/stat files unavailable; using default normalized threshold 0.
Using default threshold = 0.
Error: [Errno 2] No such file or directory: 'data/processed/extreme_thresholds.json'
Traceback (most recent call last):
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\run_baseline_experiments.py", line 264, in <module>
    main()
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\run_baseline_experiments.py", line 229, in main
    results.append(run_learned_model(name, config, data, mean, std, device, args.epochs, args.batch_size, output_dir))
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\run_baseline_experiments.py", line 137, in run_learned_model
    raise RuntimeError("Model, inputs, and targets are not on the selected device")
RuntimeError: Model, inputs, and targets are not on the selected device
Exit code: 1
```

## CUDA one-epoch smoke test, canonical device retry

Command: .venv\Scripts\python.exe -u run_baseline_experiments.py --epochs 1 --batch-size 16 --seed 42 --device cuda --models convlstm --output-dir experiments/reviewer_baselines_verified_20261013_smoke_retry2

```text
Selected device: cuda:0
GPU: NVIDIA GeForce RTX 4070; PyTorch 2.5.1+cu121; CUDA runtime 12.1
Warning: threshold/stat files unavailable; using default normalized threshold 0.
Using default threshold = 0.
Error: [Errno 2] No such file or directory: 'data/processed/extreme_thresholds.json'
convlstm epoch 1/1: train_loss=0.374847, val_loss=0.088359
{
  "protocol": {
    "sequence_length": 7,
    "forecast_horizon_days": 1,
    "train_samples": 1819,
    "validation_samples": 359,
    "test_samples": 358,
    "spatial_shape": [
      121,
      141
    ],
    "device": "cuda:0",
    "seed": 42,
    "metric_space": "same denormalized stored temperature scale for every model",
    "normalization_unit": "degrees_Celsius",
    "pytorch_version": "2.5.1+cu121",
    "cuda_runtime": "12.1",
    "run_timestamp_utc": "2026-10-13T18:29:20.571251+00:00",
    "epochs_requested": 1,
    "output_directory": "C:\\Users\\25mdsml006\\Desktop\\deep_learning\\project\\climate\\climate2\\experiments\\reviewer_baselines_verified_20261013_smoke_retry2"
  },
  "results": [
    {
      "model": "convlstm",
      "class": "ConvLSTMModel",
      "trainable_parameters": 29441,
      "epochs": 1,
      "batch_size": 16,
      "optimizer": "Adam",
      "learning_rate": 0.0001,
      "loss": "ExtremeWeightedMSE",
      "training_seconds": 10.567,
      "best_epoch": 1,
      "best_validation_loss": 0.08835883309011874,
      "history": [
        {
          "epoch": 1,
          "train_loss": 0.37484744021244215,
          "validation_loss": 0.08835883309011874
        }
      ],
      "validation": {
        "rmse": 1.9353584020718784,
        "mae": 1.2467384338378906,
        "r2": 0.9675708413124084,
        "correlation": 0.9837510867777218
      },
      "test": {
        "rmse": 1.9316340833038244,
        "mae": 1.2535701990127563,
        "r2": 0.9656150341033936,
        "correlation": 0.9828383553043664
      },
      "checkpoint": "experiments\\reviewer_baselines_verified_20261013_smoke_retry2\\convlstm_best.pth"
    }
  ]
}
Exit code: 0
```

## Full baseline comparison

Command: .venv\Scripts\python.exe -u run_baseline_experiments.py --epochs 50 --batch-size 16 --seed 42 --device cuda --models persistence,lstm,cnn_lstm,convlstm,transformer --output-dir experiments/reviewer_baselines_verified_20261013

```text
Selected device: cuda:0
GPU: NVIDIA GeForce RTX 4070; PyTorch 2.5.1+cu121; CUDA runtime 12.1
Warning: threshold/stat files unavailable; using default normalized threshold 0.
Using default threshold = 0.
Error: [Errno 2] No such file or directory: 'data/processed/extreme_thresholds.json'
lstm epoch 1/50: train_loss=2.055518, val_loss=1.874743
lstm epoch 2/50: train_loss=1.553829, val_loss=1.316166
lstm epoch 3/50: train_loss=1.038983, val_loss=0.823757
lstm epoch 4/50: train_loss=0.718050, val_loss=0.582027
lstm epoch 5/50: train_loss=0.487198, val_loss=0.360775
lstm epoch 6/50: train_loss=0.297711, val_loss=0.225081
lstm epoch 7/50: train_loss=0.208384, val_loss=0.177933
lstm epoch 8/50: train_loss=0.174094, val_loss=0.156201
lstm epoch 9/50: train_loss=0.154370, val_loss=0.140735
lstm epoch 10/50: train_loss=0.139425, val_loss=0.128045
lstm epoch 11/50: train_loss=0.127465, val_loss=0.117891
lstm epoch 12/50: train_loss=0.117843, val_loss=0.109567
lstm epoch 13/50: train_loss=0.110166, val_loss=0.103520
lstm epoch 14/50: train_loss=0.104227, val_loss=0.098111
lstm epoch 15/50: train_loss=0.099471, val_loss=0.094523
lstm epoch 16/50: train_loss=0.095750, val_loss=0.091336
lstm epoch 17/50: train_loss=0.092928, val_loss=0.088893
lstm epoch 18/50: train_loss=0.090645, val_loss=0.087021
lstm epoch 19/50: train_loss=0.088759, val_loss=0.085488
lstm epoch 20/50: train_loss=0.087117, val_loss=0.083994
lstm epoch 21/50: train_loss=0.085700, val_loss=0.082723
lstm epoch 22/50: train_loss=0.084404, val_loss=0.081613
lstm epoch 23/50: train_loss=0.083233, val_loss=0.080505
lstm epoch 24/50: train_loss=0.082060, val_loss=0.079665
lstm epoch 25/50: train_loss=0.081052, val_loss=0.078480
lstm epoch 26/50: train_loss=0.080034, val_loss=0.077668
lstm epoch 27/50: train_loss=0.079042, val_loss=0.076627
lstm epoch 28/50: train_loss=0.078023, val_loss=0.075909
lstm epoch 29/50: train_loss=0.077173, val_loss=0.074847
lstm epoch 30/50: train_loss=0.076255, val_loss=0.074024
lstm epoch 31/50: train_loss=0.075437, val_loss=0.073239
lstm epoch 32/50: train_loss=0.074485, val_loss=0.072484
lstm epoch 33/50: train_loss=0.073695, val_loss=0.071611
lstm epoch 34/50: train_loss=0.073077, val_loss=0.070857
lstm epoch 35/50: train_loss=0.072149, val_loss=0.070109
lstm epoch 36/50: train_loss=0.071371, val_loss=0.069342
lstm epoch 37/50: train_loss=0.070695, val_loss=0.068715
lstm epoch 38/50: train_loss=0.069871, val_loss=0.067999
lstm epoch 39/50: train_loss=0.069051, val_loss=0.067216
lstm epoch 40/50: train_loss=0.068401, val_loss=0.066590
lstm epoch 41/50: train_loss=0.067629, val_loss=0.065784
lstm epoch 42/50: train_loss=0.066912, val_loss=0.065021
lstm epoch 43/50: train_loss=0.066087, val_loss=0.064880
lstm epoch 44/50: train_loss=0.065395, val_loss=0.063625
lstm epoch 45/50: train_loss=0.064622, val_loss=0.062953
lstm epoch 46/50: train_loss=0.063812, val_loss=0.062194
lstm epoch 47/50: train_loss=0.063090, val_loss=0.061506
lstm epoch 48/50: train_loss=0.062408, val_loss=0.060862
lstm epoch 49/50: train_loss=0.061763, val_loss=0.060340
lstm epoch 50/50: train_loss=0.060955, val_loss=0.060012
Warning: threshold/stat files unavailable; using default normalized threshold 0.
Using default threshold = 0.
Error: [Errno 2] No such file or directory: 'data/processed/extreme_thresholds.json'
cnn_lstm epoch 1/50: train_loss=0.743421, val_loss=0.236616
cnn_lstm epoch 2/50: train_loss=0.124414, val_loss=0.077553
cnn_lstm epoch 3/50: train_loss=0.072561, val_loss=0.069712
```

## Reviewer evidence checks and aligned smoke analysis (2026-10-14)

### Current process check

Command: `Get-Process python,pythonw -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,CPU,StartTime`

```text
No Python or pythonw process rows were returned.
The prior 50-epoch command has no active unified session and produced no aggregate comparison_results.json/.csv. Its final exit code was not captured; artifact state shows LSTM checkpoint and a partial CNN-LSTM checkpoint only.
Windows Get-CimInstance Win32_Process and tasklist returned Access denied, so no claim is made from those commands.
```

### Historical daily_resampled.nc current-state scan

Command: chunked scan over 32-day reads of `data/interim/daily_resampled.nc`; exit code 0.

```text
Chunked scan data\interim\daily_resampled.nc: cells=43624977, finite=0, NaN=43624977, Inf=0, chunks=32 days
Conclusion: do not use this legacy artifact.
```

### Current stats and software metadata

Command: inspect NetCDF headers, stats JSON, and installed package/device versions. Header inspection process exit code 1 because the legacy file had no explicit chunksizes and the initial probe did not apply its fallback; the reported metadata before that exception and the separate complete NaN scan above are retained. Current normalization stats read successfully.

```text
Python 3.11.9; torch 2.5.1+cu121; CUDA 12.1; numpy 2.4.2; xarray 2026.2.0; scipy 1.17.1; sklearn 1.8.0
GPU NVIDIA GeForce RTX 4070
Source: time=61368, latitude=121, longitude=141; time 2019-01-01T00:00 through 2025-12-31T23:00; lat 35 to 5; lon 65 to 100; t2m units K.
Train: time=43824; 2019-01-01T00:00 through 2023-12-31T23:00; lat 35 to 5; lon 65 to 100; t2m units K.
Validation: time=8784; 2024-01-01T00:00 through 2024-12-31T23:00; lat 35 to 5; lon 65 to 100; t2m units K.
Test: time=8760; 2025-01-01T00:00 through 2025-12-31T23:00; lat 35 to 5; lon 65 to 100; t2m units K.
mean_std.json: mean=25.044549020486595 C; std=10.99594436868629 C; training_value_count=31153386; finite training-only population statistics.
```

### Fresh aligned prediction and persistence analysis

Command: `.venv\Scripts\python.exe -u experiments\reviewer_followup_analysis_20261014\analyze_smoke.py`; exit code 0. This loads the saved one-epoch Conv3D smoke checkpoint, performs inference on rebuilt test tensors, aligns targets to 2025-01-08 through 2025-12-31, recalculates metrics, and writes `experiments/reviewer_followup_analysis_20261014/followup_analysis.json`.

```text
Smoke Conv3D, 358 aligned dates / 6,107,838 grid values: RMSE 1.93163408 C; MAE 1.25357020 C; R2 0.96561503; Pearson r 0.98283836.
Persistence, identical 358 dates: RMSE 1.40271573 C; MAE 0.89749843 C; R2 0.98186749; Pearson r 0.99093668.
Common 351 test dates for 7/14-day window comparison (2025-01-15 to 2025-12-31): persistence RMSE 1.39585339 C; MAE 0.89275551 C; R2 0.98176080; Pearson r 0.99088221.
Persistence natural windows: 3-day=362 samples, RMSE 1.40705531 C, MAE 0.89967030 C; 7-day=358, RMSE 1.40271573 C, MAE 0.89749843 C; 14-day=351, RMSE 1.39585339 C, MAE 0.89275551 C.
Smoke seasonal RMSE/MAE C: DJF 2.09896/1.29798 (83 target days); MAM 2.10128/1.38126 (92); JJA 1.77273/1.20579 (92); SON 1.73767/1.13228 (91).
Smoke gridpoint RMSE C: minimum 0.39272, mean 1.57359, maximum 14.54708 at 35.0 N, 65.0 E.
Status: diagnostic only; one-epoch checkpoint, not a final result.
```

The first invocation of the new analysis script exited 1 with `ModuleNotFoundError: No module named 'models'`; the script was corrected to add the project root to `sys.path` and the successful rerun above exited 0. No training was launched for this analysis.

### Full baseline comparison status

The previously launched command was `.venv\Scripts\python.exe -u run_baseline_experiments.py --epochs 50 --batch-size 16 --seed 42 --device cuda --models persistence,lstm,cnn_lstm,convlstm,transformer --output-dir experiments\reviewer_baselines_verified_20261013`. Its terminal log records LSTM epoch 50/50, CNN-LSTM epoch 3/50, and then ends. The output folder has LSTM and CNN-LSTM checkpoints but no aggregate JSON/CSV. The session handle later became unavailable and no final exit code was captured. Current process query returned no Python process. Do not report this as a completed comparison.

## Final deliverable integrity check (2026-10-14)

Command: Python Markdown fence/duplicate-heading check, JSON parse, followed by `git status --short`.

```text
terminal_outputs.md: fence_markers=42; balanced=True; duplicate_headings=[]
reviewer_questions_answers.md: fence_markers=6; balanced=True; duplicate_headings=[]
followup_analysis.json: valid JSON; targets=358; period=2025-01-08..2025-12-31
reviewer_questions_answers.md: 18454 bytes
Exit code: 0
```

`git status --short` showed the expected project edits/new outputs, the previously confirmed empty `file.tmp` deletion, and the existing untracked `revision/` folder. No source hourly split, verified raw source, `revision/`, old `outputs/` result, or `experiments/latest/model.pth` was modified.

## Corrected-threshold five-model comparison (2026-10-14)

Command: `.venv\Scripts\python.exe -u run_baseline_experiments.py --epochs 50 --batch-size 16 --seed 42 --device cuda --models persistence,lstm,cnn_lstm,convlstm,transformer --output-dir experiments\reviewer_final_20261014`

```text
Selected device: cuda:0
GPU: NVIDIA GeForce RTX 4070; PyTorch 2.5.1+cu121; CUDA runtime 12.1
lstm epoch 1/50: train_loss=1.357386, val_loss=1.281001
lstm epoch 2/50: train_loss=1.123565, val_loss=0.990448
lstm epoch 3/50: train_loss=0.786988, val_loss=0.586715
lstm epoch 4/50: train_loss=0.424891, val_loss=0.273033
lstm epoch 5/50: train_loss=0.198155, val_loss=0.131722
lstm epoch 6/50: train_loss=0.117567, val_loss=0.098101
cnn_lstm epoch 28/50: train_loss=0.020636, val_loss=0.021028
cnn_lstm epoch 29/50: train_loss=0.020636, val_loss=0.020985
cnn_lstm epoch 30/50: train_loss=0.020462, val_loss=0.020824
cnn_lstm epoch 31/50: train_loss=0.020424, val_loss=0.020782
cnn_lstm epoch 32/50: train_loss=0.020278, val_loss=0.020845
cnn_lstm epoch 33/50: train_loss=0.020356, val_loss=0.020782
cnn_lstm epoch 34/50: train_loss=0.020225, val_loss=0.020681
cnn_lstm epoch 35/50: train_loss=0.020256, val_loss=0.020697
cnn_lstm epoch 36/50: train_loss=0.020158, val_loss=0.020594
cnn_lstm epoch 37/50: train_loss=0.020156, val_loss=0.020480
cnn_lstm epoch 38/50: train_loss=0.020122, val_loss=0.020793
cnn_lstm epoch 39/50: train_loss=0.020118, val_loss=0.020607
cnn_lstm epoch 40/50: train_loss=0.020032, val_loss=0.020520
cnn_lstm epoch 41/50: train_loss=0.020019, val_loss=0.020340
cnn_lstm epoch 42/50: train_loss=0.019948, val_loss=0.020330
cnn_lstm epoch 43/50: train_loss=0.019948, val_loss=0.020298
cnn_lstm epoch 44/50: train_loss=0.019978, val_loss=0.020266
cnn_lstm epoch 45/50: train_loss=0.019888, val_loss=0.020266
cnn_lstm epoch 46/50: train_loss=0.019878, val_loss=0.020291
cnn_lstm epoch 47/50: train_loss=0.019883, val_loss=0.020341
cnn_lstm epoch 48/50: train_loss=0.019879, val_loss=0.020235
cnn_lstm epoch 49/50: train_loss=0.019781, val_loss=0.020444
cnn_lstm epoch 50/50: train_loss=0.019849, val_loss=0.020382
convlstm epoch 1/50: train_loss=0.198028, val_loss=0.040255
convlstm epoch 2/50: train_loss=0.035582, val_loss=0.031816
convlstm epoch 3/50: train_loss=0.028540, val_loss=0.026574
convlstm epoch 4/50: train_loss=0.024843, val_loss=0.024273
convlstm epoch 5/50: train_loss=0.023384, val_loss=0.023276
convlstm epoch 6/50: train_loss=0.022341, val_loss=0.022253
convlstm epoch 7/50: train_loss=0.021748, val_loss=0.022202
convlstm epoch 8/50: train_loss=0.021324, val_loss=0.022511
convlstm epoch 9/50: train_loss=0.020712, val_loss=0.020814
convlstm epoch 10/50: train_loss=0.020435, val_loss=0.020642
convlstm epoch 11/50: train_loss=0.020357, val_loss=0.020367
convlstm epoch 12/50: train_loss=0.020125, val_loss=0.020132
convlstm epoch 13/50: train_loss=0.020059, val_loss=0.019915
convlstm epoch 14/50: train_loss=0.019696, val_loss=0.020789
convlstm epoch 15/50: train_loss=0.019610, val_loss=0.022561
convlstm epoch 16/50: train_loss=0.019742, val_loss=0.020950
convlstm epoch 17/50: train_loss=0.019539, val_loss=0.019489
convlstm epoch 18/50: train_loss=0.019604, val_loss=0.019863
convlstm epoch 19/50: train_loss=0.019495, val_loss=0.019382
convlstm epoch 20/50: train_loss=0.019269, val_loss=0.021506
convlstm epoch 21/50: train_loss=0.019399, val_loss=0.019476
convlstm epoch 22/50: train_loss=0.019236, val_loss=0.020827
convlstm epoch 23/50: train_loss=0.019223, val_loss=0.019470
convlstm epoch 24/50: train_loss=0.019334, val_loss=0.019541
convlstm epoch 25/50: train_loss=0.019230, val_loss=0.019303
convlstm epoch 26/50: train_loss=0.019021, val_loss=0.019224
convlstm epoch 27/50: train_loss=0.019134, val_loss=0.019311
convlstm epoch 28/50: train_loss=0.019243, val_loss=0.019676
convlstm epoch 29/50: train_loss=0.018982, val_loss=0.019137
convlstm epoch 30/50: train_loss=0.018964, val_loss=0.019796
convlstm epoch 31/50: train_loss=0.018932, val_loss=0.019023
convlstm epoch 32/50: train_loss=0.018984, val_loss=0.019446
convlstm epoch 33/50: train_loss=0.019245, val_loss=0.018970
convlstm epoch 34/50: train_loss=0.019091, val_loss=0.020981
convlstm epoch 35/50: train_loss=0.019272, val_loss=0.019594
convlstm epoch 36/50: train_loss=0.018958, val_loss=0.020238
convlstm epoch 37/50: train_loss=0.018877, val_loss=0.020920
convlstm epoch 38/50: train_loss=0.018780, val_loss=0.019063
convlstm epoch 39/50: train_loss=0.018897, val_loss=0.018886
convlstm epoch 40/50: train_loss=0.018921, val_loss=0.019499
convlstm epoch 41/50: train_loss=0.018687, val_loss=0.019451
convlstm epoch 42/50: train_loss=0.018982, val_loss=0.019312
convlstm epoch 43/50: train_loss=0.018820, val_loss=0.019394
convlstm epoch 44/50: train_loss=0.018931, val_loss=0.018948
convlstm epoch 45/50: train_loss=0.018622, val_loss=0.019088
convlstm epoch 46/50: train_loss=0.018741, val_loss=0.018887
convlstm epoch 47/50: train_loss=0.018898, val_loss=0.019555
convlstm epoch 48/50: train_loss=0.018816, val_loss=0.019840
convlstm epoch 49/50: train_loss=0.018641, val_loss=0.019671
convlstm epoch 50/50: train_loss=0.018637, val_loss=0.019141
transformer epoch 1/50: train_loss=1.866607, val_loss=1.535643
transformer epoch 2/50: train_loss=1.349794, val_loss=1.123180
transformer epoch 3/50: train_loss=0.976011, val_loss=0.797689
transformer epoch 4/50: train_loss=0.683543, val_loss=0.549950
transformer epoch 5/50: train_loss=0.463412, val_loss=0.366266
transformer epoch 6/50: train_loss=0.302874, val_loss=0.234733
transformer epoch 7/50: train_loss=0.192285, val_loss=0.145554
transformer epoch 8/50: train_loss=0.119525, val_loss=0.089682
transformer epoch 9/50: train_loss=0.074762, val_loss=0.056469
transformer epoch 10/50: train_loss=0.048987, val_loss=0.038492
transformer epoch 11/50: train_loss=0.034711, val_loss=0.028598
transformer epoch 12/50: train_loss=0.027775, val_loss=0.023971
transformer epoch 13/50: train_loss=0.023961, val_loss=0.022220
transformer epoch 14/50: train_loss=0.022325, val_loss=0.021451
transformer epoch 15/50: train_loss=0.021770, val_loss=0.020984
transformer epoch 16/50: train_loss=0.021347, val_loss=0.020633
transformer epoch 17/50: train_loss=0.021013, val_loss=0.020685
transformer epoch 18/50: train_loss=0.020821, val_loss=0.021152
transformer epoch 19/50: train_loss=0.020857, val_loss=0.020569
transformer epoch 20/50: train_loss=0.020642, val_loss=0.020565
transformer epoch 21/50: train_loss=0.020663, val_loss=0.020733
transformer epoch 22/50: train_loss=0.020816, val_loss=0.020574
transformer epoch 23/50: train_loss=0.020605, val_loss=0.020578
transformer epoch 24/50: train_loss=0.020618, val_loss=0.020567
transformer epoch 25/50: train_loss=0.020619, val_loss=0.020703
transformer epoch 26/50: train_loss=0.020639, val_loss=0.020655
transformer epoch 27/50: train_loss=0.020458, val_loss=0.020566
transformer epoch 28/50: train_loss=0.020483, val_loss=0.020563
transformer epoch 29/50: train_loss=0.020388, val_loss=0.020564
transformer epoch 30/50: train_loss=0.020308, val_loss=0.020657
transformer epoch 31/50: train_loss=0.020344, val_loss=0.020958
transformer epoch 32/50: train_loss=0.020437, val_loss=0.020577
transformer epoch 33/50: train_loss=0.020417, val_loss=0.020601
transformer epoch 34/50: train_loss=0.020363, val_loss=0.020647
transformer epoch 35/50: train_loss=0.020327, val_loss=0.020563
transformer epoch 36/50: train_loss=0.020299, val_loss=0.020559
transformer epoch 37/50: train_loss=0.020322, val_loss=0.020860
transformer epoch 38/50: train_loss=0.020266, val_loss=0.020622
transformer epoch 39/50: train_loss=0.020234, val_loss=0.020589
transformer epoch 40/50: train_loss=0.020268, val_loss=0.020901
transformer epoch 41/50: train_loss=0.020253, val_loss=0.020625
transformer epoch 42/50: train_loss=0.020257, val_loss=0.020565
transformer epoch 43/50: train_loss=0.020376, val_loss=0.020585
transformer epoch 44/50: train_loss=0.020252, val_loss=0.020662
transformer epoch 45/50: train_loss=0.020249, val_loss=0.020617
transformer epoch 46/50: train_loss=0.020224, val_loss=0.020656
transformer epoch 47/50: train_loss=0.020293, val_loss=0.020589
transformer epoch 48/50: train_loss=0.020222, val_loss=0.020567
transformer epoch 49/50: train_loss=0.020280, val_loss=0.020714
transformer epoch 50/50: train_loss=0.020230, val_loss=0.020588
{
  "protocol": {
    "sequence_length": 7,
    "forecast_horizon_days": 1,
    "train_samples": 1819,
    "validation_samples": 359,
    "test_samples": 358,
    "spatial_shape": [
      121,
      141
    ],
    "device": "cuda:0",
    "seed": 42,
    "metric_space": "same denormalized stored temperature scale for every model",
    "normalization_unit": "degrees_Celsius",
    "normalization_mean_celsius": 25.044549020486595,
    "normalization_std_celsius": 10.99594436868629,
    "loss_threshold_celsius": 37.25411376953127,
    "loss_threshold_normalized": 1.1103698181499058,
    "loss_threshold_metadata": {
      "top_5_percent_celsius": 37.25411376953127,
      "bottom_5_percent_celsius": -1.7535766601562273,
      "quantile_method": "NumPy linear quantile (Hyndman-Fan Type 7)",
      "scope": "training split only; daily maximum t2m over all grid cells and days",
      "training_daily_records": 1826,
      "training_grid_values": 31153386,
      "training_date_range": [
        "2019-01-01",
        "2023-12-31"
      ],
      "input": "data/interim/train_daily.nc (t2m in K)",
      "loss_weight": 5.0
    },
    "pytorch_version": "2.5.1+cu121",
    "cuda_runtime": "12.1",
    "run_timestamp_utc": "2026-10-13T19:06:20.991062+00:00",
    "epochs_requested": 50,
    "output_directory": "C:\\Users\\25mdsml006\\Desktop\\deep_learning\\project\\climate\\climate2\\experiments\\reviewer_final_20261014"
  },
  "results": [
    {
      "model": "Persistence",
      "class": "last-input-day",
      "trainable_parameters": 0,
      "epochs": 0,
      "validation": {
        "rmse": 1.397688681160644,
        "mae": 0.89505535364151,
        "r2": 0.9830864667892456,
        "correlation": 0.991543251362402
      },
      "test": {
        "rmse": 1.402715734593257,
        "mae": 0.8974984288215637,
        "r2": 0.9818674921989441,
        "correlation": 0.9909366819576584
      }
    },
    {
      "model": "lstm",
      "class": "LSTMBaseline",
      "trainable_parameters": 4513,
      "epochs": 50,
      "epochs_requested": 50,
      "epochs_completed": 50,
      "batch_size": 16,
      "optimizer": "Adam",
      "learning_rate": 0.0001,
      "loss": "ExtremeWeightedMSE",
      "training_seconds": 333.543,
      "best_epoch": 50,
      "best_validation_loss": 0.025640719489234944,
      "history": [
        {
          "epoch": 1,
          "train_loss": 1.3573862633161378,
          "validation_loss": 1.2810013916181482
        },
        {
          "epoch": 2,
          "train_loss": 1.1235654207698085,
          "validation_loss": 0.9904481587202653
        },
        {
          "epoch": 3,
          "train_loss": 0.7869884078962761,
          "validation_loss": 0.5867152952629587
        },
        {
          "epoch": 4,
          "train_loss": 0.4248910874389766,
          "validation_loss": 0.2730327737720116
        },
        {
          "epoch": 5,
          "train_loss": 0.19815530595287942,
          "validation_loss": 0.1317222818084385
        },
        {
          "epoch": 6,
          "train_loss": 0.11756740422233154,
          "validation_loss": 0.09810127131640911
        },
        {
          "epoch": 7,
          "train_loss": 0.09634786171087048,
          "validation_loss": 0.08447729358854501
        },
        {
          "epoch": 8,
          "train_loss": 0.08332510926482971,
          "validation_loss": 0.07325802192739818
        },
        {
          "epoch": 9,
          "train_loss": 0.07242330807473576,
          "validation_loss": 0.06389544879936654
        },
        {
          "epoch": 10,
          "train_loss": 0.06343212965549085,
          "validation_loss": 0.05625007342061271
        },
        {
          "epoch": 11,
          "train_loss": 0.05624944912759881,
          "validation_loss": 0.05033021622701832
        },
        {
          "epoch": 12,
          "train_loss": 0.050685593858361244,
          "validation_loss": 0.04582751688102017
        },
        {
          "epoch": 13,
          "train_loss": 0.04646718305976767,
          "validation_loss": 0.04265177363286848
        },
        {
          "epoch": 14,
          "train_loss": 0.043333208384482486,
          "validation_loss": 0.04011938793827658
        },
        {
          "epoch": 15,
          "train_loss": 0.04105008939248428,
          "validation_loss": 0.038492569942837174
        },
        {
          "epoch": 16,
          "train_loss": 0.039341452547855545,
          "validation_loss": 0.03719357911335385
        },
        {
          "epoch": 17,
          "train_loss": 0.03813066150535617,
          "validation_loss": 0.03628097004864527
        },
        {
          "epoch": 18,
          "train_loss": 0.037228545288375596,
          "validation_loss": 0.03562312953821991
        },
        {
          "epoch": 19,
          "train_loss": 0.0364658597922116,
          "validation_loss": 0.03518758179700893
        },
        {
          "epoch": 20,
          "train_loss": 0.03584779867608296,
          "validation_loss": 0.034555943763774376
        },
        {
          "epoch": 21,
          "train_loss": 0.035295397206618076,
          "validation_loss": 0.034146895389194076
        },
        {
          "epoch": 22,
          "train_loss": 0.034787913343231926,
          "validation_loss": 0.033802687311949936
        },
        {
          "epoch": 23,
          "train_loss": 0.03435089623784287,
          "validation_loss": 0.0334777869284153
        },
        {
          "epoch": 24,
          "train_loss": 0.03390095230976218,
          "validation_loss": 0.03299561628828878
        },
        {
          "epoch": 25,
          "train_loss": 0.03351989788771199,
          "validation_loss": 0.032641092639254486
        },
        {
          "epoch": 26,
          "train_loss": 0.03305323104978653,
          "validation_loss": 0.03239994317941044
        },
        {
          "epoch": 27,
          "train_loss": 0.0326754158820238,
          "validation_loss": 0.031963165687478104
        },
        {
          "epoch": 28,
          "train_loss": 0.03228614979276532,
          "validation_loss": 0.03162463689627855
        },
        {
          "epoch": 29,
          "train_loss": 0.03194830375478456,
          "validation_loss": 0.031236252706983814
        },
        {
          "epoch": 30,
          "train_loss": 0.031586266939708015,
          "validation_loss": 0.030960848150045975
        },
        {
          "epoch": 31,
          "train_loss": 0.031238784980878495,
          "validation_loss": 0.030623995253573292
        },
        {
          "epoch": 32,
          "train_loss": 0.030840944253692503,
          "validation_loss": 0.030394736434454502
        },
        {
          "epoch": 33,
          "train_loss": 0.030509308241961294,
          "validation_loss": 0.02999131470594717
        },
        {
          "epoch": 34,
          "train_loss": 0.030256875300485837,
          "validation_loss": 0.029651185011734135
        },
        {
          "epoch": 35,
          "train_loss": 0.02991643949950996,
          "validation_loss": 0.029396660463965458
        },
        {
          "epoch": 36,
          "train_loss": 0.029590428708807417,
          "validation_loss": 0.029073076646613037
        },
        {
          "epoch": 37,
          "train_loss": 0.029331688556754797,
          "validation_loss": 0.028920856506928154
        },
        {
          "epoch": 38,
          "train_loss": 0.028999800597758668,
          "validation_loss": 0.028583017825756386
        },
        {
          "epoch": 39,
          "train_loss": 0.028711621110376558,
          "validation_loss": 0.028252729133743305
        },
        {
          "epoch": 40,
          "train_loss": 0.02848614621580693,
          "validation_loss": 0.0280041234648746
        },
        {
          "epoch": 41,
          "train_loss": 0.02817658405228142,
          "validation_loss": 0.02778115317873333
        },
        {
          "epoch": 42,
          "train_loss": 0.02792292124215971,
          "validation_loss": 0.027463336151255215
        },
        {
          "epoch": 43,
          "train_loss": 0.027615215874424105,
          "validation_loss": 0.0276318718071865
        },
        {
          "epoch": 44,
          "train_loss": 0.027408876766761143,
          "validation_loss": 0.027046561767549618
        },
        {
          "epoch": 45,
          "train_loss": 0.027161744504905584,
          "validation_loss": 0.026776119418766186
        },
        {
          "epoch": 46,
          "train_loss": 0.02685020952240417,
          "validation_loss": 0.026533450121464935
        },
        {
          "epoch": 47,
          "train_loss": 0.026603672555402705,
          "validation_loss": 0.02626471318628477
        },
        {
          "epoch": 48,
          "train_loss": 0.026362832357878226,
          "validation_loss": 0.026086067213960316
        },
        {
          "epoch": 49,
          "train_loss": 0.026149090248764606,
          "validation_loss": 0.025956788464732792
        },
        {
          "epoch": 50,
          "train_loss": 0.025864866725577598,
          "validation_loss": 0.025640719489234944
        }
      ],
      "validation": {
        "rmse": 1.5516975059818168,
        "mae": 1.0094974040985107,
        "r2": 0.9791538119316101,
        "correlation": 0.989547752322213
      },
      "test": {
        "rmse": 1.5727305607453141,
        "mae": 1.0160795450210571,
        "r2": 0.9772056341171265,
        "correlation": 0.9885678464754004
      },
      "checkpoint": "experiments\\reviewer_final_20261014\\lstm_best.pth",
      "history_file": "experiments\\reviewer_final_20261014\\lstm_history.json"
    },
    {
      "model": "cnn_lstm",
      "class": "CNNLSTMModel",
      "trainable_parameters": 18049,
      "epochs": 50,
      "epochs_requested": 50,
      "epochs_completed": 50,
      "batch_size": 16,
      "optimizer": "Adam",
      "learning_rate": 0.0001,
      "loss": "ExtremeWeightedMSE",
      "training_seconds": 161.667,
      "best_epoch": 48,
      "best_validation_loss": 0.02023503208613914,
      "history": [
        {
          "epoch": 1,
          "train_loss": 0.5723427753699454,
          "validation_loss": 0.13099228331576224
        },
        {
          "epoch": 2,
          "train_loss": 0.05630700545091378,
          "validation_loss": 0.03327804617583752
        },
        {
          "epoch": 3,
          "train_loss": 0.031012535095214844,
          "validation_loss": 0.030602534018133
        },
        {
          "epoch": 4,
          "train_loss": 0.02901240392473706,
          "validation_loss": 0.02905377069407183
        },
        {
          "epoch": 5,
          "train_loss": 0.027594700815123423,
          "validation_loss": 0.027915672156149925
        },
        {
          "epoch": 6,
          "train_loss": 0.026456254240321487,
          "validation_loss": 0.026742289733627567
        },
        {
          "epoch": 7,
          "train_loss": 0.025584488012419457,
          "validation_loss": 0.026044687620647575
        },
        {
          "epoch": 8,
          "train_loss": 0.024810088831081725,
          "validation_loss": 0.02505359847260558
        },
        {
          "epoch": 9,
          "train_loss": 0.02391722404577753,
          "validation_loss": 0.024207955631225006
        },
        {
          "epoch": 10,
          "train_loss": 0.023362214317577974,
          "validation_loss": 0.023763988248032074
        },
        {
          "epoch": 11,
          "train_loss": 0.02299425347397725,
          "validation_loss": 0.023449399589520435
        },
        {
          "epoch": 12,
          "train_loss": 0.022689735451549814,
          "validation_loss": 0.023273802807797558
        },
        {
          "epoch": 13,
          "train_loss": 0.02241518810848918,
          "validation_loss": 0.02321610040962696
        },
        {
          "epoch": 14,
          "train_loss": 0.022252515064585105,
          "validation_loss": 0.02285137574147919
        },
        {
          "epoch": 15,
          "train_loss": 0.022024831554868764,
          "validation_loss": 0.022443534037017304
        },
        {
          "epoch": 16,
          "train_loss": 0.0217600998615748,
          "validation_loss": 0.02216835486014252
        },
        {
          "epoch": 17,
          "train_loss": 0.02156924134479803,
          "validation_loss": 0.02203919726383427
        },
        {
          "epoch": 18,
          "train_loss": 0.021440959225098293,
          "validation_loss": 0.021916505475731
        },
        {
          "epoch": 19,
          "train_loss": 0.021359825621179322,
          "validation_loss": 0.02174806748719319
        },
        {
          "epoch": 20,
          "train_loss": 0.021248870324997,
          "validation_loss": 0.021662944117965904
        },
        {
          "epoch": 21,
          "train_loss": 0.021085180097112532,
          "validation_loss": 0.021707534668562206
        },
        {
          "epoch": 22,
          "train_loss": 0.02097636524163056,
          "validation_loss": 0.02138993354595226
        },
        {
          "epoch": 23,
          "train_loss": 0.02092806869104766,
          "validation_loss": 0.021583473998243393
        },
        {
          "epoch": 24,
          "train_loss": 0.020841561846042935,
          "validation_loss": 0.02146052107538866
        },
        {
          "epoch": 25,
          "train_loss": 0.020756458675717574,
          "validation_loss": 0.02112939816130244
        },
        {
          "epoch": 26,
          "train_loss": 0.0207095908556591,
          "validation_loss": 0.021131911072070183
        },
        {
          "epoch": 27,
          "train_loss": 0.02061212321808725,
          "validation_loss": 0.02101044899419598
        },
        {
          "epoch": 28,
          "train_loss": 0.02063596612169293,
          "validation_loss": 0.021028357234014118
        },
        {
          "epoch": 29,
          "train_loss": 0.020635700890827075,
          "validation_loss": 0.020984860177597275
        },
        {
          "epoch": 30,
          "train_loss": 0.02046228696902593,
          "validation_loss": 0.020824299558349278
        },
        {
          "epoch": 31,
          "train_loss": 0.020424222663502422,
          "validation_loss": 0.02078206582075876
        },
        {
          "epoch": 32,
          "train_loss": 0.020278200605197957,
          "validation_loss": 0.02084501848920532
        },
        {
          "epoch": 33,
          "train_loss": 0.02035563363154468,
          "validation_loss": 0.020781732326292473
        },
        {
          "epoch": 34,
          "train_loss": 0.020225064208110172,
          "validation_loss": 0.0206807399087626
        },
        {
          "epoch": 35,
          "train_loss": 0.02025632088056259,
          "validation_loss": 0.02069723314565161
        },
        {
          "epoch": 36,
          "train_loss": 0.0201579092740359,
          "validation_loss": 0.020594070787015167
        },
        {
          "epoch": 37,
          "train_loss": 0.020156067943102436,
          "validation_loss": 0.020480145457322182
        },
        {
          "epoch": 38,
          "train_loss": 0.02012228136555406,
          "validation_loss": 0.02079282891329216
        },
        {
          "epoch": 39,
          "train_loss": 0.020118379164813904,
          "validation_loss": 0.0206068253306591
        },
        {
          "epoch": 40,
          "train_loss": 0.02003158736777933,
          "validation_loss": 0.02051985389350549
        },
        {
          "epoch": 41,
          "train_loss": 0.020019358064848603,
          "validation_loss": 0.020339620340129604
        },
        {
          "epoch": 42,
          "train_loss": 0.019947966495365427,
          "validation_loss": 0.020330286260856235
        },
        {
          "epoch": 43,
          "train_loss": 0.019948017383157685,
          "validation_loss": 0.020298370322131592
        },
        {
          "epoch": 44,
          "train_loss": 0.019977847931154986,
          "validation_loss": 0.020265704466272957
        },
        {
          "epoch": 45,
          "train_loss": 0.019888263310126046,
          "validation_loss": 0.020265580843324246
        },
        {
          "epoch": 46,
          "train_loss": 0.01987794008955621,
          "validation_loss": 0.020291342238045258
        },
        {
          "epoch": 47,
          "train_loss": 0.019882795474442997,
          "validation_loss": 0.02034124987118918
        },
        {
          "epoch": 48,
          "train_loss": 0.019879045438740337,
          "validation_loss": 0.02023503208613914
        },
        {
          "epoch": 49,
          "train_loss": 0.019780549939656465,
          "validation_loss": 0.020444423122250515
        },
        {
          "epoch": 50,
          "train_loss": 0.01984852654532644,
          "validation_loss": 0.0203820845598112
        }
      ],
      "validation": {
        "rmse": 1.3995886385651402,
        "mae": 0.8996180891990662,
        "r2": 0.983040452003479,
        "correlation": 0.9914921169138822
      },
      "test": {
        "rmse": 1.4005166479889664,
        "mae": 0.8986677527427673,
        "r2": 0.981924295425415,
        "correlation": 0.9909284355087896
      },
      "checkpoint": "experiments\\reviewer_final_20261014\\cnn_lstm_best.pth",
      "history_file": "experiments\\reviewer_final_20261014\\cnn_lstm_history.json"
    },
    {
      "model": "convlstm",
      "class": "ConvLSTMModel",
      "trainable_parameters": 29441,
      "epochs": 50,
      "epochs_requested": 50,
      "epochs_completed": 50,
      "batch_size": 16,
      "optimizer": "Adam",
      "learning_rate": 0.0001,
      "loss": "ExtremeWeightedMSE",
      "training_seconds": 488.65,
      "best_epoch": 39,
      "best_validation_loss": 0.01888600012044544,
      "history": [
        {
          "epoch": 1,
          "train_loss": 0.1980280385663112,
          "validation_loss": 0.040255127312696495
        },
        {
          "epoch": 2,
          "train_loss": 0.035581574448498715,
          "validation_loss": 0.03181579717151497
        },
        {
          "epoch": 3,
          "train_loss": 0.028539653197584443,
          "validation_loss": 0.026574236462297646
        },
        {
          "epoch": 4,
          "train_loss": 0.02484323929080315,
          "validation_loss": 0.024273247174594715
        },
        {
          "epoch": 5,
          "train_loss": 0.023383570181434613,
          "validation_loss": 0.02327631531364244
        },
        {
          "epoch": 6,
          "train_loss": 0.022341064929047173,
          "validation_loss": 0.02225261801124915
        },
        {
          "epoch": 7,
          "train_loss": 0.02174811240024211,
          "validation_loss": 0.022202121174853783
        },
        {
          "epoch": 8,
          "train_loss": 0.021324329944164083,
          "validation_loss": 0.02251089906886868
        },
        {
          "epoch": 9,
          "train_loss": 0.020712237592721193,
          "validation_loss": 0.02081380784511566
        },
        {
          "epoch": 10,
          "train_loss": 0.02043547003382915,
          "validation_loss": 0.02064170461633931
        },
        {
          "epoch": 11,
          "train_loss": 0.020356556441504182,
          "validation_loss": 0.02036747866836579
        },
        {
          "epoch": 12,
          "train_loss": 0.02012502453535011,
          "validation_loss": 0.020131778376905815
        },
        {
          "epoch": 13,
          "train_loss": 0.02005946785701733,
          "validation_loss": 0.019915464455666748
        },
        {
          "epoch": 14,
          "train_loss": 0.019695984608117948,
          "validation_loss": 0.02078883208172477
        },
        {
          "epoch": 15,
          "train_loss": 0.01960957503730529,
          "validation_loss": 0.022561079255588676
        },
        {
          "epoch": 16,
          "train_loss": 0.019742007359143412,
          "validation_loss": 0.02095044626975837
        },
        {
          "epoch": 17,
          "train_loss": 0.019539149984586657,
          "validation_loss": 0.01948889381373706
        },
        {
          "epoch": 18,
          "train_loss": 0.019604027271270752,
          "validation_loss": 0.019862912473795208
        },
        {
          "epoch": 19,
          "train_loss": 0.01949519663232199,
          "validation_loss": 0.01938222964172778
        },
        {
          "epoch": 20,
          "train_loss": 0.01926912348554061,
          "validation_loss": 0.021506343482305176
        },
        {
          "epoch": 21,
          "train_loss": 0.01939853587955759,
          "validation_loss": 0.019475882427523964
        },
        {
          "epoch": 22,
          "train_loss": 0.019235782447810237,
          "validation_loss": 0.020826822632680767
        },
        {
          "epoch": 23,
          "train_loss": 0.01922317138431888,
          "validation_loss": 0.01947030595139317
        },
        {
          "epoch": 24,
          "train_loss": 0.019333572584416783,
          "validation_loss": 0.019540977016415283
        },
        {
          "epoch": 25,
          "train_loss": 0.01923033496234239,
          "validation_loss": 0.019303045276066532
        },
        {
          "epoch": 26,
          "train_loss": 0.01902112907223534,
          "validation_loss": 0.019224099247999813
        },
        {
          "epoch": 27,
          "train_loss": 0.019133806383858126,
          "validation_loss": 0.01931097103363794
        },
        {
          "epoch": 28,
          "train_loss": 0.019243190473501096,
          "validation_loss": 0.01967605786479038
        },
        {
          "epoch": 29,
          "train_loss": 0.018982422031592904,
          "validation_loss": 0.019136508602810944
        },
        {
          "epoch": 30,
          "train_loss": 0.018963741350984366,
          "validation_loss": 0.0197958723925378
        },
        {
          "epoch": 31,
          "train_loss": 0.01893165387343942,
          "validation_loss": 0.019022750425273956
        },
        {
          "epoch": 32,
          "train_loss": 0.018984498080323663,
          "validation_loss": 0.019445554393789043
        },
        {
          "epoch": 33,
          "train_loss": 0.019245049801834842,
          "validation_loss": 0.018969569557710834
        },
        {
          "epoch": 34,
          "train_loss": 0.01909097078207292,
          "validation_loss": 0.020981000817340355
        },
        {
          "epoch": 35,
          "train_loss": 0.01927183200033349,
          "validation_loss": 0.01959396910894176
        },
        {
          "epoch": 36,
          "train_loss": 0.01895767033688332,
          "validation_loss": 0.020238110471678818
        },
        {
          "epoch": 37,
          "train_loss": 0.01887689683619037,
          "validation_loss": 0.020920213230926056
        },
        {
          "epoch": 38,
          "train_loss": 0.018779771549529152,
          "validation_loss": 0.019063085317611694
        },
        {
          "epoch": 39,
          "train_loss": 0.01889677790173313,
          "validation_loss": 0.01888600012044544
        },
        {
          "epoch": 40,
          "train_loss": 0.01892075993186026,
          "validation_loss": 0.019499389252260975
        },
        {
          "epoch": 41,
          "train_loss": 0.01868718845377627,
          "validation_loss": 0.019451450030116932
        },
        {
          "epoch": 42,
          "train_loss": 0.018981531785245528,
          "validation_loss": 0.01931157246555971
        },
        {
          "epoch": 43,
          "train_loss": 0.018819847430118865,
          "validation_loss": 0.019394409356881744
        },
        {
          "epoch": 44,
          "train_loss": 0.0189305706227427,
          "validation_loss": 0.01894803381646457
        },
        {
          "epoch": 45,
          "train_loss": 0.018622078900143765,
          "validation_loss": 0.019087638867938
        },
        {
          "epoch": 46,
          "train_loss": 0.018740821335660785,
          "validation_loss": 0.018887199866382973
        },
        {
          "epoch": 47,
          "train_loss": 0.018898274765856433,
          "validation_loss": 0.019554608582478504
        },
        {
          "epoch": 48,
          "train_loss": 0.018815509533803714,
          "validation_loss": 0.019840001776490524
        },
        {
          "epoch": 49,
          "train_loss": 0.018640852639484302,
          "validation_loss": 0.01967142222692137
        },
        {
          "epoch": 50,
          "train_loss": 0.018636878212227634,
          "validation_loss": 0.019141475832008797
        }
      ],
      "validation": {
        "rmse": 1.3566575787135982,
        "mae": 0.8730589151382446,
        "r2": 0.9840649366378784,
        "correlation": 0.9920194329075844
      },
      "test": {
        "rmse": 1.3649147980337155,
        "mae": 0.8745298981666565,
        "r2": 0.982831597328186,
        "correlation": 0.991407401812537
      },
      "checkpoint": "experiments\\reviewer_final_20261014\\convlstm_best.pth",
      "history_file": "experiments\\reviewer_final_20261014\\convlstm_history.json"
    },
    {
      "model": "transformer",
      "class": "SpatioTemporalTransformer",
      "trainable_parameters": 275105,
      "epochs": 50,
      "epochs_requested": 50,
      "epochs_completed": 50,
      "batch_size": 16,
      "optimizer": "Adam",
      "learning_rate": 0.0001,
      "loss": "ExtremeWeightedMSE",
      "training_seconds": 70.617,
      "best_epoch": 36,
      "best_validation_loss": 0.020559415707121723,
      "history": [
        {
          "epoch": 1,
          "train_loss": 1.866606645416795,
          "validation_loss": 1.5356433287910793
        },
        {
          "epoch": 2,
          "train_loss": 1.3497942633796156,
          "validation_loss": 1.1231800343679346
        },
        {
          "epoch": 3,
          "train_loss": 0.9760113374183053,
          "validation_loss": 0.7976891229981962
        },
        {
          "epoch": 4,
          "train_loss": 0.6835434117860961,
          "validation_loss": 0.5499499148648718
        },
        {
          "epoch": 5,
          "train_loss": 0.46341222210934285,
          "validation_loss": 0.36626583013845526
        },
        {
          "epoch": 6,
          "train_loss": 0.3028738249027938,
          "validation_loss": 0.23473295731389004
        },
        {
          "epoch": 7,
          "train_loss": 0.19228492755638926,
          "validation_loss": 0.1455544847185197
        },
        {
          "epoch": 8,
          "train_loss": 0.11952540030082066,
          "validation_loss": 0.08968196210006009
        },
        {
          "epoch": 9,
          "train_loss": 0.07476166916782395,
          "validation_loss": 0.05646896313713944
        },
        {
          "epoch": 10,
          "train_loss": 0.048987057517495075,
          "validation_loss": 0.0384922644690327
        },
        {
          "epoch": 11,
          "train_loss": 0.034710816173046305,
          "validation_loss": 0.02859762902169124
        },
        {
          "epoch": 12,
          "train_loss": 0.027774511836469173,
          "validation_loss": 0.023970624593936878
        },
        {
          "epoch": 13,
          "train_loss": 0.023960894725301808,
          "validation_loss": 0.0222195569101883
        },
        {
          "epoch": 14,
          "train_loss": 0.022324719270201104,
          "validation_loss": 0.021450994293326916
        },
        {
          "epoch": 15,
          "train_loss": 0.02176981007582263,
          "validation_loss": 0.020984282150216724
        },
        {
          "epoch": 16,
          "train_loss": 0.021346989618777706,
          "validation_loss": 0.020633386448025703
        },
        {
          "epoch": 17,
          "train_loss": 0.021013497064510982,
          "validation_loss": 0.02068496823472821
        },
        {
          "epoch": 18,
          "train_loss": 0.02082147960665456,
          "validation_loss": 0.02115159615388383
        },
        {
          "epoch": 19,
          "train_loss": 0.020857072149387056,
          "validation_loss": 0.020568809107593868
        },
        {
          "epoch": 20,
          "train_loss": 0.020641764732110397,
          "validation_loss": 0.02056532357211994
        },
        {
          "epoch": 21,
          "train_loss": 0.020663413488747256,
          "validation_loss": 0.020732583194647148
        },
        {
          "epoch": 22,
          "train_loss": 0.0208160695946661,
          "validation_loss": 0.020574172472824222
        },
        {
          "epoch": 23,
          "train_loss": 0.020604562300273722,
          "validation_loss": 0.020578289525988308
        },
        {
          "epoch": 24,
          "train_loss": 0.020617599631741382,
          "validation_loss": 0.02056691176055566
        },
        {
          "epoch": 25,
          "train_loss": 0.02061882855272607,
          "validation_loss": 0.02070346612321294
        },
        {
          "epoch": 26,
          "train_loss": 0.02063885959388133,
          "validation_loss": 0.0206547775508269
        },
        {
          "epoch": 27,
          "train_loss": 0.020457535508301174,
          "validation_loss": 0.020565824623665085
        },
        {
          "epoch": 28,
          "train_loss": 0.020482966161676143,
          "validation_loss": 0.020562676631886025
        },
        {
          "epoch": 29,
          "train_loss": 0.02038758331419606,
          "validation_loss": 0.020563567502667076
        },
        {
          "epoch": 30,
          "train_loss": 0.020307967210547964,
          "validation_loss": 0.020657487497057602
        },
        {
          "epoch": 31,
          "train_loss": 0.020343822190178593,
          "validation_loss": 0.020958406040849892
        },
        {
          "epoch": 32,
          "train_loss": 0.02043691571605833,
          "validation_loss": 0.020576508229841358
        },
        {
          "epoch": 33,
          "train_loss": 0.020416500863798877,
          "validation_loss": 0.02060092216276604
        },
        {
          "epoch": 34,
          "train_loss": 0.020362642079003547,
          "validation_loss": 0.020646958773874718
        },
        {
          "epoch": 35,
          "train_loss": 0.020327278045251182,
          "validation_loss": 0.02056290808579196
        },
        {
          "epoch": 36,
          "train_loss": 0.020298935048151435,
          "validation_loss": 0.020559415707121723
        },
        {
          "epoch": 37,
          "train_loss": 0.020322272112887157,
          "validation_loss": 0.02086003675408985
        },
        {
          "epoch": 38,
          "train_loss": 0.02026594233323346,
          "validation_loss": 0.02062206670803868
        },
        {
          "epoch": 39,
          "train_loss": 0.02023364860858572,
          "validation_loss": 0.020589281480921352
        },
        {
          "epoch": 40,
          "train_loss": 0.020267580366252286,
          "validation_loss": 0.02090091043678315
        },
        {
          "epoch": 41,
          "train_loss": 0.020253381381432217,
          "validation_loss": 0.020624537749782852
        },
        {
          "epoch": 42,
          "train_loss": 0.020256711676586093,
          "validation_loss": 0.020564718009985012
        },
        {
          "epoch": 43,
          "train_loss": 0.02037639208464769,
          "validation_loss": 0.020585239500455235
        },
        {
          "epoch": 44,
          "train_loss": 0.020252421735214035,
          "validation_loss": 0.020662368275225163
        },
        {
          "epoch": 45,
          "train_loss": 0.020249303512013796,
          "validation_loss": 0.02061725950435452
        },
        {
          "epoch": 46,
          "train_loss": 0.020223845662385748,
          "validation_loss": 0.020655602378689724
        },
        {
          "epoch": 47,
          "train_loss": 0.020293155823948614,
          "validation_loss": 0.020588967301275417
        },
        {
          "epoch": 48,
          "train_loss": 0.020222248158237914,
          "validation_loss": 0.020567001531953396
        },
        {
          "epoch": 49,
          "train_loss": 0.020279774156382734,
          "validation_loss": 0.020713808136465756
        },
        {
          "epoch": 50,
          "train_loss": 0.020229730289429426,
          "validation_loss": 0.020587977183901745
        }
      ],
      "validation": {
        "rmse": 1.3979236788320364,
        "mae": 0.8956495523452759,
        "r2": 0.9830808043479919,
        "correlation": 0.9915440563852548
      },
      "test": {
        "rmse": 1.4030249171256943,
        "mae": 0.8987118005752563,
        "r2": 0.9818595051765442,
        "correlation": 0.9909356052009267
      },
      "checkpoint": "experiments\\reviewer_final_20261014\\transformer_best.pth",
      "history_file": "experiments\\reviewer_final_20261014\\transformer_history.json"
    }
  ]
}
Exit code: 0
```

## 2026-10-14 — Matched-date input-window ablation

Command: `.\.venv\Scripts\python.exe -u experiments\reviewer_final_20261014\run_window_ablation.py`

```text
.\.venv\Scripts\python.exe : Traceback (most recent call last):
At line:2 char:258
+ ... `n```text"; .\.venv\Scripts\python.exe -u experiments\reviewer_final_ ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError

  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\experiments\reviewer_final_20261014\run_wind
ow_ablation.py", line 9, in <module>
    from models.model_utils import get_model
ModuleNotFoundError: No module named 'models'
```

Exit code: 1

## 2026-10-14 — Matched-date input-window ablation retry

Command: `.\.venv\Scripts\python.exe -u experiments\reviewer_final_20261014\run_window_ablation.py`

```text



window=3 epoch=1/50 train=0.217829 val=0.038499
window=3 epoch=2/50 train=0.033130 val=0.029108
window=3 epoch=3/50 train=0.026753 val=0.025227
window=3 epoch=4/50 train=0.023984 val=0.023931
window=3 epoch=5/50 train=0.022727 val=0.022362
window=3 epoch=6/50 train=0.022031 val=0.021907
window=3 epoch=7/50 train=0.021278 val=0.021526
window=3 epoch=8/50 train=0.021002 val=0.021325
window=3 epoch=9/50 train=0.020739 val=0.020681
window=3 epoch=10/50 train=0.020726 val=0.020634
window=3 epoch=11/50 train=0.020306 val=0.020320
window=3 epoch=12/50 train=0.020013 val=0.020865
window=3 epoch=13/50 train=0.019936 val=0.020463
window=3 epoch=14/50 train=0.019929 val=0.020113
window=3 epoch=15/50 train=0.019797 val=0.019837
window=3 epoch=16/50 train=0.019472 val=0.019663
window=3 epoch=17/50 train=0.019531 val=0.019721
window=3 epoch=18/50 train=0.019509 val=0.020593
window=3 epoch=19/50 train=0.019515 val=0.019599
window=3 epoch=20/50 train=0.019528 val=0.019326
window=3 epoch=21/50 train=0.019304 val=0.019728
window=3 epoch=22/50 train=0.019234 val=0.019404
window=3 epoch=23/50 train=0.019640 val=0.019291
window=3 epoch=24/50 train=0.019108 val=0.019284
window=3 epoch=25/50 train=0.019105 val=0.019306
window=3 epoch=26/50 train=0.019240 val=0.019088
window=3 epoch=27/50 train=0.019130 val=0.019133
window=3 epoch=28/50 train=0.019267 val=0.019224
window=3 epoch=29/50 train=0.019044 val=0.019550
window=3 epoch=30/50 train=0.019097 val=0.019214
window=3 epoch=31/50 train=0.019185 val=0.019336
window=3 epoch=32/50 train=0.019016 val=0.019763
window=3 epoch=33/50 train=0.018841 val=0.019283
window=3 epoch=34/50 train=0.018877 val=0.019130
window=3 epoch=35/50 train=0.019075 val=0.019220
window=3 epoch=36/50 train=0.019051 val=0.019159
window=3 epoch=37/50 train=0.019305 val=0.019379
window=3 epoch=38/50 train=0.018943 val=0.018944
window=3 epoch=39/50 train=0.018822 val=0.019177
window=3 epoch=40/50 train=0.018962 val=0.019676
window=3 epoch=41/50 train=0.018953 val=0.018869
window=3 epoch=42/50 train=0.018883 val=0.019277
window=3 epoch=43/50 train=0.018925 val=0.019480
window=3 epoch=44/50 train=0.018850 val=0.019040
window=3 epoch=45/50 train=0.018817 val=0.019361
window=3 epoch=46/50 train=0.018827 val=0.018901
window=3 epoch=47/50 train=0.018830 val=0.019563
window=3 epoch=48/50 train=0.018743 val=0.018842
window=3 epoch=49/50 train=0.018994 val=0.018877
window=3 epoch=50/50 train=0.018683 val=0.019312
window=3 selected_epoch=48 common_test={'rmse_celsius': 1.3678377621439826, 'mae_celsius': 0.873910129070282, 'r2': 0.9824856519699097, 'pearson_r': 0.9912776328575975}
window=7 epoch=1/50 train=0.224356 val=0.040447
window=7 epoch=2/50 train=0.033638 val=0.030222
window=7 epoch=3/50 train=0.027292 val=0.025817
window=7 epoch=4/50 train=0.024218 val=0.023761
window=7 epoch=5/50 train=0.023059 val=0.023512
window=7 epoch=6/50 train=0.022054 val=0.022415
window=7 epoch=7/50 train=0.021362 val=0.021744
window=7 epoch=8/50 train=0.021069 val=0.021048
window=7 epoch=9/50 train=0.020589 val=0.020642
window=7 epoch=10/50 train=0.020495 val=0.020397
window=7 epoch=11/50 train=0.020117 val=0.020405
window=7 epoch=12/50 train=0.020179 val=0.019977
window=7 epoch=13/50 train=0.019828 val=0.019958
window=7 epoch=14/50 train=0.019700 val=0.019824
window=7 epoch=15/50 train=0.019590 val=0.019613
window=7 epoch=16/50 train=0.019439 val=0.020209
window=7 epoch=17/50 train=0.019518 val=0.020252
window=7 epoch=18/50 train=0.019352 val=0.020026
window=7 epoch=19/50 train=0.019310 val=0.020140
window=7 epoch=20/50 train=0.019208 val=0.020009
window=7 epoch=21/50 train=0.019284 val=0.019269
window=7 epoch=22/50 train=0.019439 val=0.019736
window=7 epoch=23/50 train=0.019353 val=0.019599
window=7 epoch=24/50 train=0.019122 val=0.019167
window=7 epoch=25/50 train=0.019134 val=0.020217
window=7 epoch=26/50 train=0.018923 val=0.019140
window=7 epoch=27/50 train=0.019263 val=0.019260
window=7 epoch=28/50 train=0.018816 val=0.019305
window=7 epoch=29/50 train=0.018920 val=0.019790
window=7 epoch=30/50 train=0.018838 val=0.019210
window=7 epoch=31/50 train=0.018975 val=0.019545
window=7 epoch=32/50 train=0.019005 val=0.019906
window=7 epoch=33/50 train=0.018926 val=0.019092
window=7 epoch=34/50 train=0.018803 val=0.019032
window=7 epoch=35/50 train=0.019078 val=0.019945
window=7 epoch=36/50 train=0.018935 val=0.018989


window=3 epoch=1/50 train=0.217829 val=0.038499
window=3 epoch=2/50 train=0.033130 val=0.029108
window=3 epoch=3/50 train=0.026753 val=0.025227
window=3 epoch=4/50 train=0.023984 val=0.023931
window=3 epoch=5/50 train=0.022727 val=0.022362
window=3 epoch=6/50 train=0.022031 val=0.021907
window=3 epoch=7/50 train=0.021278 val=0.021526
window=3 epoch=8/50 train=0.021002 val=0.021325
window=3 epoch=9/50 train=0.020739 val=0.020681
window=3 epoch=10/50 train=0.020726 val=0.020634
window=3 epoch=11/50 train=0.020306 val=0.020320
window=3 epoch=12/50 train=0.020013 val=0.020865
window=3 epoch=13/50 train=0.019936 val=0.020463
window=3 epoch=14/50 train=0.019929 val=0.020113
window=3 epoch=15/50 train=0.019797 val=0.019837
window=3 epoch=16/50 train=0.019472 val=0.019663
window=3 epoch=17/50 train=0.019531 val=0.019721
window=3 epoch=18/50 train=0.019509 val=0.020593
window=3 epoch=19/50 train=0.019515 val=0.019599
window=3 epoch=20/50 train=0.019528 val=0.019326
window=3 epoch=21/50 train=0.019304 val=0.019728
window=3 epoch=22/50 train=0.019234 val=0.019404
window=3 epoch=23/50 train=0.019640 val=0.019291
window=3 epoch=24/50 train=0.019108 val=0.019284
window=3 epoch=25/50 train=0.019105 val=0.019306
window=3 epoch=26/50 train=0.019240 val=0.019088
window=3 epoch=27/50 train=0.019130 val=0.019133
window=3 epoch=28/50 train=0.019267 val=0.019224
window=3 epoch=29/50 train=0.019044 val=0.019550
window=3 epoch=30/50 train=0.019097 val=0.019214
window=3 epoch=31/50 train=0.019185 val=0.019336
window=3 epoch=32/50 train=0.019016 val=0.019763
window=3 epoch=33/50 train=0.018841 val=0.019283
window=3 epoch=34/50 train=0.018877 val=0.019130
window=3 epoch=35/50 train=0.019075 val=0.019220
window=3 epoch=36/50 train=0.019051 val=0.019159
window=3 epoch=37/50 train=0.019305 val=0.019379
window=3 epoch=38/50 train=0.018943 val=0.018944
window=3 epoch=39/50 train=0.018822 val=0.019177
window=3 epoch=40/50 train=0.018962 val=0.019676
window=3 epoch=41/50 train=0.018953 val=0.018869
window=3 epoch=42/50 train=0.018883 val=0.019277
window=3 epoch=43/50 train=0.018925 val=0.019480
window=3 epoch=44/50 train=0.018850 val=0.019040
window=3 epoch=45/50 train=0.018817 val=0.019361
window=3 epoch=46/50 train=0.018827 val=0.018901
window=3 epoch=47/50 train=0.018830 val=0.019563
window=3 epoch=48/50 train=0.018743 val=0.018842
window=3 epoch=49/50 train=0.018994 val=0.018877
window=3 epoch=50/50 train=0.018683 val=0.019312
window=3 selected_epoch=48 common_test={'rmse_celsius': 1.3678377621439826, 'mae_celsius': 0.873910129070282, 'r2': 0.9824856519699097, 'pearson_r': 0.9912776328575975}
window=7 epoch=1/50 train=0.224356 val=0.040447
window=7 epoch=2/50 train=0.033638 val=0.030222
window=7 epoch=3/50 train=0.027292 val=0.025817
window=7 epoch=4/50 train=0.024218 val=0.023761
window=7 epoch=5/50 train=0.023059 val=0.023512
window=7 epoch=6/50 train=0.022054 val=0.022415
window=7 epoch=7/50 train=0.021362 val=0.021744
window=7 epoch=8/50 train=0.021069 val=0.021048
window=7 epoch=9/50 train=0.020589 val=0.020642
window=7 epoch=10/50 train=0.020495 val=0.020397
window=7 epoch=11/50 train=0.020117 val=0.020405
window=7 epoch=12/50 train=0.020179 val=0.019977
window=7 epoch=13/50 train=0.019828 val=0.019958
window=7 epoch=14/50 train=0.019700 val=0.019824
window=7 epoch=15/50 train=0.019590 val=0.019613
window=7 epoch=16/50 train=0.019439 val=0.020209
window=7 epoch=17/50 train=0.019518 val=0.020252
window=7 epoch=18/50 train=0.019352 val=0.020026
window=7 epoch=19/50 train=0.019310 val=0.020140
window=7 epoch=20/50 train=0.019208 val=0.020009
window=7 epoch=21/50 train=0.019284 val=0.019269
window=7 epoch=22/50 train=0.019439 val=0.019736
window=7 epoch=23/50 train=0.019353 val=0.019599
window=7 epoch=24/50 train=0.019122 val=0.019167
window=7 epoch=25/50 train=0.019134 val=0.020217
window=7 epoch=26/50 train=0.018923 val=0.019140
window=7 epoch=27/50 train=0.019263 val=0.019260
window=7 epoch=28/50 train=0.018816 val=0.019305
window=7 epoch=29/50 train=0.018920 val=0.019790
window=7 epoch=30/50 train=0.018838 val=0.019210
window=7 epoch=31/50 train=0.018975 val=0.019545
window=7 epoch=32/50 train=0.019005 val=0.019906
window=7 epoch=33/50 train=0.018926 val=0.019092
window=7 epoch=34/50 train=0.018803 val=0.019032
window=7 epoch=35/50 train=0.019078 val=0.019945
window=7 epoch=36/50 train=0.018935 val=0.018989


window=3 epoch=1/50 train=0.217829 val=0.038499
window=3 epoch=2/50 train=0.033130 val=0.029108
window=3 epoch=3/50 train=0.026753 val=0.025227
window=3 epoch=4/50 train=0.023984 val=0.023931
window=3 epoch=5/50 train=0.022727 val=0.022362
window=3 epoch=6/50 train=0.022031 val=0.021907
window=3 epoch=7/50 train=0.021278 val=0.021526
window=3 epoch=8/50 train=0.021002 val=0.021325
window=3 epoch=9/50 train=0.020739 val=0.020681
window=3 epoch=10/50 train=0.020726 val=0.020634
window=3 epoch=11/50 train=0.020306 val=0.020320
window=3 epoch=12/50 train=0.020013 val=0.020865
window=3 epoch=13/50 train=0.019936 val=0.020463
window=3 epoch=14/50 train=0.019929 val=0.020113
window=3 epoch=15/50 train=0.019797 val=0.019837
window=3 epoch=16/50 train=0.019472 val=0.019663
window=3 epoch=17/50 train=0.019531 val=0.019721
window=3 epoch=18/50 train=0.019509 val=0.020593
window=3 epoch=19/50 train=0.019515 val=0.019599
window=3 epoch=20/50 train=0.019528 val=0.019326
window=3 epoch=21/50 train=0.019304 val=0.019728
window=3 epoch=22/50 train=0.019234 val=0.019404
window=3 epoch=23/50 train=0.019640 val=0.019291
window=3 epoch=24/50 train=0.019108 val=0.019284
window=3 epoch=25/50 train=0.019105 val=0.019306
window=3 epoch=26/50 train=0.019240 val=0.019088
window=3 epoch=27/50 train=0.019130 val=0.019133
window=3 epoch=28/50 train=0.019267 val=0.019224
window=3 epoch=29/50 train=0.019044 val=0.019550
window=3 epoch=30/50 train=0.019097 val=0.019214
window=3 epoch=31/50 train=0.019185 val=0.019336
window=3 epoch=32/50 train=0.019016 val=0.019763
window=3 epoch=33/50 train=0.018841 val=0.019283
window=3 epoch=34/50 train=0.018877 val=0.019130
window=3 epoch=35/50 train=0.019075 val=0.019220
window=3 epoch=36/50 train=0.019051 val=0.019159
window=3 epoch=37/50 train=0.019305 val=0.019379
window=3 epoch=38/50 train=0.018943 val=0.018944
window=3 epoch=39/50 train=0.018822 val=0.019177
window=3 epoch=40/50 train=0.018962 val=0.019676
window=3 epoch=41/50 train=0.018953 val=0.018869
window=3 epoch=42/50 train=0.018883 val=0.019277
window=3 epoch=43/50 train=0.018925 val=0.019480
window=3 epoch=44/50 train=0.018850 val=0.019040
window=3 epoch=45/50 train=0.018817 val=0.019361
window=3 epoch=46/50 train=0.018827 val=0.018901
window=3 epoch=47/50 train=0.018830 val=0.019563
window=3 epoch=48/50 train=0.018743 val=0.018842
window=3 epoch=49/50 train=0.018994 val=0.018877
window=3 epoch=50/50 train=0.018683 val=0.019312
window=3 selected_epoch=48 common_test={'rmse_celsius': 1.3678377621439826, 'mae_celsius': 0.873910129070282, 'r2': 0.9824856519699097, 'pearson_r': 0.9912776328575975}
window=7 epoch=1/50 train=0.224356 val=0.040447
window=7 epoch=2/50 train=0.033638 val=0.030222
window=7 epoch=3/50 train=0.027292 val=0.025817
window=7 epoch=4/50 train=0.024218 val=0.023761
window=7 epoch=5/50 train=0.023059 val=0.023512
window=7 epoch=6/50 train=0.022054 val=0.022415
window=7 epoch=7/50 train=0.021362 val=0.021744
window=7 epoch=8/50 train=0.021069 val=0.021048
window=7 epoch=9/50 train=0.020589 val=0.020642
window=7 epoch=10/50 train=0.020495 val=0.020397
window=7 epoch=11/50 train=0.020117 val=0.020405
window=7 epoch=12/50 train=0.020179 val=0.019977
window=7 epoch=13/50 train=0.019828 val=0.019958
window=7 epoch=14/50 train=0.019700 val=0.019824
window=7 epoch=15/50 train=0.019590 val=0.019613
window=7 epoch=16/50 train=0.019439 val=0.020209
window=7 epoch=17/50 train=0.019518 val=0.020252
window=7 epoch=18/50 train=0.019352 val=0.020026
window=7 epoch=19/50 train=0.019310 val=0.020140
window=7 epoch=20/50 train=0.019208 val=0.020009
window=7 epoch=21/50 train=0.019284 val=0.019269
window=7 epoch=22/50 train=0.019439 val=0.019736
window=7 epoch=23/50 train=0.019353 val=0.019599
window=7 epoch=24/50 train=0.019122 val=0.019167
window=7 epoch=25/50 train=0.019134 val=0.020217
window=7 epoch=26/50 train=0.018923 val=0.019140
window=7 epoch=27/50 train=0.019263 val=0.019260
window=7 epoch=28/50 train=0.018816 val=0.019305
window=7 epoch=29/50 train=0.018920 val=0.019790
window=7 epoch=30/50 train=0.018838 val=0.019210
window=7 epoch=31/50 train=0.018975 val=0.019545
window=7 epoch=32/50 train=0.019005 val=0.019906
window=7 epoch=33/50 train=0.018926 val=0.019092
window=7 epoch=34/50 train=0.018803 val=0.019032
window=7 epoch=35/50 train=0.019078 val=0.019945
window=7 epoch=36/50 train=0.018935 val=0.018989
window=7 selected_epoch=41 common_test={'rmse_celsius': 1.3612863542450517, 'mae_celsius': 0.8726701736450195, 'r2': 0.982653021812439, 'pearson_r': 0.9913750861139368}
window=14 epoch=1/50 train=0.216120 val=0.039806
window=14 epoch=2/50 train=0.033356 val=0.029981
window=14 epoch=3/50 train=0.027335 val=0.026073
window=14 epoch=4/50 train=0.024503 val=0.024321
window=14 epoch=5/50 train=0.023077 val=0.023352
window=14 epoch=6/50 train=0.022351 val=0.022298
window=14 epoch=7/50 train=0.021573 val=0.021676
window=14 epoch=8/50 train=0.021265 val=0.021455
window=14 epoch=9/50 train=0.020954 val=0.021012
window=14 epoch=10/50 train=0.020642 val=0.021455
window=14 epoch=11/50 train=0.020352 val=0.020609
window=14 epoch=12/50 train=0.019930 val=0.020289
window=14 epoch=13/50 train=0.019803 val=0.020098
window=14 epoch=14/50 train=0.019632 val=0.019902
window=14 epoch=15/50 train=0.019653 val=0.020103
window=14 epoch=16/50 train=0.019585 val=0.019642
window=14 epoch=17/50 train=0.019503 val=0.019655
window=14 epoch=18/50 train=0.019193 val=0.020676
window=14 epoch=19/50 train=0.019222 val=0.019735
window=14 epoch=20/50 train=0.019405 val=0.019457
window=14 epoch=21/50 train=0.019226 val=0.019707
window=14 epoch=22/50 train=0.019121 val=0.019885
window=14 epoch=23/50 train=0.019535 val=0.019829
window=14 epoch=24/50 train=0.018975 val=0.019294
window=14 epoch=25/50 train=0.018885 val=0.019384
window=14 epoch=26/50 train=0.019210 val=0.019171
window=14 epoch=27/50 train=0.019035 val=0.019827
window=14 epoch=28/50 train=0.019093 val=0.019436
window=14 epoch=29/50 train=0.019131 val=0.019173
window=14 epoch=30/50 train=0.018823 val=0.019045
window=14 epoch=31/50 train=0.018771 val=0.019070
window=14 epoch=32/50 train=0.019086 val=0.020050
window=14 epoch=33/50 train=0.018894 val=0.019088
window=14 epoch=34/50 train=0.018883 val=0.020722
window=14 epoch=35/50 train=0.018855 val=0.019071
window=14 epoch=36/50 train=0.018855 val=0.019019
window=14 epoch=37/50 train=0.018656 val=0.018962
window=14 epoch=38/50 train=0.018968 val=0.019180
window=14 epoch=39/50 train=0.018755 val=0.019104
window=14 epoch=40/50 train=0.018697 val=0.018913
window=14 epoch=41/50 train=0.018609 val=0.019147
window=14 epoch=42/50 train=0.018805 val=0.018929
window=14 epoch=43/50 train=0.018598 val=0.018970
window=14 epoch=44/50 train=0.018678 val=0.019614
window=14 epoch=45/50 train=0.018737 val=0.019265
window=14 epoch=46/50 train=0.018628 val=0.018942
window=14 epoch=47/50 train=0.018529 val=0.019070
window=14 epoch=48/50 train=0.018681 val=0.020232
window=14 epoch=49/50 train=0.018887 val=0.019035
window=14 epoch=50/50 train=0.018622 val=0.018941
window=14 selected_epoch=40 common_test={'rmse_celsius': 1.3588287746893075, 'mae_celsius': 0.8683741092681885, 'r2': 0.9827155470848083, 'pearson_r': 0.9913939282383901}
ABLaTION_COMPLETE C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\experiments\reviewer_final_20261014\window_ablation
```

Exit code: 0

## 2026-10-14 — Selected-checkpoint seasonal and spatial analysis

Command: `.\.venv\Scripts\python.exe experiments\reviewer_final_20261014\analyze_final_errors.py`

```text
Normalization stats: mean=25.044549 C, std=10.995944 C
Model loaded from C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\experiments\reviewer_final_20261014\convlstm_best.pth

Evaluation test: 358 aligned samples
Target dates: 2025-01-08T00:00:00.000000000 to 2025-12-31T00:00:00.000000000
RMSE=1.364915 C; MAE=0.874530 C; R2=0.982832; Pearson r=0.991407
{
  "checkpoint": "experiments/reviewer_final_20261014/convlstm_best.pth",
  "aligned_test_dates": [
    "2025-01-08",
    "2025-12-31"
  ],
  "samples": 358,
  "seasonal": {
    "DJF": {
      "target_days": 83,
      "rmse_celsius": 1.3078193664550781,
      "mae_celsius": 0.8283376097679138
    },
    "MAM": {
      "target_days": 92,
      "rmse_celsius": 1.4941539764404297,
      "mae_celsius": 0.9718661904335022
    },
    "JJA": {
      "target_days": 92,
      "rmse_celsius": 1.3956328630447388,
      "mae_celsius": 0.9048813581466675
    },
    "SON": {
      "target_days": 91,
      "rmse_celsius": 1.242128610610962,
      "mae_celsius": 0.787570595741272
    }
  },
  "spatial_gridpoint_rmse": {
    "min": {
      "latitude": 14.75,
      "longitude": 67.5,
      "rmse_celsius": 0.2869308292865753
    },
    "mean": 1.1755183935165405,
    "max": {
      "latitude": 35.0,
      "longitude": 100.0,
      "rmse_celsius": 5.539139270782471
    }
  },
  "high_error_point_35N_65E": {
    "coordinate_latitude": 35.0,
    "coordinate_longitude": 65.0,
    "hourly_records": 8760,
    "hourly_finite": true,
    "daily_records_checked": 365,
    "hourly_24h_max_matches_daily_max": true,
    "max_abs_difference_K": 0.0,
    "forecast_samples": 358,
    "forecast_target_dates": [
      "2025-01-08",
      "2025-12-31"
    ],
    "last_input_day_matches_daily_series_max_abs_difference_C": 1.9073486328125e-06,
    "targets_match_daily_series_max_abs_difference_C": 1.9073486328125e-06,
    "largest_abs_error": {
      "target_date": "2025-02-11",
      "previous_input_date": "2025-02-10",
      "previous_input_tmax_C": -1.920654296875,
      "observed_target_tmax_C": -10.193449020385742,
      "predicted_tmax_C": 4.100568771362305,
      "absolute_error_C": 14.294017791748047
    },
    "conv3d_selected_checkpoint": "experiments/reviewer_final_20261014/convlstm_best.pth"
  }
}
```

Exit code: 0

## 2026-10-14 ? Validation evaluator cross-check

Command: `.\.venv\Scripts\python.exe experiments\reviewer_final_20261014\val_crosscheck.py`

```text
Evaluation val: 359 aligned samples
Target dates: 2024-01-08 through 2024-12-31
RMSE=1.356658 C; MAE=0.873059 C; R2=0.984065; Pearson r=0.992019
Evaluator target alignment verified against daily targets.
```

Exit code: 0. A first temporary-script attempt exited 1 because the script ran outside the project import path; it failed before evaluation. The project-root script retry above succeeded.

## 2026-10-14 ? Final syntax check

Command: `.\.venv\Scripts\python.exe -m py_compile evaluate_model.py preprocessing\compute_extremes.py training\losses.py run_baseline_experiments.py experiments\reviewer_final_20261014\run_window_ablation.py experiments\reviewer_final_20261014\analyze_final_errors.py`

```text
All listed Python files compiled successfully.
```

Exit code: 0. The corrected completed ablation artifacts are preserved under `experiments/reviewer_final_20261014/window_ablation_final/`; the pre-existing tracked one-epoch artifacts in `window_ablation/` were restored to their original blob contents.

import numpy as np
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
import json
p='data/processed/tensors/test_X.npy'; y='data/processed/tensors/test_y.npy'
X=np.load(p,mmap_mode='r');Y=np.load(y,mmap_mode='r');s=json.load(open('data/processed/mean_std.json'));m=float(s['mean']);d=float(s['std'])
pred=np.asarray(X[7:,-1,0])*d+m;target=np.asarray(Y[7:,0])*d+m
print('matched_dates=351; 2025-01-15 through 2025-12-31')
print('persistence_rmse_celsius',float(np.sqrt(mean_squared_error(target.ravel(),pred.ravel()))))
print('persistence_mae_celsius',float(mean_absolute_error(target.ravel(),pred.ravel())))
print('persistence_r2',float(r2_score(target.ravel(),pred.ravel())))
print('persistence_pearson_r',float(np.corrcoef(pred.ravel(),target.ravel())[0,1]))
'@ | .\.venv\Scripts\python.exe -


matched_dates=351; 2025-01-15 through 2025-12-31
persistence_rmse_celsius 1.3958533935623685
persistence_mae_celsius 0.8927555084228516
persistence_r2 0.9817607998847961
persistence_pearson_r 0.9908822105711548
## 2026-10-14 — Selected checkpoint metric recheck

Command: `.\.venv\Scripts\python.exe experiments\reviewer_final_20261014\verify_selected_checkpoints.py`

```text
.\.venv\Scripts\python.exe : Traceback (most recent call last):
At line:2 char:61
+ ... check.log'; .\.venv\Scripts\python.exe experiments\reviewer_final_202 ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError

  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\experiments\reviewer_final_20261014\verify_s
elected_checkpoints.py", line 40, in <module>
    if __name__=='__main__':main()
                            ^^^^^^
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\experiments\reviewer_final_20261014\verify_s
elected_checkpoints.py", line 33, in main
    measured=score(np.concatenate(ps),np.concatenate(ys)); expected=entry[split]
                                                                    ~~~~~^^^^^^^
KeyError: 'val'
```

Exit code: 1

## 2026-10-14 — Selected checkpoint metric recheck retry

Command: `.\.venv\Scripts\python.exe experiments\reviewer_final_20261014\verify_selected_checkpoints.py`

```text
.\.venv\Scripts\python.exe : Traceback (most recent call last):
At line:2 char:67
+ ... retry.log'; .\.venv\Scripts\python.exe experiments\reviewer_final_202 ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError

  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\experiments\reviewer_final_20261014\verify_s
elected_checkpoints.py", line 40, in <module>
    if __name__=='__main__':main()
                            ^^^^^^
  File "C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2\experiments\reviewer_final_20261014\verify_s
elected_checkpoints.py", line 35, in main
    if max(delta.values())>1e-5:raise AssertionError(f'{name} {split} checkpoint mismatch: deltas={delta}')
                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: lstm val checkpoint mismatch: deltas={'rmse': 1.5354942819836075, 'mae': 0.9993448257446289, 'r2':
0.06167018413543701, 'correlation': 0.029169751337848382}
```

Exit code: 1

## 2026-10-14 — Checkpoint to aggregate recheck (collected all model discrepancies)

Command: `.\.venv\Scripts\python.exe experiments\reviewer_final_20261014\verify_selected_checkpoints.py`

```text
lstm {'val': {'metrics': {'rmse': 3.0871917879654243, 'mae': 2.0088422298431396, 'r2': 0.9174836277961731, 'correlation': 0.9603780009843647}, 'max_abs_metric_delta': 1.5354942819836075, 'matches_aggregate': False, 'samples': 359}, 'test': {'metrics': {'rmse': 2.9620641009434863, 'mae': 1.906995415687561, 'r2': 0.919144868850708, 'correlation': 0.9611562816154705}, 'max_abs_metric_delta': 1.3893335401981721, 'matches_aggregate': False, 'samples': 358}}
cnn_lstm {'val': {'metrics': {'rmse': 1.3995886385651402, 'mae': 0.8996180891990662, 'r2': 0.983040452003479, 'correlation': 0.9914921169138822}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 359}, 'test': {'metrics': {'rmse': 1.4005166479889664, 'mae': 0.8986677527427673, 'r2': 0.981924295425415, 'correlation': 0.9909284355087896}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 358}}
convlstm {'val': {'metrics': {'rmse': 1.3566575787135982, 'mae': 0.8730589151382446, 'r2': 0.9840649366378784, 'correlation': 0.9920194329075844}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 359}, 'test': {'metrics': {'rmse': 1.3649147980337155, 'mae': 0.8745298981666565, 'r2': 0.982831597328186, 'correlation': 0.991407401812537}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 358}}
transformer {'val': {'metrics': {'rmse': 1.3979236788320364, 'mae': 0.8956495523452759, 'r2': 0.9830808043479919, 'correlation': 0.9915440563852548}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 359}, 'test': {'metrics': {'rmse': 1.4030249171256943, 'mae': 0.8987118005752563, 'r2': 0.9818595051765442, 'correlation': 0.9909356052009267}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 358}}
ALL_SELECTED_CHECKPOINTS_MATCH False
```

Exit code: 0

## 2026-10-14 — LSTM checkpoint and history repair run

Command: `.\.venv\Scripts\python.exe -u run_baseline_experiments.py --epochs 50 --batch-size 16 --seed 42 --device cuda --models lstm --output-dir experiments\reviewer_lstm_repaired_20261014`

```text
Selected device: cuda:0
GPU: NVIDIA GeForce RTX 4070; PyTorch 2.5.1+cu121; CUDA runtime 12.1
lstm epoch 1/50: train_loss=1.357386, val_loss=1.281001
lstm epoch 2/50: train_loss=1.123565, val_loss=0.990448
lstm epoch 3/50: train_loss=0.786988, val_loss=0.586715
lstm epoch 4/50: train_loss=0.424891, val_loss=0.273033
lstm epoch 5/50: train_loss=0.198155, val_loss=0.131722
lstm epoch 6/50: train_loss=0.117567, val_loss=0.098101
lstm epoch 7/50: train_loss=0.096348, val_loss=0.084477
lstm epoch 8/50: train_loss=0.083325, val_loss=0.073258
lstm epoch 9/50: train_loss=0.072423, val_loss=0.063895
lstm epoch 10/50: train_loss=0.063432, val_loss=0.056250
lstm epoch 11/50: train_loss=0.056249, val_loss=0.050330
lstm epoch 12/50: train_loss=0.050686, val_loss=0.045828
lstm epoch 13/50: train_loss=0.046467, val_loss=0.042652
lstm epoch 14/50: train_loss=0.043333, val_loss=0.040119
lstm epoch 15/50: train_loss=0.041050, val_loss=0.038493
lstm epoch 16/50: train_loss=0.039341, val_loss=0.037194
lstm epoch 17/50: train_loss=0.038131, val_loss=0.036281
lstm epoch 18/50: train_loss=0.037229, val_loss=0.035623
lstm epoch 19/50: train_loss=0.036466, val_loss=0.035188
lstm epoch 20/50: train_loss=0.035848, val_loss=0.034556
lstm epoch 21/50: train_loss=0.035295, val_loss=0.034147
lstm epoch 22/50: train_loss=0.034788, val_loss=0.033803
lstm epoch 23/50: train_loss=0.034351, val_loss=0.033478
lstm epoch 24/50: train_loss=0.033901, val_loss=0.032996
lstm epoch 25/50: train_loss=0.033520, val_loss=0.032641
lstm epoch 26/50: train_loss=0.033053, val_loss=0.032400
lstm epoch 27/50: train_loss=0.032675, val_loss=0.031963
lstm epoch 28/50: train_loss=0.032286, val_loss=0.031625
lstm epoch 29/50: train_loss=0.031948, val_loss=0.031236
lstm epoch 30/50: train_loss=0.031586, val_loss=0.030961
lstm epoch 31/50: train_loss=0.031239, val_loss=0.030624
lstm epoch 32/50: train_loss=0.030841, val_loss=0.030395
lstm epoch 33/50: train_loss=0.030509, val_loss=0.029991
lstm epoch 34/50: train_loss=0.030257, val_loss=0.029651
lstm epoch 35/50: train_loss=0.029916, val_loss=0.029397
lstm epoch 36/50: train_loss=0.029590, val_loss=0.029073
lstm epoch 37/50: train_loss=0.029332, val_loss=0.028921
lstm epoch 38/50: train_loss=0.029000, val_loss=0.028583
lstm epoch 39/50: train_loss=0.028712, val_loss=0.028253
lstm epoch 40/50: train_loss=0.028486, val_loss=0.028004
lstm epoch 41/50: train_loss=0.028177, val_loss=0.027781
lstm epoch 42/50: train_loss=0.027923, val_loss=0.027463
lstm epoch 43/50: train_loss=0.027615, val_loss=0.027632
lstm epoch 44/50: train_loss=0.027409, val_loss=0.027047
lstm epoch 45/50: train_loss=0.027162, val_loss=0.026776
lstm epoch 46/50: train_loss=0.026850, val_loss=0.026533
lstm epoch 47/50: train_loss=0.026604, val_loss=0.026265
lstm epoch 48/50: train_loss=0.026363, val_loss=0.026086
lstm epoch 49/50: train_loss=0.026149, val_loss=0.025957
lstm epoch 50/50: train_loss=0.025865, val_loss=0.025641
{
  "protocol": {
    "sequence_length": 7,
    "forecast_horizon_days": 1,
    "train_samples": 1819,
    "validation_samples": 359,
    "test_samples": 358,
    "spatial_shape": [
      121,
      141
    ],
    "device": "cuda:0",
    "seed": 42,
    "metric_space": "same denormalized stored temperature scale for every model",
    "normalization_unit": "degrees_Celsius",
    "normalization_mean_celsius": 25.044549020486595,
    "normalization_std_celsius": 10.99594436868629,
    "loss_threshold_celsius": 37.25411376953127,
    "loss_threshold_normalized": 1.1103698181499058,
    "loss_threshold_metadata": {
      "top_5_percent_celsius": 37.25411376953127,
      "bottom_5_percent_celsius": -1.7535766601562273,
      "quantile_method": "NumPy linear quantile (Hyndman-Fan Type 7)",
      "scope": "training split only; daily maximum t2m over all grid cells and days",
      "training_daily_records": 1826,
      "training_grid_values": 31153386,
      "training_date_range": [
        "2019-01-01",
        "2023-12-31"
      ],
      "input": "data/interim/train_daily.nc (t2m in K)",
      "loss_weight": 5.0
    },
    "pytorch_version": "2.5.1+cu121",
    "cuda_runtime": "12.1",
    "run_timestamp_utc": "2026-10-13T19:48:17.096197+00:00",
    "epochs_requested": 50,
    "output_directory": "C:\\Users\\25mdsml006\\Desktop\\deep_learning\\project\\climate\\climate2\\experiments\\reviewer_lstm_repaired_20261014"
  },
  "results": [
    {
      "model": "lstm",
      "class": "LSTMBaseline",
      "trainable_parameters": 4513,
      "epochs": 50,
      "epochs_requested": 50,
      "epochs_completed": 50,
      "batch_size": 16,
      "optimizer": "Adam",
      "learning_rate": 0.0001,
      "loss": "ExtremeWeightedMSE",
      "training_seconds": 331.793,
      "best_epoch": 50,
      "best_validation_loss": 0.025640719489234944,
      "history": [
        {
          "epoch": 1,
          "train_loss": 1.3573862633161378,
          "validation_loss": 1.2810013916181482
        },
        {
          "epoch": 2,
          "train_loss": 1.1235654207698085,
          "validation_loss": 0.9904481587202653
        },
        {
          "epoch": 3,
          "train_loss": 0.7869884078962761,
          "validation_loss": 0.5867152952629587
        },
        {
          "epoch": 4,
          "train_loss": 0.4248910874389766,
          "validation_loss": 0.2730327737720116
        },
        {
          "epoch": 5,
          "train_loss": 0.19815530595287942,
          "validation_loss": 0.1317222818084385
        },
        {
          "epoch": 6,
          "train_loss": 0.11756740422233154,
          "validation_loss": 0.09810127131640911
        },
        {
          "epoch": 7,
          "train_loss": 0.09634786171087048,
          "validation_loss": 0.08447729358854501
        },
        {
          "epoch": 8,
          "train_loss": 0.08332510926482971,
          "validation_loss": 0.07325802192739818
        },
        {
          "epoch": 9,
          "train_loss": 0.07242330807473576,
          "validation_loss": 0.06389544879936654
        },
        {
          "epoch": 10,
          "train_loss": 0.06343212965549085,
          "validation_loss": 0.05625007342061271
        },
        {
          "epoch": 11,
          "train_loss": 0.05624944912759881,
          "validation_loss": 0.05033021622701832
        },
        {
          "epoch": 12,
          "train_loss": 0.050685593858361244,
          "validation_loss": 0.04582751688102017
        },
        {
          "epoch": 13,
          "train_loss": 0.04646718305976767,
          "validation_loss": 0.04265177363286848
        },
        {
          "epoch": 14,
          "train_loss": 0.043333208384482486,
          "validation_loss": 0.04011938793827658
        },
        {
          "epoch": 15,
          "train_loss": 0.04105008939248428,
          "validation_loss": 0.038492569942837174
        },
        {
          "epoch": 16,
          "train_loss": 0.039341452547855545,
          "validation_loss": 0.03719357911335385
        },
        {
          "epoch": 17,
          "train_loss": 0.03813066150535617,
          "validation_loss": 0.03628097004864527
        },
        {
          "epoch": 18,
          "train_loss": 0.037228545288375596,
          "validation_loss": 0.03562312953821991
        },
        {
          "epoch": 19,
          "train_loss": 0.0364658597922116,
          "validation_loss": 0.03518758179700893
        },
        {
          "epoch": 20,
          "train_loss": 0.03584779867608296,
          "validation_loss": 0.034555943763774376
        },
        {
          "epoch": 21,
          "train_loss": 0.035295397206618076,
          "validation_loss": 0.034146895389194076
        },
        {
          "epoch": 22,
          "train_loss": 0.034787913343231926,
          "validation_loss": 0.033802687311949936
        },
        {
          "epoch": 23,
          "train_loss": 0.03435089623784287,
          "validation_loss": 0.0334777869284153
        },
        {
          "epoch": 24,
          "train_loss": 0.03390095230976218,
          "validation_loss": 0.03299561628828878
        },
        {
          "epoch": 25,
          "train_loss": 0.03351989788771199,
          "validation_loss": 0.032641092639254486
        },
        {
          "epoch": 26,
          "train_loss": 0.03305323104978653,
          "validation_loss": 0.03239994317941044
        },
        {
          "epoch": 27,
          "train_loss": 0.0326754158820238,
          "validation_loss": 0.031963165687478104
        },
        {
          "epoch": 28,
          "train_loss": 0.03228614979276532,
          "validation_loss": 0.03162463689627855
        },
        {
          "epoch": 29,
          "train_loss": 0.03194830375478456,
          "validation_loss": 0.031236252706983814
        },
        {
          "epoch": 30,
          "train_loss": 0.031586266939708015,
          "validation_loss": 0.030960848150045975
        },
        {
          "epoch": 31,
          "train_loss": 0.031238784980878495,
          "validation_loss": 0.030623995253573292
        },
        {
          "epoch": 32,
          "train_loss": 0.030840944253692503,
          "validation_loss": 0.030394736434454502
        },
        {
          "epoch": 33,
          "train_loss": 0.030509308241961294,
          "validation_loss": 0.02999131470594717
        },
        {
          "epoch": 34,
          "train_loss": 0.030256875300485837,
          "validation_loss": 0.029651185011734135
        },
        {
          "epoch": 35,
          "train_loss": 0.02991643949950996,
          "validation_loss": 0.029396660463965458
        },
        {
          "epoch": 36,
          "train_loss": 0.029590428708807417,
          "validation_loss": 0.029073076646613037
        },
        {
          "epoch": 37,
          "train_loss": 0.029331688556754797,
          "validation_loss": 0.028920856506928154
        },
        {
          "epoch": 38,
          "train_loss": 0.028999800597758668,
          "validation_loss": 0.028583017825756386
        },
        {
          "epoch": 39,
          "train_loss": 0.028711621110376558,
          "validation_loss": 0.028252729133743305
        },
        {
          "epoch": 40,
          "train_loss": 0.02848614621580693,
          "validation_loss": 0.0280041234648746
        },
        {
          "epoch": 41,
          "train_loss": 0.02817658405228142,
          "validation_loss": 0.02778115317873333
        },
        {
          "epoch": 42,
          "train_loss": 0.02792292124215971,
          "validation_loss": 0.027463336151255215
        },
        {
          "epoch": 43,
          "train_loss": 0.027615215874424105,
          "validation_loss": 0.0276318718071865
        },
        {
          "epoch": 44,
          "train_loss": 0.027408876766761143,
          "validation_loss": 0.027046561767549618
        },
        {
          "epoch": 45,
          "train_loss": 0.027161744504905584,
          "validation_loss": 0.026776119418766186
        },
        {
          "epoch": 46,
          "train_loss": 0.02685020952240417,
          "validation_loss": 0.026533450121464935
        },
        {
          "epoch": 47,
          "train_loss": 0.026603672555402705,
          "validation_loss": 0.02626471318628477
        },
        {
          "epoch": 48,
          "train_loss": 0.026362832357878226,
          "validation_loss": 0.026086067213960316
        },
        {
          "epoch": 49,
          "train_loss": 0.026149090248764606,
          "validation_loss": 0.025956788464732792
        },
        {
          "epoch": 50,
          "train_loss": 0.025864866725577598,
          "validation_loss": 0.025640719489234944
        }
      ],
      "validation": {
        "rmse": 1.5516975059818168,
        "mae": 1.0094974040985107,
        "r2": 0.9791538119316101,
        "correlation": 0.989547752322213
      },
      "test": {
        "rmse": 1.5727305607453141,
        "mae": 1.0160795450210571,
        "r2": 0.9772056341171265,
        "correlation": 0.9885678464754004
      },
      "checkpoint": "experiments\\reviewer_lstm_repaired_20261014\\lstm_best.pth",
      "history_file": "experiments\\reviewer_lstm_repaired_20261014\\lstm_history.json"
    }
  ]
}
```

Exit code: 0

## 2026-10-14 — Final selected-checkpoint verification

Command: `.\.venv\Scripts\python.exe experiments\reviewer_final_20261014\verify_selected_checkpoints.py`

```text
lstm {'val': {'metrics': {'rmse': 1.5516975059818168, 'mae': 1.0094974040985107, 'r2': 0.9791538119316101, 'correlation': 0.989547752322213}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 359}, 'test': {'metrics': {'rmse': 1.5727305607453141, 'mae': 1.0160795450210571, 'r2': 0.9772056341171265, 'correlation': 0.9885678464754004}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 358}}
cnn_lstm {'val': {'metrics': {'rmse': 1.3995886385651402, 'mae': 0.8996180891990662, 'r2': 0.983040452003479, 'correlation': 0.9914921169138822}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 359}, 'test': {'metrics': {'rmse': 1.4005166479889664, 'mae': 0.8986677527427673, 'r2': 0.981924295425415, 'correlation': 0.9909284355087896}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 358}}
convlstm {'val': {'metrics': {'rmse': 1.3566575787135982, 'mae': 0.8730589151382446, 'r2': 0.9840649366378784, 'correlation': 0.9920194329075844}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 359}, 'test': {'metrics': {'rmse': 1.3649147980337155, 'mae': 0.8745298981666565, 'r2': 0.982831597328186, 'correlation': 0.991407401812537}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 358}}
transformer {'val': {'metrics': {'rmse': 1.3979236788320364, 'mae': 0.8956495523452759, 'r2': 0.9830808043479919, 'correlation': 0.9915440563852548}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 359}, 'test': {'metrics': {'rmse': 1.4030249171256943, 'mae': 0.8987118005752563, 'r2': 0.9818595051765442, 'correlation': 0.9909356052009267}, 'max_abs_metric_delta': 0.0, 'matches_aggregate': True, 'samples': 358}}
ALL_SELECTED_CHECKPOINTS_MATCH True
```

Exit code: 0


## 2026-10-14: Documentation synchronization

Commands: inspected `README.md`, `reviewer_questions_answers.md`, `terminal_outputs.md`, and the final experiment JSON artifacts; updated documentation only.

Files updated: `README.md`, `reviewer_questions_answers.md`; created `changes.md`. Existing terminal log content was retained and this record appended.

Verification: values in the README and change log were copied from `experiments/reviewer_final_20261014/comparison_results.json`, `experiments/reviewer_final_20261014/window_ablation_final/window_ablation_results.json`, `experiments/reviewer_final_20261014/error_analysis.json`, and `experiments/reviewer_final_20261014/high_error_point_35N_65E.json`. No training or data rebuild was run. Exact validation/test source equality remains unverified.

Documentation integrity check: UTF-8 decode passed for all edited Markdown files; code fences balanced in README/reviewer answers/log/data guide/change log; removed duplicate CNN-LSTM heading; no source, revision, checkpoint, or prior experiment artifact modified.

Exit code: 0


elected device: cuda:0
GPU: NVIDIA GeForce RTX 4070; PyTorch 2.5.1+cu121; CUDA runtime 12.1
recurrent_convlstm epoch 1/50: train_loss=0.837803, val_loss=0.224333
recurrent_convlstm epoch 2/50: train_loss=0.143002, val_loss=0.090828
recurrent_convlstm epoch 3/50: train_loss=0.084547, val_loss=0.068658
recurrent_convlstm epoch 4/50: train_loss=0.067915, val_loss=0.058402
recurrent_convlstm epoch 5/50: train_loss=0.057551, val_loss=0.050908
recurrent_convlstm epoch 6/50: train_loss=0.051252, val_loss=0.046784
recurrent_convlstm epoch 7/50: train_loss=0.047317, val_loss=0.044243
recurrent_convlstm epoch 8/50: train_loss=0.044244, val_loss=0.041075
recurrent_convlstm epoch 9/50: train_loss=0.041954, val_loss=0.039084
recurrent_convlstm epoch 10/50: train_loss=0.040258, val_loss=0.037605
recurrent_convlstm epoch 11/50: train_loss=0.038893, val_loss=0.036722
recurrent_convlstm epoch 12/50: train_loss=0.037550, val_loss=0.035595
recurrent_convlstm epoch 13/50: train_loss=0.036263, val_loss=0.034369
recurrent_convlstm epoch 14/50: train_loss=0.035048, val_loss=0.033513
recurrent_convlstm epoch 15/50: train_loss=0.033831, val_loss=0.032171
recurrent_convlstm epoch 16/50: train_loss=0.032534, val_loss=0.031087
recurrent_convlstm epoch 17/50: train_loss=0.031208, val_loss=0.029880
recurrent_convlstm epoch 18/50: train_loss=0.030056, val_loss=0.029239
recurrent_convlstm epoch 19/50: train_loss=0.028854, val_loss=0.027893
recurrent_convlstm epoch 20/50: train_loss=0.027713, val_loss=0.027391
recurrent_convlstm epoch 21/50: train_loss=0.026591, val_loss=0.025814
recurrent_convlstm epoch 22/50: train_loss=0.025636, val_loss=0.025128
recurrent_convlstm epoch 23/50: train_loss=0.024824, val_loss=0.024295
recurrent_convlstm epoch 24/50: train_loss=0.024151, val_loss=0.024270
recurrent_convlstm epoch 25/50: train_loss=0.023378, val_loss=0.023068
recurrent_convlstm epoch 26/50: train_loss=0.022886, val_loss=0.022717
recurrent_convlstm epoch 27/50: train_loss=0.022466, val_loss=0.022693
recurrent_convlstm epoch 28/50: train_loss=0.022093, val_loss=0.022033
recurrent_convlstm epoch 29/50: train_loss=0.021570, val_loss=0.021762
recurrent_convlstm epoch 30/50: train_loss=0.021276, val_loss=0.021301
recurrent_convlstm epoch 31/50: train_loss=0.021045, val_loss=0.021105
recurrent_convlstm epoch 32/50: train_loss=0.020762, val_loss=0.020881
recurrent_convlstm epoch 33/50: train_loss=0.020576, val_loss=0.020613
recurrent_convlstm epoch 34/50: train_loss=0.020361, val_loss=0.020671
recurrent_convlstm epoch 35/50: train_loss=0.020214, val_loss=0.020306
recurrent_convlstm epoch 36/50: train_loss=0.019987, val_loss=0.020299
recurrent_convlstm epoch 37/50: train_loss=0.019961, val_loss=0.020481
recurrent_convlstm epoch 38/50: train_loss=0.019752, val_loss=0.019921
recurrent_convlstm epoch 39/50: train_loss=0.019566, val_loss=0.019837
recurrent_convlstm epoch 40/50: train_loss=0.019476, val_loss=0.019827
recurrent_convlstm epoch 41/50: train_loss=0.019389, val_loss=0.019684
recurrent_convlstm epoch 42/50: train_loss=0.019262, val_loss=0.019571
recurrent_convlstm epoch 43/50: train_loss=0.019301, val_loss=0.019924
recurrent_convlstm epoch 44/50: train_loss=0.019263, val_loss=0.019588
recurrent_convlstm epoch 45/50: train_loss=0.019090, val_loss=0.019463
recurrent_convlstm epoch 46/50: train_loss=0.019109, val_loss=0.019531
recurrent_convlstm epoch 47/50: train_loss=0.018989, val_loss=0.019698
recurrent_convlstm epoch 48/50: train_loss=0.019009, val_loss=0.019336
recurrent_convlstm epoch 49/50: train_loss=0.018967, val_loss=0.019270
recurrent_convlstm epoch 50/50: train_loss=0.018862, val_loss=0.019301
{
  "protocol": {
    "sequence_length": 7,
    "forecast_horizon_days": 1,
    "train_samples": 1819,
    "validation_samples": 359,
    "test_samples": 358,
    "spatial_shape": [
      121,
      141
    ],
    "device": "cuda:0",
    "seed": 42,
    "metric_space": "same denormalized stored temperature scale for every model",
    "normalization_unit": "degrees_Celsius",
    "normalization_mean_celsius": 25.044549020486595,
    "normalization_std_celsius": 10.99594436868629,
    "loss_threshold_celsius": 37.25411376953127,
    "loss_threshold_normalized": 1.1103698181499058,
    "loss_threshold_metadata": {
      "top_5_percent_celsius": 37.25411376953127,
      "bottom_5_percent_celsius": -1.7535766601562273,
      "quantile_method": "NumPy linear quantile (Hyndman-Fan Type 7)",
      "scope": "training split only; daily maximum t2m over all grid cells and days",
      "training_daily_records": 1826,
      "training_grid_values": 31153386,
      "training_date_range": [
        "2019-01-01",
        "2023-12-31"
      ],
      "input": "data/interim/train_daily.nc (t2m in K)",
      "loss_weight": 5.0
    },
    "pytorch_version": "2.5.1+cu121",
    "cuda_runtime": "12.1",
    "run_timestamp_utc": "2026-10-14T15:25:07.823038+00:00",
    "epochs_requested": 50,
    "output_directory": "C:\\Users\\25mdsml006\\Desktop\\deep_learning\\project\\climate\\climate2\\experiments\\reviewer_recurrent_convlstm_20261014"
  },
  "results": [
    {
      "model": "recurrent_convlstm",
      "class": "RecurrentConvLSTM",
      "trainable_parameters": 38177,
      "epochs": 50,
      "epochs_requested": 50,
      "epochs_completed": 50,
      "batch_size": 16,
      "optimizer": "Adam",
      "learning_rate": 0.0001,
      "loss": "ExtremeWeightedMSE",
      "training_seconds": 489.302,
      "best_epoch": 49,
      "best_validation_loss": 0.01926989517296138,
      "history": [
        {
          "epoch": 1,
          "train_loss": 0.8378030532284787,
          "validation_loss": 0.22433297854402792
        },
        {
          "epoch": 2,
          "train_loss": 0.14300174370669483,
          "validation_loss": 0.09082798449241597
        },
        {
          "epoch": 3,
          "train_loss": 0.08454694948567633,
          "validation_loss": 0.06865772070444148
        },
        {
          "epoch": 4,
          "train_loss": 0.06791528141158715,
          "validation_loss": 0.058402026234113655
        },
        {
          "epoch": 5,
          "train_loss": 0.05755083929551275,
          "validation_loss": 0.05090763047337532
        },
        {
          "epoch": 6,
          "train_loss": 0.051251788117122235,
          "validation_loss": 0.04678356728476027
        },
        {
          "epoch": 7,
          "train_loss": 0.047317366851003545,
          "validation_loss": 0.04424263787982256
        },
        {
          "epoch": 8,
          "train_loss": 0.04424359276890755,
          "validation_loss": 0.04107508856965148
        },
        {
          "epoch": 9,
          "train_loss": 0.04195359540417006,
          "validation_loss": 0.03908424443848755
        },
        {
          "epoch": 10,
          "train_loss": 0.04025808107434658,
          "validation_loss": 0.03760483261683713
        },
        {
          "epoch": 11,
          "train_loss": 0.03889323359257296,
          "validation_loss": 0.03672177571317424
        },
        {
          "epoch": 12,
          "train_loss": 0.037550143701465505,
          "validation_loss": 0.03559547225418298
        },
        {
          "epoch": 13,
          "train_loss": 0.03626306840267621,
          "validation_loss": 0.03436923431961433
        },
        {
          "epoch": 14,
          "train_loss": 0.035047513465478755,
          "validation_loss": 0.03351257668565149
        },
        {
          "epoch": 15,
          "train_loss": 0.033830822331079265,
          "validation_loss": 0.03217094197221424
        },
        {
          "epoch": 16,
          "train_loss": 0.03253373627861341,
          "validation_loss": 0.031086893509263577
        },
        {
          "epoch": 17,
          "train_loss": 0.031208465758122896,
          "validation_loss": 0.02987950918791087
        },
        {
          "epoch": 18,
          "train_loss": 0.030056089456928402,
          "validation_loss": 0.029239185559360878
        },
        {
          "epoch": 19,
          "train_loss": 0.028854070345691422,
          "validation_loss": 0.027893311546548553
        },
        {
          "epoch": 20,
          "train_loss": 0.027712704858889704,
          "validation_loss": 0.02739131685508334
        },
        {
          "epoch": 21,
          "train_loss": 0.026590537933403987,
          "validation_loss": 0.02581358162443275
        },
        {
          "epoch": 22,
          "train_loss": 0.02563613323135334,
          "validation_loss": 0.02512822215161894
        },
        {
          "epoch": 23,
          "train_loss": 0.024823835299333984,
          "validation_loss": 0.02429505040788132
        },
        {
          "epoch": 24,
          "train_loss": 0.024150828046626167,
          "validation_loss": 0.024269548892650917
        },
        {
          "epoch": 25,
          "train_loss": 0.023378427842991392,
          "validation_loss": 0.023067646335972393
        },
        {
          "epoch": 26,
          "train_loss": 0.022885945396857302,
          "validation_loss": 0.02271738830629898
        },
        {
          "epoch": 27,
          "train_loss": 0.022466457277340323,
          "validation_loss": 0.022693121724802513
        },
        {
          "epoch": 28,
          "train_loss": 0.02209342916479759,
          "validation_loss": 0.022032826410039612
        },
        {
          "epoch": 29,
          "train_loss": 0.02157027027651406,
          "validation_loss": 0.021762458202631577
        },
        {
          "epoch": 30,
          "train_loss": 0.021276266281411313,
          "validation_loss": 0.021300644006418144
        },
        {
          "epoch": 31,
          "train_loss": 0.021045416005347903,
          "validation_loss": 0.021104894214026306
        },
        {
          "epoch": 32,
          "train_loss": 0.02076192038427842,
          "validation_loss": 0.02088071997074977
        },
        {
          "epoch": 33,
          "train_loss": 0.020576479730376025,
          "validation_loss": 0.020613065394370453
        },
        {
          "epoch": 34,
          "train_loss": 0.020361121327273156,
          "validation_loss": 0.02067136570163395
        },
        {
          "epoch": 35,
          "train_loss": 0.02021376940568811,
          "validation_loss": 0.020305985827808796
        },
        {
          "epoch": 36,
          "train_loss": 0.01998706299223398,
          "validation_loss": 0.020299369145346725
        },
        {
          "epoch": 37,
          "train_loss": 0.019961116410661162,
          "validation_loss": 0.020481382618131844
        },
        {
          "epoch": 38,
          "train_loss": 0.019751516734494975,
          "validation_loss": 0.019920839928090572
        },
        {
          "epoch": 39,
          "train_loss": 0.019565511560230925,
          "validation_loss": 0.01983655074044414
        },
        {
          "epoch": 40,
          "train_loss": 0.01947611393897157,
          "validation_loss": 0.019826577409454014
        },
        {
          "epoch": 41,
          "train_loss": 0.01938884251081107,
          "validation_loss": 0.019683966737078583
        },
        {
          "epoch": 42,
          "train_loss": 0.01926228452245133,
          "validation_loss": 0.019571401340805965
        },
        {
          "epoch": 43,
          "train_loss": 0.019300537077677354,
          "validation_loss": 0.01992432007809048
        },
        {
          "epoch": 44,
          "train_loss": 0.019263391595399172,
          "validation_loss": 0.019588378905926063
        },
        {
          "epoch": 45,
          "train_loss": 0.01908961017697788,
          "validation_loss": 0.019462546333670616
        },
        {
          "epoch": 46,
          "train_loss": 0.019108874445552367,
          "validation_loss": 0.01953133985238231
        },
        {
          "epoch": 47,
          "train_loss": 0.01898859130839507,
          "validation_loss": 0.019697903453007988
        },
        {
          "epoch": 48,
          "train_loss": 0.019008767415295568,
          "validation_loss": 0.019335787905299145
        },
        {
          "epoch": 49,
          "train_loss": 0.018967051859618278,
          "validation_loss": 0.01926989517296138
        },
        {
          "epoch": 50,
          "train_loss": 0.01886152091289037,
          "validation_loss": 0.019300753574656403
        }
      ],
      "validation": {
        "rmse": 1.3713978052590978,
        "mae": 0.8820029497146606,
        "r2": 0.9837167859077454,
        "correlation": 0.9918877052027177
      },
      "test": {
        "rmse": 1.3785302187070654,
        "mae": 0.8828738331794739,
        "r2": 0.9824873805046082,
        "correlation": 0.991279621560664
      },
      "checkpoint": "experiments\\reviewer_recurrent_convlstm_20261014\\recurrent_convlstm_best.pth",
      "history_file": "experiments\\reviewer_recurrent_convlstm_20261014\\recurrent_convlstm_history.json"
    }
  ]
}