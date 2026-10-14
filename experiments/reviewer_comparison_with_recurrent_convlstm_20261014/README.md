# Six-method comparison

This table combines the original verified five-method comparison in `experiments/reviewer_final_20261014/comparison_results.csv` with the separately trained ConvLSTM baseline in `experiments/reviewer_recurrent_convlstm_20261014/comparison_results.csv`. Both runs used seed 42, batch size 16, Adam at 1e-4, the same chronological split, weighted loss and 50-epoch budget; learned checkpoints were selected on validation loss. All test metrics refer to the aligned independent 2025 dates. This is a single-seed comparison and the small differences are not significance-tested.
