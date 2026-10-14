# Reviewer Questions: Evidence Based Answers

Evidence reflects project artifacts and the corrected 50-epoch RTX 4070 experiment completed 2026-10-14. **Verified** means directly checked against code/data/results; **Needs Experiment** means the experiment is not complete; **Unable to Confirm** means project evidence is insufficient.

## 1. Dataset — Verified

Source: `data/interim/region_subset_raw_verified.nc`. Variable `t2m`, hourly 2 m temperature, units K. Times: 2019-01-01 00:00 through 2025-12-31 23:00 UTC (61,368 hourly records). Coordinates: latitude 35 to 5 degrees N descending; longitude 65 to 100 degrees E; 0.25-degree spacing; dimensions time=61,368, latitude=121, longitude=141. Validation and test source value equality remains unverified; their split date/cadence/dimension/finite checks passed. The source file was preserved.

## 2. Preprocessing — Verified

Hourly values are grouped into complete UTC calendar days; each daily cell is the maximum of the 24 hourly `t2m` readings. Non-finite hourly values are rejected rather than imputed. The invalid legacy `data/interim/daily_resampled.nc` contains only NaNs and was not used. Current split daily files and normalized arrays pass `verify_preprocessing.py`.

Kelvin daily maxima are converted to Celsius before normalization. Training-only global statistics: mean 25.0445490205 C, population standard deviation 10.9959443687 C, from 31,153,386 values. `z=(C-mean_C)/std_C`; inverse is `C=z*std_C+mean_C`. The evaluator was corrected to respect the stats unit and no longer applies an erroneous Kelvin-to-Celsius subtraction to Celsius statistics.

The corrected extreme threshold is training-only daily 95th percentile = 37.2541137695 C (NumPy linear/Hyndman-Fan Type 7), based on the 1,826 training daily maps and 31,153,386 grid values. It is mapped to normalized units as `(threshold_C-mean_C)/std_C = 1.1103698181`; `ExtremeWeightedMSE` uses weight 5 for targets above that threshold. `data/processed/extreme_thresholds.json` records scope, method, date range and count.

## 3. Splits and counts — Verified

All use a seven-day input and next-day target; sequences do not cross split boundaries.

| Split | Hourly range, inclusive UTC | Hourly records | Daily range | Daily records | Input-target sequences |
|---|---|---:|---|---:|---:|
| Train | 2019-01-01 00:00–2023-12-31 23:00 | 43,824 | 2019-01-01–2023-12-31 | 1,826 | 1,819 |
| Validation | 2024-01-01 00:00–2024-12-31 23:00 | 8,784 | 2024-01-01–2024-12-31 | 366 | 359 |
| Test | 2025-01-01 00:00–2025-12-31 23:00 | 8,760 | 2025-01-01–2025-12-31 | 365 | 358 |

The manuscript's 1,089 sample figure matches an old `outputs/evaluation/train_results.json` with `split=train`, but not the current verified tensor (1,819 sequences). Its provenance cannot be reconstructed and it should be removed or explicitly identified as a stale historical subset.

## 4. Model architecture — Verified

The proposed implementation is a Conv3D encoder-decoder, not ConvLSTM: code class `ConvLSTMModel` in `models/convlstm.py` contains no recurrence, gates, or cell state. Input Bx7x1x121x141 is permuted to Bx1x7x121x141. Conv3D(1,32,kernel 3x3x3,padding 1) gives Bx32x7x121x141 (896 parameters); ReLU; Conv3D(32,32,3x3x3,padding 1) same shape (27,680 parameters); ReLU; Conv3D(32,1,3x3x3,padding 1) gives Bx1x7x121x141 (865 parameters); last time index gives Bx1x121x141. Total 29,441 trainable parameters. A genuine ConvLSTM comparator has now been implemented separately in `models/recurrent_convlstm.py`. It has one recurrent layer with 32 hidden channels. At each time step, a 3x3 convolution on concatenated input and hidden state produces input/forget/output/candidate maps; sigmoid/tanh gates update hidden and cell states. After seven steps, a 1x1 Conv2d maps the final hidden state to the next-day grid. It has 38,177 parameters. The legacy `convlstm` key still selects the distinct 29,441-parameter Conv3D model. The historic Figure 3 source remains unavailable, so the new baseline should not be described as the exact historical Figure 3 implementation.

Experiment config: seven input days, one-day horizon, hidden dim 32, batch 16, Adam lr 1e-4, seed 42, 50 epochs, weighted MSE threshold above, CUDA RTX 4070. Best checkpoint selected only by validation loss.

## 5. Metrics — Verified aligned results

Fresh predictions and targets have matching shapes and were aligned against daily targets. Values below are Celsius errors; R2 and Pearson r are separately computed across the same flattened test grid values.

| Model | Actual epochs | Best validation epoch | Test RMSE C | Test MAE C | Test R2 | Test Pearson r |
|---|---:|---:|---:|---:|---:|---:|
| Persistence (last input day) | 0 | n/a | 1.402716 | 0.897498 | 0.981867 | 0.990937 |
| LSTM | 50 | 50 | 1.572731 | 1.016080 | 0.977206 | 0.988568 |
| CNN-LSTM | 50 | 48 | 1.400517 | 0.898668 | 0.981924 | 0.990928 |
| Conv3D encoder-decoder | 50 | 39 | 1.364915 | 0.874530 | 0.982832 | 0.991407 |
| Transformer | 50 | 36 | 1.403025 | 0.898712 | 0.981860 | 0.990936 |
| ConvLSTM baseline | 50 | 49 | 1.378530 | 0.882874 | 0.982487 | 0.991280 |

The selected Conv3D checkpoint was independently evaluated with `evaluate_model.py` on both validation and test: 359 aligned validation samples (2024-01-08 through 2024-12-31) and 358 aligned test samples (2025-01-08 through 2025-12-31). Validation metrics match the runner; test evaluator vs runner deltas were below 2.4e-8 for all four statistics. The earlier r=0.2477 cannot be traced or explained from available evidence: its source predictions, exact targets, and calculation code are absent. Misalignment, aggregation differences, or a bug are possible explanations but none is verified. The old 0.9720 also cannot be paired with 0.2477 as metrics from the current aligned predictions. Withdraw the old pair unless its original evaluation artifacts are recovered. Current Conv3D test values are R2=0.982832 and Pearson r=0.991407.

## 6. Comparisons and window ablation — Verified

Six-model results above use identical test dates. The added ConvLSTM used the same split and training protocol (seed 42, batch 16, Adam 1e-4, 50 epochs; validation-selected checkpoint). Conv3D RMSE is 1.364915 C versus 1.378530 C for ConvLSTM, a small 0.013615 C gap that is not significance-tested. Persistence is a legitimate baseline and remains strong; Conv3D improves on it by 0.03780 C RMSE and 0.02297 C MAE on the full 358 test dates. These are single-seed results, not significance tests. The separate Conv3D 3/7/14-day ablation completed 50 epochs per window. The common test dates are 2025-01-15 through 2025-12-31 (351 targets), with each checkpoint selected by its own validation loss; the test set was not used for selection.

| Input days | Completed epochs | Best validation epoch | Common test RMSE C | MAE C | R2 | Pearson r |
|---:|---:|---:|---:|---:|---:|---:|
| Persistence baseline | 0 | n/a | 1.395853 | 0.892756 | 0.981761 | 0.990882 |
| 3 | 50 | 48 | 1.367838 | 0.873910 | 0.982486 | 0.991278 |
| 7 | 50 | 41 | 1.361286 | 0.872670 | 0.982653 | 0.991375 |
| 14 | 50 | 40 | 1.358829 | 0.868374 | 0.982716 | 0.991394 |

The persistence row is computed on the same 351 target dates. The 14-day window is best among the learned windows by RMSE/MAE on this matched test subset, with small differences; this single-seed result does not establish statistical significance. Full histories, checkpoints and aggregate CSV/JSON are in `experiments/reviewer_final_20261014/window_ablation_final/`.

## 7. Error analysis — Verified

**Verified.** Final-checkpoint seasonal and gridpoint errors are in `experiments/reviewer_final_20261014/error_analysis.json`.

| Season | Target days | RMSE C | MAE C |
|---|---:|---:|---:|
| DJF | 83 | 1.307819 | 0.828338 |
| MAM | 92 | 1.494154 | 0.971866 |
| JJA | 92 | 1.395633 | 0.904881 |
| SON | 91 | 1.242129 | 0.787571 |

Gridpoint RMSE ranges from 0.286931 C at 14.75 N, 67.5 E to 5.539139 C at 35 N, 100 E; unweighted mean of per-gridpoint RMSE is 1.175518 C. At the specifically queried 35 N, 65 E location, all 8,760 hourly test values are finite and the 365 daily maxima match stored daily values exactly. The 358 forecast targets align within 1.91e-6 C. Its largest absolute error is 14.294018 C on 2025-02-11 (input previous-day Tmax -1.920654 C; observed -10.193449 C; predicted 4.100569 C). The maximum RMSE gridpoint is elsewhere; these are distinct error summaries. Test data were not altered.

## 8. Reproducibility — Verified environment and commands

Verified environment: Python 3.11.9, PyTorch 2.5.1+cu121, CUDA runtime 12.1, RTX 4070; recorded dependency versions include NumPy 2.4.2, xarray 2026.2.0, SciPy 1.17.1 and scikit-learn 1.8.0.

```powershell
.\.venv\Scripts\python.exe -u preprocessing\compute_extremes.py
.\.venv\Scripts\python.exe -u verify_preprocessing.py
.\.venv\Scripts\python.exe -u run_baseline_experiments.py --epochs 50 --batch-size 16 --seed 42 --device cuda --models persistence,lstm,cnn_lstm,convlstm,transformer --output-dir experiments\reviewer_final_20261014
.\.venv\Scripts\python.exe -u experiments\reviewer_final_20261014\run_window_ablation.py --output-dir experiments\reviewer_final_20261014\window_ablation_NEW_RUN
```

The first two commands reproduce the corrected threshold and validate saved preprocessing. The run output directory is intentionally fixed and existing result outputs are protected from overwrite; use a new output directory for a new run. Evaluation cross-check command is recorded in `terminal_outputs.md`.

## Unresolved issues

- Validation/test hourly values have not been compared value-for-value with the verified raw source; their structural/finite checks passed.
- The original manuscript/Figure 3 source was unavailable for exact reconciliation; the newly added ConvLSTM is an explicit comparator, not a claim about the historical figure implementation.
- Six-method comparison is one seed and one split; uncertainty across seeds is not estimated.
- The 1,089 historical sample count's original selection rule is unknown.

## Recommended manuscript corrections

1. Replace the 1,089 count with 1,819/359/358 train/validation/test sequences for the stated seven-day next-day protocol; give hourly and daily counts in the table above.
2. Describe hourly-to-daily maximum aggregation and training-only Celsius z-score. Distinguish R2 from Pearson correlation.
3. Rename the proposed architecture Conv3D encoder-decoder, show its three Conv3D layers, and label the separately implemented ConvLSTM as a baseline.
4. Replace historical metric quartet with the corrected aligned test table and disclose single-seed protocol and strong persistence baseline.
5. State validation/test source-value equality as unverified until that comparison is run.

## Point-by-point reviewer response draft

1. **Dataset:** “We specify ERA5 hourly t2m in Kelvin, 2019-01-01 00:00 to 2025-12-31 23:00 UTC, over 5–35 N and 65–100 E at 0.25-degree resolution (121x141).”
2. **Preprocessing:** “We use the maximum of each complete 24-hour UTC day, reject rather than impute non-finite values, and normalize Celsius daily maxima using training-only global mean and standard deviation. The inverse transform is corrected.”
3. **Splits:** “The current seven-day/next-day protocol has 1,819 train, 359 validation, and 358 test sequences. The 1,089 figure came from a stale artifact whose subset provenance is unavailable.”
4. **Architecture:** "The proposed model is a 29,441-parameter Conv3D encoder-decoder. We added a separate 38,177-parameter ConvLSTM baseline with one layer and 32 hidden channels. The historical Figure 3 source is unavailable, so we cannot confirm that it matches this baseline."
5. **Metrics:** “We reevaluated aligned 2025 predictions and targets. The selected Conv3D obtains RMSE 1.364915 C, MAE 0.874530 C, R2 0.982832, and Pearson r 0.991407. R2 and correlation are reported as distinct statistics; prior unsupported historical values are withdrawn.”
6. **Comparisons:** “We provide persistence, LSTM, CNN-LSTM, Conv3D, and Transformer comparisons with checkpoints selected on validation data only. We also report the 3/7/14-day Conv3D ablation on the same 351 test target dates.”
7. **Error analysis:** “At 35 N, 65 E, source daily aggregation and prediction-date alignment were checked; the largest absolute error is traced to 2025-02-11. We do not modify held-out observations.”
8. **Reproducibility:** “We provide the environment versions and exact preprocessing, verification, model-comparison, and ablation commands, together with saved histories and checkpoints.”

## Artifact paths

- Original five-method run: `experiments/reviewer_final_20261014/`; six-method merged table: `experiments/reviewer_comparison_with_recurrent_convlstm_20261014/comparison_results.csv`; ConvLSTM checkpoint and metrics: `experiments/reviewer_recurrent_convlstm_20261014/`.
- Incremental completion ledger: `experiments/reviewer_final_20261014/completed_results.json`.
- Checkpoints/histories: CNN-LSTM, Conv3D and Transformer are under `experiments/reviewer_final_20261014/`; the verified 50-epoch LSTM checkpoint/history are under `experiments/reviewer_lstm_repaired_20261014/`. The tracked six-epoch LSTM files in the main directory are preserved as historical partial artifacts and are not the checkpoint used for the reported LSTM metrics. Persistence has no checkpoint.
- Extreme threshold: `data/processed/extreme_thresholds.json`.
- High-error trace and seasonal/spatial aggregate: `experiments/reviewer_final_20261014/high_error_point_35N_65E.json` and `experiments/reviewer_final_20261014/error_analysis.json`.
- Matched-date window ablation artifacts: `experiments/reviewer_final_20261014/window_ablation_final/`.
- Command records: `terminal_outputs.md`.

## Documentation status (2026-10-14)

README and change-log summaries were synchronized with the artifacts listed above. This does not change any data, checkpoint, metric, or experiment output. Exact raw-source value equality for validation/test remains **Unable to Confirm**; no new model training was performed as part of the documentation update.
