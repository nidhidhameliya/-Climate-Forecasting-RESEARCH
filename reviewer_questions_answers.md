# Reviewer Questions: Evidence Based Answers

**Project reviewed:** ERA5 two metre temperature forecasting pipeline in `climate2`  
**Evidence date:** 14 October 2026 (Asia/Kolkata)

Status labels: **Verified** means supported by the current code/artifacts and the recorded checks; **Needs Experiment** means the claim needs a controlled experiment that has not been completed; **Unable to Confirm** means the project does not preserve enough evidence to resolve it.

## 1. Dataset

**Verified.** The verified hourly source is `data/interim/region_subset_raw_verified.nc`. Its current NetCDF metadata reports variable `t2m`, units K, 61,368 hourly timestamps from 2019-01-01 00:00 through 2025-12-31 23:00, and dimensions `(time=61368, latitude=121, longitude=141)`. Latitude runs from 35.0°N down to 5.0°N; longitude runs from 65.0°E through 100.0°E. The inclusive coordinate steps are 0.25° in both directions, giving bounds 5–35°N, 65–100°E and a 0.25° grid. The timestamps are hourly ERA5 values of 2 m air temperature. The source and split files were not modified during this review.

## 2. Preprocessing, missing values, and normalization

**Verified.** The new downstream builder `preprocessing/rebuild_downstream.py` reads the existing hourly split files in storage-aligned time chunks. It takes the maximum of exactly 24 hourly values for each UTC day and carries partial days across storage-chunk boundaries. It rejects non-finite hourly values; there is no imputation. The checked hourly splits were finite, and the serialized daily output files were checked for finite values, expected timestamps, dimensions, and Kelvin units before atomic replacement. The old `data/interim/daily_resampled.nc` was separately rechecked in 32-day chunks and contains 43,624,977 NaNs out of 43,624,977 cells, so it must not be used.

Normalization is a single global scalar z-score from **training daily values only**, after converting Kelvin to Celsius: `z = (daily_max_K - 273.15 - mean_C) / std_C`. The current `data/processed/mean_std.json` contains mean 25.0445490205 °C, population standard deviation 10.9959443687 °C, and 31,153,386 training grid values. Both statistics were finite and the standard deviation was positive. Inverse normalization to Celsius is `z * std_C + mean_C`; convert that Celsius result to Kelvin by adding 273.15. Do not subtract 273.15 from these Celsius statistics.

The old `evaluate_model.py` assumes its loaded mean is in Kelvin and subtracts 273.15 after denormalization. That convention conflicts with the current `mean_std.json`, which explicitly stores Celsius. Use the corrected Celsius inverse transform in `run_baseline_experiments.py` or fix the evaluator before using it with the current stats. The extreme-threshold file `data/processed/extreme_thresholds.json` is absent; training logs record a fallback threshold of 0 normalized units with `ExtremeWeightedMSE` and extreme weight 5.0. This is not the intended 95th-percentile threshold and should be disclosed or corrected for a final experiment.

## 3. Splits, record counts, and the 1,089 claim

**Verified.** Split boundaries are calendar years. Daily sequence count is `daily records - input window (7)`, since each sample predicts the next day. Shapes below are from the rebuilt arrays and the successful preprocessing verifier.

| Split | Hourly date range (inclusive) | Hourly records | Daily date range | Daily records | Sequences | X shape; y shape |
|---|---|---:|---|---:|---:|---|
| Train | 2019-01-01 00:00 – 2023-12-31 23:00 | 43,824 | 2019-01-01 – 2023-12-31 | 1,826 | 1,819 | `(1819,7,1,121,141)`; `(1819,1,121,141)` |
| Validation | 2024-01-01 00:00 – 2024-12-31 23:00 | 8,784 | 2024-01-01 – 2024-12-31 | 366 | 359 | `(359,7,1,121,141)`; `(359,1,121,141)` |
| Test | 2025-01-01 00:00 – 2025-12-31 23:00 | 8,760 | 2025-01-01 – 2025-12-31 | 365 | 358 | `(358,7,1,121,141)`; `(358,1,121,141)` |

The 1,089 count appears in the old `outputs/evaluation/train_results.json`, whose metadata says `split=train`, `num_samples=1089`. It does not match the rebuilt train tensor (1,819 sequences) and is not the current validation or test count. Its provenance cannot be recovered from the saved artifact; describe it as a stale result from a different/older preprocessing or sample selection, not as the current split size. Old validation output also says 358 samples, while the rebuilt 2024 validation tensor has 359. Current test count 358 is consistent with 365 days minus seven input days.

## 4. Model architecture and relation to Figure 3

**Verified.** Despite its class and file names (`ConvLSTMModel`, `models/convlstm.py`), the proposed implementation is a **Conv3D encoder-decoder, not a genuine ConvLSTM**. For input `B×7×1×121×141`, it permutes to Conv3D order `B×1×7×121×141`, then applies:

| Layer | Configuration | Output tensor for this input | Trainable parameters |
|---|---|---|---:|
| Conv3D | 1→32 channels, kernel 3×3×3, padding 1 | B×32×7×121×141 | 896 |
| ReLU | elementwise | B×32×7×121×141 | 0 |
| Conv3D | 32→32, kernel 3×3×3, padding 1 | B×32×7×121×141 | 27,680 |
| ReLU | elementwise | B×32×7×121×141 | 0 |
| Conv3D decoder | 32→1, kernel 3×3×3, padding 1 | B×1×7×121×141 | 865 |
| Last time index | `out[:, :, -1, :, :]` | B×1×121×141 | 0 |

Total trainable parameters: **29,441**. The convolutions mix the seven input frames locally along time and space. There are no recurrent gates, cell state, or recurrent update. The repository also contains an independent per-grid-cell LSTM baseline, a CNN plus pooled-feature LSTM, and a pooled-feature Transformer in `models/`.

The manuscript/Figure 3 source file was not present in the project inventory, so its exact blocks and arrows cannot be checked. The project documentation itself marks the Figure 3 explanation as partial. Correct the figure/caption to match the code if it depicts ConvLSTM gates or recurrent state; compare it with the LSTM baseline only after the manuscript figure is supplied.

Training configuration in `config.yaml`: input length 7 days, hidden dimension 32, batch size 8, 100 epochs, Adam learning rate 1e-4, CUDA requested, and `ExtremeWeightedMSE`. The recorded smoke test overrode batch size to 16 and epochs to 1; the interrupted comparison requested 50 epochs, batch size 16, seed 42.

## 5. Metric verification

**Verified for the artifacts named below; the manuscript's four-number test claim is not verified.**

| Metric/source | RMSE (°C) | MAE (°C) | R² | Pearson r | Evidence/status |
|---|---:|---:|---:|---:|---|
| Manuscript values queried | 1.8886 | 1.6200 | 0.9720 | 0.2477 | Not a reproducible aligned test result. 1.8886/1.6200 occur in the old train report, while 0.9720 occurs as Pearson correlation in the old test report; 0.2477 is not found in project result artifacts. |
| Historical saved test report, 358 samples | 1.88236 | 1.61278 | Not saved | 0.972017 | `outputs/evaluation/test_results.json`; dated from the old artifact set and cannot be regenerated from saved prediction arrays (none found). Treat as historical, not verified against the rebuilt split. |
| Current Conv3D one-epoch smoke checkpoint, rebuilt test tensors, 358 target dates | 1.93163 | 1.25357 | 0.965615 | 0.982838 | Recalculated from aligned model predictions and targets in the follow-up diagnostic. This is a smoke-only result, not a final trained model result. |
| Persistence, same 358 target dates | 1.40272 | 0.89750 | 0.981867 | 0.990937 | Recalculated from the final input day and exact same targets. Persistence outperforms the one-epoch smoke model; do not present the smoke result as a final model comparison. |

The old train report is the source of RMSE 1.8886117 °C and MAE 1.6200423 °C, with 1,089 samples. The old validation report has MAE 1.6200051 °C. The old test report's 0.9720169 is Pearson correlation, not R²: `evaluate_model.py` computes a correlation but does not compute R², and its JSON has no R² field. The Pearson value 0.2477 is not reproduced. The current smoke test directly computes all four metrics on 6,107,838 aligned grid values (358×121×141); those results differ from the manuscript claim. The old result JSON has no saved prediction arrays, so the historical checkpoint metrics cannot be independently recalculated with current data and current normalization.

## 6. Baseline and input-window comparisons

**Verified baseline; learned-model/window ablation needs experiment.** A no-training persistence forecast was calculated from the last input day. Natural per-window target ranges differ, so do not compare their scores as if they used identical dates. The 14-day range (2025-01-15–2025-12-31) is the common target subset for a fair 3/7/14-day window comparison. Older prose in `research.md`/`README.md` cites persistence RMSE 1.1277 °C and Conv3D RMSE 1.8823 °C, but those figures predate the repaired normalization and lack a present matching results JSON/prediction arrays; they are historical claims, not valid current comparisons. `experiments/exp_01_baseline/metrics.json` is empty, and no completed result artifacts were found for the older ConvLSTM/Transformer folders. The `revision/` directory contains analysis scripts, not completed generated comparison tables.

| Input window | Test sequences | Natural target dates | Persistence RMSE (°C) | Persistence MAE (°C) |
|---:|---:|---|---:|---:|
| 3 days | 362 | 2025-01-04 – 2025-12-31 | 1.40706 | 0.89967 |
| 7 days | 358 | 2025-01-08 – 2025-12-31 | 1.40272 | 0.89750 |
| 14 days | 351 | 2025-01-15 – 2025-12-31 | 1.39585 | 0.89276 |

On the common 351 dates, persistence has RMSE 1.39585 °C and MAE 0.89276 °C. No controlled learned-model experiment for 3-, 7-, and 14-day inputs has completed. The five-model 50-epoch run stopped after LSTM completed and CNN-LSTM reached epoch 3; only partial checkpoints exist and no final comparison JSON/CSV was written. The process is no longer available, and Windows process enumeration via CIM/tasklist returned access denied; the available PowerShell Python-process query returned no Python processes. Do not treat partial checkpoints as completed benchmark results.

## 7. Seasonal and spatial errors

**Verified for the one-epoch smoke checkpoint only; final-model error analysis needs experiment.** The aligned smoke predictions were grouped by target date into meteorological seasons. Persistence is included as context, not as a learned model. All errors are °C.

| Season | Target days | Smoke Conv3D RMSE | Smoke Conv3D MAE | Persistence RMSE | Persistence MAE |
|---|---:|---:|---:|---:|---:|
| DJF | 83 | 2.0990 | 1.2980 | 1.3465 | 0.8535 |
| MAM | 92 | 2.1013 | 1.3813 | 1.5330 | 0.9954 |
| JJA | 92 | 1.7727 | 1.2058 | 1.4427 | 0.9304 |
| SON | 91 | 1.7377 | 1.1323 | 1.2677 | 0.8054 |

Across 2025 target dates 2025-01-08–2025-12-31, smoke-model per-gridpoint RMSE ranges from 0.3927 to 14.5471 °C (mean of gridpoint RMSEs 1.5736 °C). The highest-error grid point is 35.0°N, 65.0°E at 14.5471 °C RMSE. These are diagnostic smoke results only; the substantial worst-point error and persistence advantage make a final trained error analysis necessary.

## 8. Reproducibility and next commands

**Verified environment:** Windows project virtual environment; Python 3.11.9, PyTorch 2.5.1+cu121, CUDA runtime 12.1, NumPy 2.4.2, xarray 2026.2.0, SciPy 1.17.1, scikit-learn 1.8.0; GPU NVIDIA GeForce RTX 4070. PyTorch reported CUDA available. The command outputs and exits are recorded in `terminal_outputs.md`.

The following commands reproduce preprocessing and a new, separate smoke/full run without reusing or overwriting prior experiment folders:

```powershell
.\.venv\Scripts\python.exe -u preprocessing\rebuild_downstream.py
.\.venv\Scripts\python.exe -u verify_preprocessing.py
.\.venv\Scripts\python.exe -u run_baseline_experiments.py --epochs 1 --batch-size 16 --seed 42 --device cuda --models convlstm --output-dir experiments\reviewer_smoke_20261014
```

After preprocessing passes and the smoke command exits 0, a complete comparison can be run in a fresh directory:

```powershell
.\.venv\Scripts\python.exe -u run_baseline_experiments.py --epochs 50 --batch-size 16 --seed 42 --device cuda --models persistence,lstm,cnn_lstm,convlstm,transformer --output-dir experiments\reviewer_full_20261014
```

The current aligned smoke seasonal/spatial and persistence calculation is reproducible with:

```powershell
.\.venv\Scripts\python.exe -u experiments\reviewer_followup_analysis_20261014\analyze_smoke.py
```

That script writes only `experiments/reviewer_followup_analysis_20261014/followup_analysis.json`. It does not save raw model predictions. A proper learned-model 3/7/14-day ablation requires generating separate sequences for each window, training and selecting each model using validation only, and evaluating the same 351 test target dates. Do not reuse the current seven-day checkpoint as if it had been trained on the other windows.

## Unresolved items and manuscript corrections

- Mark validation/test value-for-value equality against the raw source **unverified**. Their date bounds, hourly cadence, dimensions, Kelvin units, and finite values passed; only train/source equality was previously verified.
- Replace the stale 1,089 sample claim with 1,819 train, 359 validation, and 358 test sequences under the verified 7-day/1-day protocol; explain the old count as an unreconciled historical artifact.
- Rename the proposed method “Conv3D encoder-decoder” unless the code is changed to implement recurrent ConvLSTM cells. Update Figure 3 and its caption using the actual manuscript figure.
- Report R² and Pearson r as distinct metrics, recomputed from the same held-out predictions. Remove or correct the unsupported 0.2477 correlation claim.
- Do not report historical or one-epoch smoke scores as the final test result. A completed training/comparison and final held-out analysis remain outstanding; current persistence already outperforms the smoke checkpoint.
- Correct `evaluate_model.py` for the Celsius normalization metadata before using it. Decide whether to generate a proper training-only extreme threshold or explicitly describe the current fallback loss.
- Explain that validation/test source equality and the provenance of the manuscript's Figure 3 and 1,089 count remain unconfirmed.

## Point-by-point reviewer response draft

1. **Dataset:** “We now specify the exact ERA5 `t2m` subset: hourly Kelvin data for 2019-01-01 00:00 through 2025-12-31 23:00, 5–35°N and 65–100°E on a 0.25° grid (121×141).”
2. **Preprocessing:** “We aggregate each complete UTC day as the maximum of its 24 hourly values, reject non-finite input values, and calculate global z-score statistics from the training split only after Kelvin-to-Celsius conversion. We have corrected the inverse transform convention and excluded the all-NaN legacy daily file.”
3. **Splits:** “The verified seven-day input / next-day target splits contain 1,819 train, 359 validation, and 358 test sequences. The earlier 1,089 count belongs to an unreconciled historical train artifact and is not the current split size.”
4. **Architecture:** “The implementation previously called ConvLSTM is actually a three-layer Conv3D encoder-decoder with 29,441 trainable parameters. We will relabel the method and revise Figure 3/caption, or provide a new genuine ConvLSTM implementation and results.”
5. **Metrics:** “The four manuscript numbers do not form a verified held-out result. The saved historical test artifact reports RMSE 1.88236 °C, MAE 1.61278 °C and Pearson r 0.97202 but no R² and no preserved prediction arrays. A fresh one-epoch diagnostic gives different metrics and is not a final result; 0.2477 remains unsupported.”
6. **Comparisons:** “We have calculated persistence on the rebuilt test split. It outperforms the one-epoch smoke model. We will complete matched-date learned-model comparisons and the 3/7/14-day input ablation before making comparative performance claims.”
7. **Error analysis:** “We provide seasonal and spatial diagnostics for the smoke checkpoint as preliminary only. Final error analysis will be rerun using the completed selected model and the aligned held-out dates.”
8. **Reproducibility:** “We report the verified Python/PyTorch/CUDA/GPU environment and provide the preprocessing, validation, smoke, and full-comparison commands. The complete 50-epoch comparison and learned-model window ablation are still pending.”

## Files changed and validation record

Exact files created or modified during this project session:

- Added: `reviewer_questions_answers.md`, `preprocessing/rebuild_downstream.py`, `verify_preprocessing.py`, `experiments/reviewer_followup_analysis_20261014/analyze_smoke.py`, `experiments/reviewer_followup_analysis_20261014/followup_analysis.json`, and `terminal_outputs.md`.
- Modified: `run_baseline_experiments.py`, `training/losses.py`, `data/processed/mean_std.json`, `data/processed/train.npy`, `data/processed/val.npy`, `data/processed/test.npy`, `data/processed/tensors/train_X.npy`, `train_y.npy`, `val_X.npy`, `val_y.npy`, `test_X.npy`, `test_y.npy`, and the generated `data/interim/train_daily.nc`, `val_daily.nc`, `test_daily.nc`.
- Experiment outputs created by this work: `experiments/reviewer_baselines_verified_20261013_smoke_retry2/convlstm_best.pth`, `comparison_results.json`, `comparison_results.csv`; partial full-run outputs `experiments/reviewer_baselines_verified_20261013/lstm_best.pth` and `cnn_lstm_best.pth`.
- Backups created: `backups/terminal_outputs_before_repair_20261013_233505.md`, `backups/pipeline_20261013_222743/run_baseline_experiments.py`, `backups/losses_20261013_235847/losses.py`, and `backups/pre_chunked_20261013_233446/{train_daily.nc,val_daily.nc,test_daily.nc}`.
- Deleted: `file.tmp` (0 bytes, confirmed empty).

The raw verified source `data/interim/region_subset_raw_verified.nc`, hourly splits `train.nc`/`val.nc`/`test.nc`, `revision/`, historical `outputs/` reports, and historical `experiments/latest/model.pth` checkpoint were preserved. The preprocessing verifier exited 0; the smoke experiment exited 0; the follow-up aligned-metric/season/spatial analysis exited 0. The five-model run is incomplete and has no captured final exit code or aggregate results file. See `terminal_outputs.md` for commands and actual outcomes.
