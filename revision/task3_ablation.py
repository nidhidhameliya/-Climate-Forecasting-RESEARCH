"""
Task 3 - Ablation study.

Varies one factor at a time while keeping others at default:
  - Window length k in {1, 3, 5, 7, 14, 21}
  - Channels in {16, 32, 64}
  - Encoder depth in {1, 2, 3}
  - Kernel size: (3,3,3) vs (3,5,5)

For each configuration: train with seeds 0-4, report mean+/-std RMSE, MAE.
Writes: revision/results/table3_ablation.csv
"""

import os
import sys
import json
import csv

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from revision.utils import (
    load_split, load_norm_stats, denorm, compute_metrics, get_test_dates,
    set_seed, RESULTS_DIR, PREDS_DIR, NLAT, NLON,
)

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(PREDS_DIR, exist_ok=True)

MEAN, STD = load_norm_stats()

SEEDS = [0, 1, 2, 3, 4]
EPOCHS = 50
BATCH = 16
LR = 1e-3
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ── Helper: create sequences from a normalized split array ───────────────────
def create_sequences(arr, seq_len):
    """arr: (N_days, H, W) normalized. Returns X (N, k, 1, H, W), y (N, 1, H, W)."""
    X, y = [], []
    for i in range(len(arr) - seq_len):
        X.append(arr[i:i + seq_len])
        y.append(arr[i + seq_len])
    X = np.array(X)[:, :, np.newaxis]  # (N, k, 1, H, W)
    y = np.array(y)[:, np.newaxis]    # (N, 1, H, W)
    return X, y


# Load raw normalized daily arrays (before sequencing)
def load_daily(split):
    return np.load(os.path.join(PROJECT_ROOT, "data", "processed", f"{split}.npy"))  # (N_days, H, W)


train_daily = load_daily("train")  # (1826, 121, 141)
val_daily = load_daily("val")      # (366, 121, 141)
test_daily = load_daily("test")    # (365, 121, 141)

print(f"Daily shapes: train={train_daily.shape}, val={val_daily.shape}, test={test_daily.shape}")


# ── Flexible Conv3D model ─────────────────────────────────────────────────────
class FlexConv3D(nn.Module):
    """
    Flexible Conv3D encoder-decoder.
    - n_channels: hidden feature channels
    - depth: number of Conv3D layers in encoder (1, 2, or 3)
    - kernel: tuple e.g. (3,3,3) or (3,5,5)
    """

    def __init__(self, n_channels=32, depth=2, kernel=(3, 3, 3)):
        super().__init__()
        pad = tuple(k // 2 for k in kernel)
        enc_layers = []
        in_ch = 1
        for _ in range(depth):
            enc_layers += [
                nn.Conv3d(in_ch, n_channels, kernel_size=kernel, padding=pad),
                nn.ReLU(inplace=True),
            ]
            in_ch = n_channels
        self.encoder = nn.Sequential(*enc_layers)
        self.decoder = nn.Conv3d(n_channels, 1, kernel_size=kernel, padding=pad)

    def forward(self, x):
        # x: (B, T, 1, H, W) -> permute to (B, 1, T, H, W)
        x = x.permute(0, 2, 1, 3, 4)
        features = self.encoder(x)
        out = self.decoder(features)
        return out[:, :, -1, :, :]  # (B, 1, H, W)


def count_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def train_eval(model, train_X_t, train_y_t, test_X_t, test_y_C_np):
    """Train model and return predictions in deg C."""
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.MSELoss()
    ds = TensorDataset(train_X_t, train_y_t)
    loader = DataLoader(ds, batch_size=BATCH, shuffle=True)

    model.train()
    for ep in range(EPOCHS):
        for xb, yb in loader:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            opt.zero_grad()
            loss_fn(model(xb), yb).backward()
            opt.step()

    model.eval()
    preds_norm = []
    with torch.no_grad():
        for i in range(0, len(test_X_t), BATCH):
            xb = test_X_t[i:i + BATCH].to(DEVICE)
            preds_norm.append(model(xb).cpu().numpy())
    preds_norm = np.concatenate(preds_norm, axis=0)[:, 0]  # (N, H, W)
    return denorm(preds_norm, MEAN, STD)


def run_ablation(factor, value, n_channels, depth, kernel, seq_len):
    """Run 5-seed experiment for one configuration. Returns dict for CSV."""
    # Build sequences with this seq_len
    tr_X, tr_y = create_sequences(train_daily, seq_len)
    te_X, te_y = create_sequences(test_daily, seq_len)
    n_test = te_X.shape[0]

    te_y_C = denorm(te_y[:, 0], MEAN, STD)

    train_X_t = torch.tensor(tr_X, dtype=torch.float32)
    train_y_t = torch.tensor(tr_y, dtype=torch.float32)
    test_X_t = torch.tensor(te_X, dtype=torch.float32)

    all_rmse, all_mae = [], []
    for seed in SEEDS:
        set_seed(seed)
        model = FlexConv3D(n_channels=n_channels, depth=depth, kernel=kernel).to(DEVICE)
        preds_C = train_eval(model, train_X_t, train_y_t, test_X_t, te_y_C)
        m = compute_metrics(preds_C, te_y_C)
        all_rmse.append(m["RMSE"])
        all_mae.append(m["MAE"])

    n_params = count_params(FlexConv3D(n_channels=n_channels, depth=depth, kernel=kernel))
    rmse_m = np.mean(all_rmse)
    rmse_s = np.std(all_rmse)
    mae_m = np.mean(all_mae)
    mae_s = np.std(all_mae)

    row = {
        "factor": factor,
        "value": str(value),
        "n_channels": n_channels,
        "depth": depth,
        "kernel": str(kernel),
        "seq_len": seq_len,
        "parameters": n_params,
        "n_test": n_test,
        "RMSE_mean": f"{rmse_m:.4f}",
        "RMSE_std": f"{rmse_s:.4f}",
        "MAE_mean": f"{mae_m:.4f}",
        "MAE_std": f"{mae_s:.4f}",
    }
    print(f"  [{factor}={value}] k={seq_len}, ch={n_channels}, depth={depth}, "
          f"kernel={kernel}, n_test={n_test}, params={n_params:,}, "
          f"RMSE={rmse_m:.4f}+/-{rmse_s:.4f}")
    return row


rows = []

# ── Window length ablation ─────────────────────────────────────────────────────
print("\n=== Window length ablation ===")
for k in [1, 3, 5, 7, 14, 21]:
    row = run_ablation("window_k", k, n_channels=32, depth=2, kernel=(3, 3, 3), seq_len=k)
    rows.append(row)

# ── Channel ablation ───────────────────────────────────────────────────────────
print("\n=== Channel ablation ===")
for ch in [16, 32, 64]:
    if ch == 32:
        # Already done in window_k=7
        row = run_ablation("channels", ch, n_channels=ch, depth=2, kernel=(3, 3, 3), seq_len=7)
    else:
        row = run_ablation("channels", ch, n_channels=ch, depth=2, kernel=(3, 3, 3), seq_len=7)
    row["factor"] = "channels"
    rows.append(row)

# ── Depth ablation ─────────────────────────────────────────────────────────────
print("\n=== Depth ablation ===")
for depth in [1, 2, 3]:
    row = run_ablation("depth", depth, n_channels=32, depth=depth, kernel=(3, 3, 3), seq_len=7)
    rows.append(row)

# ── Kernel ablation ────────────────────────────────────────────────────────────
print("\n=== Kernel ablation ===")
for kernel in [(3, 3, 3), (3, 5, 5)]:
    row = run_ablation("kernel", str(kernel), n_channels=32, depth=2, kernel=kernel, seq_len=7)
    rows.append(row)

# ── Write CSV ─────────────────────────────────────────────────────────────────
csv_path = os.path.join(RESULTS_DIR, "table3_ablation.csv")
fieldnames = ["factor", "value", "n_channels", "depth", "kernel", "seq_len",
              "parameters", "n_test", "RMSE_mean", "RMSE_std", "MAE_mean", "MAE_std"]
with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"\nSaved -> {csv_path}")
print("Task 3 complete.")
