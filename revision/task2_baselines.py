"""
Task 2 - Extra baselines.

Implements and evaluates (on the test set, de-normalized deg C):
  1. Climatology (per-pixel DOY mean from training, 29-Feb handled by interpolation)
  2. Seasonal-naive (same calendar date one year earlier = test 2025 -> 2024 val data)
  3. 7-day-mean persistence
  4. Ridge regression (per-pixel, sklearn, previous 7 days)
  5. 2D U-Net (7 input channels stacked)
  6. ConvLSTM (2 layers, 32 hidden, 3x3 kernels, seeds 0-4)

Writes: revision/results/table2_baselines.csv
"""

import os
import sys
import json
import csv
import time
from datetime import date

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.linear_model import Ridge

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from revision.utils import (
    load_split, load_norm_stats, denorm, compute_metrics, get_test_dates,
    get_train_dates, get_val_dates, set_seed, make_config,
    RESULTS_DIR, PREDS_DIR, NLAT, NLON,
)

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(PREDS_DIR, exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────────────
print("Loading data splits...")
train_X, train_y = load_split("train")   # (1819, 7, 1, 121, 141)
val_X, val_y = load_split("val")         # (359,  7, 1, 121, 141)
test_X, test_y = load_split("test")      # (358,  7, 1, 121, 141)

MEAN, STD = load_norm_stats()
print(f"  norm stats: mean={MEAN:.4f} C, std={STD:.4f} C")

# De-normalized ground truths
train_y_C = denorm(train_y[:, 0], MEAN, STD)   # (1819, 121, 141)
val_y_C = denorm(val_y[:, 0], MEAN, STD)        # (359,  121, 141)
test_y_C = denorm(test_y[:, 0], MEAN, STD)      # (358,  121, 141)

# Also extract X last-frame in Celsius for persistence
train_X_C = denorm(train_X[:, :, 0], MEAN, STD)  # (1819, 7, 121, 141)
val_X_C = denorm(val_X[:, :, 0], MEAN, STD)       # (359,  7, 121, 141)
test_X_C = denorm(test_X[:, :, 0], MEAN, STD)     # (358,  7, 121, 141)

train_dates = get_train_dates()  # list of 1819 dates (targets)
val_dates = get_val_dates()       # list of 359 dates
test_dates = get_test_dates()     # list of 358 dates

results = []  # will accumulate rows for CSV


# ── 1. Climatology ────────────────────────────────────────────────────────────
print("\n[1] Climatology baseline...")
# Build per-DOY mean from training targets
doy_sums = {}  # doy -> (sum_array, count)
for i, d in enumerate(train_dates):
    doy = d.timetuple().tm_yday
    if doy not in doy_sums:
        doy_sums[doy] = (np.zeros((NLAT, NLON), dtype=np.float64), 0)
    doy_sums[doy] = (doy_sums[doy][0] + train_y_C[i], doy_sums[doy][1] + 1)

doy_means = {doy: s / c for doy, (s, c) in doy_sums.items()}

# Handle 29 Feb: interpolate between DOY 59 and 61
if 60 not in doy_means:
    if 59 in doy_means and 61 in doy_means:
        doy_means[60] = 0.5 * (doy_means[59] + doy_means[61])
    elif 59 in doy_means:
        doy_means[60] = doy_means[59]
    else:
        doy_means[60] = np.zeros((NLAT, NLON), dtype=np.float64)

clim_preds = []
for d in test_dates:
    doy = d.timetuple().tm_yday
    clim_preds.append(doy_means.get(doy, np.zeros((NLAT, NLON))))
clim_preds = np.array(clim_preds)  # (358, 121, 141)

m = compute_metrics(clim_preds, test_y_C)
m["model"] = "Climatology"
m["params"] = "N/A"
results.append(m)
print(f"  Climatology: RMSE={m['RMSE']:.4f}, MAE={m['MAE']:.4f}, R2={m['R2']:.4f}, r={m['Corr']:.4f}")
np.save(os.path.join(PREDS_DIR, "clim_preds.npy"), clim_preds.astype(np.float32))


# ── 2. Seasonal-naive ─────────────────────────────────────────────────────────
print("\n[2] Seasonal-naive baseline (same date one year earlier)...")
# Test is 2025; same calendar date in 2024 is in val set (indexed by val_dates)
val_date_to_idx = {d: i for i, d in enumerate(val_dates)}
sn_preds = []
for d in test_dates:
    try:
        prev_date = date(2024, d.month, d.day)
    except ValueError:
        # Feb 29 2025 doesn't exist, use Feb 28
        prev_date = date(2024, 2, 28)
    idx = val_date_to_idx.get(prev_date)
    if idx is not None:
        sn_preds.append(val_y_C[idx])
    else:
        # Fallback to climatology
        doy = d.timetuple().tm_yday
        sn_preds.append(doy_means.get(doy, np.zeros((NLAT, NLON))))
sn_preds = np.array(sn_preds)

m = compute_metrics(sn_preds, test_y_C)
m["model"] = "Seasonal-naive"
m["params"] = "N/A"
results.append(m)
print(f"  Seasonal-naive: RMSE={m['RMSE']:.4f}, MAE={m['MAE']:.4f}, R2={m['R2']:.4f}, r={m['Corr']:.4f}")
np.save(os.path.join(PREDS_DIR, "seasonal_naive_preds.npy"), sn_preds.astype(np.float32))


# ── 3. 7-day-mean persistence ─────────────────────────────────────────────────
print("\n[3] 7-day-mean persistence baseline...")
persist_preds = test_X_C.mean(axis=1)  # (358, 121, 141)  mean of last 7 days

m = compute_metrics(persist_preds, test_y_C)
m["model"] = "Persistence (7-day mean)"
m["params"] = "N/A"
results.append(m)
print(f"  Persistence: RMSE={m['RMSE']:.4f}, MAE={m['MAE']:.4f}, R2={m['R2']:.4f}, r={m['Corr']:.4f}")
np.save(os.path.join(PREDS_DIR, "persist_preds.npy"), persist_preds.astype(np.float32))


# ── 4. Ridge regression (per-pixel) ──────────────────────────────────────────
print("\n[4] Ridge regression (per-pixel) baseline...")
# Flatten spatially: train on (N, 7) -> (1,) per pixel
# For efficiency, reshape to (pixels, samples) and fit in batch
# train_X_C: (1819, 7, 121, 141) -> (1819*121*141, 7)
N_train = train_X_C.shape[0]
N_test = test_X_C.shape[0]

# Reshape to (pixels, n_samples, 7)
X_tr = train_X_C.transpose(2, 3, 0, 1).reshape(NLAT * NLON, N_train, 7)  # (17061, 1819, 7)
y_tr = train_y_C.transpose(1, 2, 0).reshape(NLAT * NLON, N_train)         # (17061, 1819)
X_te = test_X_C.transpose(2, 3, 0, 1).reshape(NLAT * NLON, N_test, 7)    # (17061, 358, 7)

ridge_preds_flat = np.zeros((NLAT * NLON, N_test), dtype=np.float32)
ridge = Ridge(alpha=1.0)

t0 = time.time()
for px in range(NLAT * NLON):
    ridge.fit(X_tr[px], y_tr[px])
    ridge_preds_flat[px] = ridge.predict(X_te[px])
    if px % 5000 == 0:
        elapsed = time.time() - t0
        print(f"  Ridge: pixel {px}/{NLAT * NLON}, elapsed={elapsed:.0f}s")

ridge_preds = ridge_preds_flat.reshape(NLAT, NLON, N_test).transpose(2, 0, 1)  # (358, 121, 141)

m = compute_metrics(ridge_preds, test_y_C)
m["model"] = "Ridge Regression (per-pixel)"
m["params"] = f"{7 + 1} per pixel x {NLAT * NLON} = {8 * NLAT * NLON}"
results.append(m)
print(f"  Ridge: RMSE={m['RMSE']:.4f}, MAE={m['MAE']:.4f}, R2={m['R2']:.4f}, r={m['Corr']:.4f}")
np.save(os.path.join(PREDS_DIR, "ridge_preds.npy"), ridge_preds.astype(np.float32))


# ── 5. 2D U-Net ───────────────────────────────────────────────────────────────
print("\n[5] 2D U-Net baseline...")


class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1), nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1), nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.net(x)


class UNet2D(nn.Module):
    """Simple 2D U-Net. Input: (B, 7, H, W). Output: (B, 1, H, W)."""

    def __init__(self, in_channels=7, base=32):
        super().__init__()
        self.enc1 = DoubleConv(in_channels, base)
        self.pool1 = nn.MaxPool2d(2)
        self.enc2 = DoubleConv(base, base * 2)
        self.pool2 = nn.MaxPool2d(2)
        self.bottleneck = DoubleConv(base * 2, base * 4)
        self.up2 = nn.ConvTranspose2d(base * 4, base * 2, 2, stride=2)
        self.dec2 = DoubleConv(base * 4, base * 2)
        self.up1 = nn.ConvTranspose2d(base * 2, base, 2, stride=2)
        self.dec1 = DoubleConv(base * 2, base)
        self.out = nn.Conv2d(base, 1, 1)

    def forward(self, x):
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool1(e1))
        b = self.bottleneck(self.pool2(e2))
        d2 = self.dec2(torch.cat([self.up2(b), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        return self.out(d1)


def train_and_eval_seeded(ModelClass, model_kwargs, train_X_t, train_y_t,
                           test_X_t, test_y_C_np, epochs=50, batch_size=16,
                           lr=1e-3, seeds=(0, 1, 2, 3, 4), model_name="model"):
    """Train a model with multiple seeds, return mean+std metrics and predictions."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    all_metrics = []
    all_preds = []

    for seed in seeds:
        set_seed(seed)
        model = ModelClass(**model_kwargs).to(device)
        opt = torch.optim.Adam(model.parameters(), lr=lr)
        loss_fn = nn.MSELoss()

        ds = TensorDataset(train_X_t, train_y_t)
        loader = DataLoader(ds, batch_size=batch_size, shuffle=True)

        model.train()
        for ep in range(epochs):
            for xb, yb in loader:
                xb, yb = xb.to(device), yb.to(device)
                opt.zero_grad()
                loss_fn(model(xb), yb).backward()
                opt.step()
            if (ep + 1) % 10 == 0:
                print(f"    [{model_name}] seed={seed} epoch {ep+1}/{epochs}")

        # Eval
        model.eval()
        preds_norm = []
        with torch.no_grad():
            for i in range(0, len(test_X_t), batch_size):
                xb = test_X_t[i:i + batch_size].to(device)
                preds_norm.append(model(xb).cpu().numpy())
        preds_norm = np.concatenate(preds_norm, axis=0)[:, 0]  # (N, H, W)
        preds_C = denorm(preds_norm, MEAN, STD)
        m = compute_metrics(preds_C, test_y_C_np)
        m["seed"] = seed
        all_metrics.append(m)
        all_preds.append(preds_C)

        # Save per-seed prediction
        np.save(os.path.join(PREDS_DIR, f"{model_name}_seed{seed}_preds.npy"),
                preds_C.astype(np.float32))

    return all_metrics, np.stack(all_preds, axis=0)


# Build tensors for U-Net (7 channels = 7 input days)
# train_X:  (1819, 7, 1, 121, 141) -> (1819, 7, 121, 141)
unet_train_X = torch.tensor(train_X[:, :, 0], dtype=torch.float32)  # (1819, 7, 121, 141)
unet_train_y = torch.tensor(train_y[:, 0:1], dtype=torch.float32)   # (1819, 1, 121, 141)
unet_test_X = torch.tensor(test_X[:, :, 0], dtype=torch.float32)    # (358,  7, 121, 141)

unet_metrics, unet_preds_all = train_and_eval_seeded(
    UNet2D, {"in_channels": 7, "base": 32},
    unet_train_X, unet_train_y, unet_test_X, test_y_C,
    epochs=50, batch_size=16, lr=1e-3, model_name="unet2d"
)

unet_rmse_mean = np.mean([m["RMSE"] for m in unet_metrics])
unet_rmse_std = np.std([m["RMSE"] for m in unet_metrics])
unet_mae_mean = np.mean([m["MAE"] for m in unet_metrics])
unet_mae_std = np.std([m["MAE"] for m in unet_metrics])
unet_r2 = np.mean([m["R2"] for m in unet_metrics])
unet_corr = np.mean([m["Corr"] for m in unet_metrics])

dummy_unet = UNet2D(in_channels=7, base=32)
unet_params = sum(p.numel() for p in dummy_unet.parameters() if p.requires_grad)

m_row = {
    "model": "2D U-Net",
    "params": unet_params,
    "RMSE": f"{unet_rmse_mean:.4f}",
    "RMSE_std": f"{unet_rmse_std:.4f}",
    "MAE": f"{unet_mae_mean:.4f}",
    "MAE_std": f"{unet_mae_std:.4f}",
    "R2": f"{unet_r2:.4f}",
    "Corr": f"{unet_corr:.4f}",
}
results.append(m_row)
print(f"  U-Net: RMSE={unet_rmse_mean:.4f}+/-{unet_rmse_std:.4f}")


# ── 6. ConvLSTM (proper, 2 layers, 32 hidden, 3x3) ───────────────────────────
print("\n[6] ConvLSTM (2 layers, 32 hidden, 3x3) baseline...")


class ConvLSTMCell(nn.Module):
    def __init__(self, in_channels, hidden_channels, kernel_size=3):
        super().__init__()
        pad = kernel_size // 2
        self.hidden_channels = hidden_channels
        self.conv = nn.Conv2d(
            in_channels + hidden_channels,
            4 * hidden_channels,
            kernel_size,
            padding=pad,
        )

    def forward(self, x, h, c):
        combined = torch.cat([x, h], dim=1)
        gates = self.conv(combined)
        i, f, g, o = gates.chunk(4, dim=1)
        i, f, o = torch.sigmoid(i), torch.sigmoid(f), torch.sigmoid(o)
        g = torch.tanh(g)
        c_next = f * c + i * g
        h_next = o * torch.tanh(c_next)
        return h_next, c_next


class ConvLSTM2Layer(nn.Module):
    """2-layer ConvLSTM -> 1x1 conv output. Input: (B, T, 1, H, W)."""

    def __init__(self, hidden=32, kernel=3):
        super().__init__()
        self.cell1 = ConvLSTMCell(1, hidden, kernel)
        self.cell2 = ConvLSTMCell(hidden, hidden, kernel)
        self.out = nn.Conv2d(hidden, 1, 1)
        self.hidden = hidden

    def forward(self, x):
        B, T, C, H, W = x.shape
        h1 = torch.zeros(B, self.hidden, H, W, device=x.device)
        c1 = torch.zeros_like(h1)
        h2 = torch.zeros(B, self.hidden, H, W, device=x.device)
        c2 = torch.zeros_like(h2)
        for t in range(T):
            h1, c1 = self.cell1(x[:, t], h1, c1)
            h2, c2 = self.cell2(h1, h2, c2)
        return self.out(h2)


# Build tensors for ConvLSTM: (B, T, 1, H, W)
clstm_train_X = torch.tensor(train_X, dtype=torch.float32)  # (1819, 7, 1, 121, 141)
clstm_train_y = torch.tensor(train_y, dtype=torch.float32)  # (1819, 1, 121, 141)
clstm_test_X = torch.tensor(test_X, dtype=torch.float32)     # (358,  7, 1, 121, 141)

clstm_metrics, clstm_preds_all = train_and_eval_seeded(
    ConvLSTM2Layer, {"hidden": 32, "kernel": 3},
    clstm_train_X, clstm_train_y, clstm_test_X, test_y_C,
    epochs=50, batch_size=16, lr=1e-3, model_name="convlstm2"
)

clstm_rmse_mean = np.mean([m["RMSE"] for m in clstm_metrics])
clstm_rmse_std = np.std([m["RMSE"] for m in clstm_metrics])
clstm_mae_mean = np.mean([m["MAE"] for m in clstm_metrics])
clstm_mae_std = np.std([m["MAE"] for m in clstm_metrics])
clstm_r2 = np.mean([m["R2"] for m in clstm_metrics])
clstm_corr = np.mean([m["Corr"] for m in clstm_metrics])

dummy_clstm = ConvLSTM2Layer(hidden=32, kernel=3)
clstm_params = sum(p.numel() for p in dummy_clstm.parameters() if p.requires_grad)

m_row = {
    "model": "ConvLSTM (2-layer)",
    "params": clstm_params,
    "RMSE": f"{clstm_rmse_mean:.4f}",
    "RMSE_std": f"{clstm_rmse_std:.4f}",
    "MAE": f"{clstm_mae_mean:.4f}",
    "MAE_std": f"{clstm_mae_std:.4f}",
    "R2": f"{clstm_r2:.4f}",
    "Corr": f"{clstm_corr:.4f}",
}
results.append(m_row)
print(f"  ConvLSTM: RMSE={clstm_rmse_mean:.4f}+/-{clstm_rmse_std:.4f}")


# ── Write CSV ─────────────────────────────────────────────────────────────────
csv_path = os.path.join(RESULTS_DIR, "table2_baselines.csv")
fieldnames = ["model", "params", "RMSE", "RMSE_std", "MAE", "MAE_std", "R2", "Corr"]
with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        # Normalise: non-seeded models store floats, seeded store strings already
        out = {}
        for k in fieldnames:
            v = row.get(k, "")
            if isinstance(v, float):
                out[k] = f"{v:.4f}"
            else:
                out[k] = v
        writer.writerow(out)

print(f"\nSaved -> {csv_path}")
print("\nTask 2 complete.")
