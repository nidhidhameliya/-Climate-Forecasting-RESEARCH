import torch
import torch.nn as nn
import json
import math


class ExtremeWeightedMSE(nn.Module):
    def __init__(
        self,
        threshold_path="data/processed/extreme_thresholds.json",
        stats_path="data/processed/mean_std.json",
        extreme_weight=5.0,
    ):
        super(ExtremeWeightedMSE, self).__init__()

        with open(threshold_path, "r", encoding="utf-8") as f:
            thresholds = json.load(f)
        with open(stats_path, "r", encoding="utf-8") as f:
            stats = json.load(f)

        threshold_celsius = float(thresholds["top_5_percent_celsius"])
        mean = float(stats["mean"])
        std = float(stats["std"])
        if not all(math.isfinite(value) for value in (threshold_celsius, mean, std)) or std <= 0:
            raise ValueError("Extreme threshold and normalization stats must be finite; std must be positive")
        if stats.get("unit") != "degrees_Celsius":
            raise ValueError(f"Expected Celsius normalization stats, got {stats.get('unit')!r}")

        # The target tensors are z-scored Celsius. Convert the training-only
        # Celsius quantile to this same normalized space.
        self.threshold = (threshold_celsius - mean) / std
        self.extreme_weight = float(extreme_weight)

    def forward(self, preds, targets):

        extreme_mask = (targets > self.threshold).float()
        weights = 1.0 + self.extreme_weight * extreme_mask

        loss = weights * (preds - targets) ** 2

        return torch.mean(loss)


# ✅ This is what train.py expects
def get_loss(config=None):
    """
    Returns the loss function.
    Uses ExtremeWeightedMSE by default.
    """

    extreme_weight = 5.0

    if config is not None and "extreme_weight" in config:
        extreme_weight = config["extreme_weight"]

    return ExtremeWeightedMSE(extreme_weight=extreme_weight)
