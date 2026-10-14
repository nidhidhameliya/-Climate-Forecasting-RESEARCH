# Climate forecasting research status

This document records the verified study setup, results, figure assets, and remaining limitations for the ERA5 next-day temperature forecasting project. It supersedes earlier draft audit statements in this file that described invalid normalization artifacts and preliminary smoke-run metrics.

## Study and data

- **Source:** ERA5 hourly 2 m air temperature (`t2m`) in Kelvin.
- **Study period:** 2019-01-01 00:00 through 2025-12-31 23:00 UTC.
- **Region:** 5 deg N to 35 deg N and 65 deg E to 100 deg E, inclusive.
- **Grid:** 121 x 141 at 0.25-degree spacing.
- **Daily target:** maximum of the 24 hourly values for each complete UTC day.
- **Forecast task:** use the preceding 7 daily temperature maps to forecast the next daily map.
- **Splits:** windows are built independently inside each year range to avoid crossing split boundaries.

| Split | Date range | Hourly records | Daily maps | 7-day input/target samples |
|---|---|---:|---:|---:|
| Train | 2019-01-01 to 2023-12-31 | 43,824 | 1,826 | 1,819 |
| Validation | 2024-01-01 to 2024-12-31 | 8,784 | 366 | 359 |
| Independent test | 2025-01-01 to 2025-12-31 | 8,760 | 365 | 358 |

A seven-day input window paired with the following day's target yields `number of daily maps - 7` examples per split. The often-cited 1,089 sample count belongs to an earlier, different split description; it is not the sequence count for these current 2019-2025 tensors.

## Quality control and normalization

The current preprocessing rejects non-finite values; it does not claim to reconstruct missing ERA5 values by interpolation or station-based correction. A daily target is formed only from a complete set of 24 hourly UTC observations. Train/source equality was checked. Validation and test date ranges, cadence, dimensions, and finite values were checked, but exact value-by-value equality of those arrays against the raw source has not been established. ERA5 is a reanalysis reference, not independent station truth.

Temperature is converted from Kelvin to Celsius. Normalization is a training-only z-score:

`z = (temperature_C - training_mean_C) / training_population_std_C`

The saved training statistics are mean 25.044549 C and population standard deviation 10.995944 C. The same statistics are applied to validation and test data; no statistics are fitted on either of those splits.

## Model and method

The proposed implementation is named `ConvLSTMModel` in code for compatibility, but it is **not a ConvLSTM**. It is a three-layer Conv3D encoder-decoder:

1. Input `(B, 7, 1, 121, 141)` is rearranged to `(B, 1, 7, 121, 141)`.
2. Encoder Conv3D: 1 to 32 channels, kernel 3 x 3 x 3, padding 1; ReLU.
3. Encoder Conv3D: 32 to 32 channels, kernel 3 x 3 x 3, padding 1; ReLU.
4. Decoder Conv3D: 32 to 1 channel, kernel 3 x 3 x 3, padding 1.
5. The final temporal index is returned as the next-day grid.

The model has 29,441 trainable parameters. There are no recurrent gates, hidden state, or cell state. The word `convlstm` in the config is a legacy model identifier and should not be used to characterize the implemented architecture.

The original five-method comparison used seed 42, batch size 16, Adam with learning rate 1e-4, and up to 50 epochs per learned model. A genuine ConvLSTM was subsequently trained with the same data split, seed, batch size, optimizer, loss and 50-epoch budget; its checkpoint was selected by validation loss. All learned checkpoints are validation-selected. Test metrics below are computed over the aligned independent 2025 targets; RMSE and MAE are in degrees C. R2 and Pearson correlation are distinct statistics.

| Method | Parameters | Best epoch | Test RMSE (C) | Test MAE (C) | Test R2 | Pearson r |
|---|---:|---:|---:|---:|---:|---:|
| Persistence | 0 | n/a | 1.402716 | 0.897498 | 0.981867 | 0.990937 |
| LSTM | 4,513 | 50 | 1.572731 | 1.016080 | 0.977206 | 0.988568 |
| CNN-LSTM | 18,049 | 48 | 1.400517 | 0.898668 | 0.981924 | 0.990928 |
| Conv3D encoder-decoder | 29,441 | 39 | 1.364915 | 0.874530 | 0.982832 | 0.991407 |
| Transformer | 275,105 | 36 | 1.403025 | 0.898712 | 0.981860 | 0.990936 |
| ConvLSTM baseline | 38,177 | 49 | 1.378530 | 0.882874 | 0.982487 | 0.991280 |

On the full 358-date 2025 test set, Conv3D RMSE is 1.364915 C and the ConvLSTM baseline RMSE is 1.378530 C (a 0.013615 C difference); persistence is 1.402716 C. These are single-seed results and the small Conv3D versus ConvLSTM difference is not significance-tested. The Conv3D result is a modest improvement over persistence in this single-seed, single-test-year comparison. It does not show that Conv3D is universally superior. The earlier reported pair R2 = 0.9720 and correlation = 0.2477 is not reproducible from preserved artifacts: the original predictions, target array, and metric-calculation code that produced r=0.2477 are unavailable. Therefore its specific cause cannot be established; possible causes such as misalignment, spatial aggregation, or a coding error are hypotheses only and must not be presented as fact. On the current aligned test arrays, the Conv3D metrics are R2 = 0.982832 and Pearson r = 0.991407.

### Input-window ablation

The following runs use the same 351 test dates (2025-01-15 through 2025-12-31), with a validation-selected checkpoint for each learned model. They are single-seed results and the small differences are not significance-tested.

| Input days | Best epoch | Test RMSE (C) | Test MAE (C) | Test R2 | Pearson r |
|---:|---:|---:|---:|---:|---:|
| Persistence | n/a | 1.395853 | 0.892756 | 0.981761 | 0.990882 |
| 3 | 48 | 1.367838 | 0.873910 | 0.982486 | 0.991278 |
| 7 | 41 | 1.361286 | 0.872670 | 0.982653 | 0.991375 |
| 14 | 40 | 1.358829 | 0.868374 | 0.982716 | 0.991394 |

## Figures

Visualization images are kept in PNG format only. Their generation scripts now write PNG files only.

- [`outputs/visualizations/`](outputs/visualizations/) contains verified test and validation diagnostics, example forecast maps, model comparison, window and seasonal errors, spatial errors, and training/validation histories. See the [visualization audit](outputs/visualizations/VISUALIZATION_AUDIT.md). Regenerate with `python outputs/visualizations/generate_verified_visualizations.py` from the repository root; the script runs inference and does not retrain the model.
- [`paper_figures/`](paper_figures/FIGURE_CAPTIONS.md) contains six manuscript figures with captions and provenance. Regenerate PNGs with `python paper_figures/generate_paper_figures.py`.
- [`paper_figures_explained/`](paper_figures_explained/HOW_TO_EXPLAIN.md) contains conference-oriented figures and plain-language speaking notes. Regenerate PNGs with `python paper_figures_explained/generate_relevant_figures.py`.

The test maps use ERA5 as the target reference and cover the full rectangular grid, including ocean cells. They do not show station validation or political boundaries. Training-set evaluation figures are omitted because a verified training evaluation output set was unavailable.

## Novelty and limits

The Conv3D layers themselves are established methods; this project should not claim a new neural architecture. Its contribution is an audited application-specific comparison of next-day ERA5 daily-maximum temperature maps over the stated region, with year-based splits, matched-date model comparisons, input-window ablation, and spatial/seasonal diagnostics. The current evidence is limited to one initialization and one held-out test year. No independent station observations, uncertainty intervals, repeated-seed significance tests, or operational numerical-weather-prediction comparison are available.

The new ConvLSTM baseline is a one-layer ConvLSTM: 32 hidden channels; a 3x3 convolution over concatenated input and hidden state produces four gate maps; sigmoid input, forget, and output gates and a tanh candidate update the cell and hidden states for each of the seven input days; a 1x1 Conv2d projects the final hidden state to the next-day temperature map. It has 38,177 trainable parameters. The original Figure 3 baseline implementation remains unverified; do not claim this new implementation is identical to that historical figure unless the figure/source is checked. The legacy `convlstm` identifier still maps to the Conv3D model.

## Future work and likely questions

- Compare predictions against independent station observations and operational forecast products.
- Repeat training across multiple seeds and years, report uncertainty, and test whether model differences are statistically meaningful.
- Trace validation and test values back to the raw ERA5 files and document any rejected or corrected records. Do not claim imputation unless a reproducible procedure and evidence are added.
- Reconcile the historical Figure 3 baseline with the newly implemented ConvLSTM; identify it as a new baseline until the original source is verified.
- Test additional atmospheric variables and forecast horizons with leakage-safe splits.
- Compare against additional suitable methods under aligned dates, inputs, tuning budgets, and metrics.
- Develop a defensible novelty claim through a broader literature comparison; the present contribution is the controlled evaluation and analysis, not a new Conv3D operator.

## Key artifacts

- [README.md](README.md): repository overview, dataset summary, and headline benchmark.
- [reviewer_questions_answers.md](reviewer_questions_answers.md): detailed answers to likely reviewer questions.
- [paper_figures_explained/HOW_TO_EXPLAIN.md](paper_figures_explained/HOW_TO_EXPLAIN.md): conference explanations and cross-question notes.
- [experiments/reviewer_final_20261014/](experiments/reviewer_final_20261014/): corrected checkpoints, comparison results, and analyses.
- [data/processed/mean_std.json](data/processed/mean_std.json): training-only normalization statistics.

## References

1. Hersbach, H. et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, 146, 1999-2049.
2. Shi, X. et al. (2015). Convolutional LSTM Network: A Machine Learning Approach for Precipitation Nowcasting. *Advances in Neural Information Processing Systems*.
