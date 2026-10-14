# Project Change Log

## 2026-10-14: ConvLSTM baseline added

- Implemented a genuine one-layer ConvLSTM baseline (`models/recurrent_convlstm.py`): 32 hidden channels, 3?3 gate convolution, seven recurrent input steps, and 1?1 output projection (38,177 trainable parameters).
- Trained for 50 epochs with seed 42, batch size 16, Adam at 1e-4, and validation-selected checkpoint (best epoch 49).
- Independent 2025 test metrics: RMSE 1.378530 degrees C, MAE 0.882874 degrees C, R2 0.982487, Pearson r 0.991280. Compared with Conv3D RMSE 1.364915 degrees C and persistence 1.402716 degrees C; this single-seed gap is not significance-tested.
- Updated `brief.md`, `research.md`, `reviewer_questions_answers.md`, README, and conference speaking notes. Created a six-method comparison CSV and regenerated comparison figures.
- The historic `r=0.2477` source remains unavailable; its cause is not established and should not be guessed.


This log summarizes material project updates. Detailed command output remains in `terminal_outputs.md`; experiment artifacts are preserved in their listed directories.

## 2026-10-14: Verified ERA5 forecasting and reviewer documentation

- Corrected the evaluator inverse transform to produce Celsius consistently and checked prediction/target sample alignment.
- Rebuilt downstream preprocessing artifacts and training-only normalization/extreme threshold; preprocessing verification passed.
- Completed a 50-epoch, seed-42 comparison (persistence, LSTM, CNN-LSTM, Conv3D encoder-decoder, Transformer) on the RTX 4070. Selected learned checkpoints by validation loss, then evaluated on test data.
- Repaired the LSTM run in `experiments/reviewer_lstm_repaired_20261014/` after detecting that the earlier partial history/checkpoint did not match the aggregate. Preserved the earlier files.
- Completed matched-date 3/7/14-day Conv3D ablation; saved histories, checkpoints, and aggregate results in `experiments/reviewer_final_20261014/window_ablation_final/`.
- Added seasonal/spatial error analysis and the 35?N, 65?E input/target alignment trace.
- Updated README and reviewer answers with verified metrics, architecture naming (Conv3D, not ConvLSTM), commands, artifact locations, and limitations.
- Source equality of validation/test against the verified raw hourly file remains unverified. Results use one seed and one temporal split; no significance testing or independent station validation is available.

### Main test comparison

| Model | Completed epochs | Best epoch | RMSE degrees C | MAE degrees C | R-squared | Pearson r |
|---|---:|---:|---:|---:|---:|---:|
| Persistence | 0 | ? | 1.402716 | 0.897498 | 0.981867 | 0.990937 |
| LSTM | 50 | 50 | 1.572731 | 1.016080 | 0.977206 | 0.988568 |
| CNN-LSTM | 50 | 48 | 1.400517 | 0.898668 | 0.981924 | 0.990928 |
| Conv3D encoder-decoder | 50 | 39 | 1.364915 | 0.874530 | 0.982832 | 0.991407 |
| Transformer | 50 | 36 | 1.403025 | 0.898712 | 0.981860 | 0.990936 |

### Matched-date window ablation (351 test dates)

| Input days | Completed epochs | Best epoch | RMSE degrees C | MAE degrees C | R-squared | Pearson r |
|---:|---:|---:|---:|---:|---:|---:|
| Persistence | 0 | ? | 1.395853 | 0.892756 | 0.981761 | 0.990882 |
| 3 | 50 | 48 | 1.367838 | 0.873910 | 0.982486 | 0.991278 |
| 7 | 50 | 41 | 1.361286 | 0.872670 | 0.982653 | 0.991375 |
| 14 | 50 | 40 | 1.358829 | 0.868374 | 0.982716 | 0.991394 |

## 2026-10-14: Documentation synchronization

- Updated README evidence, reproduction pointers, remaining work, repository clone URL, and model headings.
- Linked the reviewer report and terminal log; retained all existing terminal log content.
- No datasets, source files, `revision/`, experiment results, or checkpoints were deleted or overwritten.
