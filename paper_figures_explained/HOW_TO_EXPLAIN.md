# Explainable figures for the paper and conference

These figures use the verified 2019–2025 ERA5 study files, saved model checkpoints, and the aligned 2025 test tensors. Each is available as a 600-dpi PNG. The script `generate_relevant_figures.py` recreates them; it does not retrain models.

## Suggested order and 20-second explanation

### Figure 0 — `figure_0_data_and_split`

**Say:** “We used hourly ERA5 2-metre temperature from 2019 through 2025 over 5°–35°N and 65°–100°E. We split by year: 2019–2023 for training, 2024 for validation, and 2025 for test. Seven-day sliding windows yield 1,819, 359, and 358 input/target examples. The missing seven examples per year are the first seven days, because each target needs seven preceding days.”

**If asked:** A “daily map” is one 121 × 141 grid for a day. A “sequence” is seven daily input maps paired with the following target map. Windows are constructed separately inside each split.

### Figure 1 — `figure_1_actual_architecture`

**Say:** “The input is seven temperature maps. The code reorders the tensor and applies three 3D convolution layers with 32 intermediate channels, then takes the last temporal slice as tomorrow's map. It has 29,441 trainable parameters.”

**If asked:** "The proposed model has a legacy class name but is Conv3D with no recurrent state. We separately trained a one-layer ConvLSTM baseline with 32 hidden channels, recurrent gates, and a 1x1 output projection; it has 38,177 parameters. Its results are included in the updated comparison."

### Figure 2 — `figure_2_delhi_point_forecast`

**Say:** “This is the full 2025 next-day series at the grid cell nearest Delhi, 28.50°N and 77.25°E. The dark line is the ERA5 target, blue is the model forecast, and orange is persistence, which carries forward the previous day's value. The local RMSE and MAE are printed on the chart.”

**If asked:** This is one grid point and is an illustration; the headline scores aggregate all test dates and all grid points. The model forecasts one day ahead. This chart does not validate long-range forecasts or independent station data.

### Figure 3 — `figure_3_test_scatter_and_residuals`

**Say:** “Each hexagon groups test forecasts by observed and predicted temperature; brighter cells contain more grid-cell/date pairs. The dashed diagonal is perfect agreement. The residual histogram shows forecast minus target, so values right of zero are overpredictions and values left are underpredictions. The metrics use the same aligned 2025 test arrays.”

**If asked about the old correlation:** "The old R2=0.9720 and r=0.2477 cannot both come from the same aligned arrays under standard formulas. We cannot identify the cause because the source predictions and calculation code are unavailable. Current aligned Conv3D test values are R2=0.9828 and Pearson r=0.9914."

### Figure 4 — `figure_4_model_comparison_rmse`

**Say:** "This compares six methods on the same 358 test targets. Conv3D has RMSE 1.365 C, ConvLSTM 1.379 C, and persistence 1.403 C. The Conv3D-ConvLSTM difference is small in this single-seed run."

**If asked:** “This is a modest difference from one random seed and one test year; we did not establish statistical significance. I would describe it as a result from this experiment, not proof the model is universally better.” The vertical axis starts at zero so bar lengths are not visually exaggerated.

### Figure 5 — `figure_5_window_and_seasonal_analysis`

**Say:** “The left panel changes the Conv3D input history from 3 to 7 to 14 days and evaluates on the same 351 dates. The dashed line is persistence on those dates. The right panel breaks the selected model's 358 test forecasts down by season. Error is highest in MAM and lowest in SON in this test year.”

**If asked:** The window differences are small and no significance test was run. Seasonal breakdown describes 2025 only, so it does not establish that the system is robust across years.

### Figure 6 — `figure_6_spatial_bias_and_rmse`

**Say:** “The left panel shows mean signed error at each grid cell: positive means overprediction, negative means underprediction. The right panel shows each cell's RMSE. These are computed across the 358 held-out forecasts; the circle marks the grid point used in Figure 2.”

**If asked:** “The map covers the full rectangular ERA5 grid and includes every grid cell, including ocean cells; it is not a land-only India mask and has no political borders. The analysis describes one test year, not general spatial robustness.”

## Keep these claims precise

- The holdout is temporally independent of model fitting/checkpoint selection, but the reference targets are ERA5 reanalysis, not independent station observations.
- The evaluation horizon is one day. Dashboard autoregressive forecasts beyond one day are outside the reported benchmark.
- The current verified training sequence count is 1,819. The old 1,089 number is from a legacy artifact with unrecoverable provenance and is not used.
- No missing value imputation was performed. Incomplete/non-finite hourly data were rejected and an invalid all-NaN intermediate file was excluded; the validation/test source equality audit is not complete.
- The contribution is the regional ERA5 pipeline and task-specific comparison/analysis, including a genuine ConvLSTM baseline; no new neural architecture is claimed.
- External numerical weather prediction and literature-score comparisons were not run under matched protocols.
