# Visualization audit

The earlier PNGs in this directory were generated from legacy predictions and do not represent the corrected selected checkpoint/results. The old training-set images have been removed because they cannot be reproduced from the verified current experiment logs. The old validation/test images have been replaced with updated plots generated from `experiments/reviewer_final_20261014/convlstm_best.pth` and the current stored tensors.

Run `python outputs/visualizations/generate_verified_visualizations.py` from the repository root to recreate the current plots. It performs fresh inference; it does not retrain a model. It uses training-only Celsius normalization from `data/processed/mean_std.json`.

## Current images

- `test_evaluation.png`: observed-vs-predicted density and residual distribution on the 2025 held-out test set.
- `test_prediction_map.png`: previous day, ERA5 target, fresh Conv3D prediction, and absolute error for a median-grid-RMSE 2025 test date.
- `val_evaluation.png`: the same diagnostic for 2024 validation data; validation is for model/checkpoint selection, not the final test estimate.
- `val_prediction_map.png`: a median-grid-RMSE 2024 validation example.
- `model_comparison_test.png`: verified six-method comparison from `experiments/reviewer_comparison_with_recurrent_convlstm_20261014/comparison_results.csv`, on 358 aligned 2025 targets.
- `training_validation_curves.png`: actual epoch histories; the repaired 50-epoch LSTM log is used.
- `window_seasonal_errors.png`: verified matched-date window ablation and 2025 seasonal errors.
- `spatial_test_errors.png`: per-grid-cell signed bias and RMSE recomputed from the selected checkpoint over the 2025 test period.

The test metrics reproduce the reported values to the displayed precision. Small last-decimal differences can result from running fresh inference on the available device. All reference targets are ERA5 reanalysis; they are not independent station observations. Spatial plots cover the full rectangular grid, including ocean cells, without a land mask or administrative outlines.
