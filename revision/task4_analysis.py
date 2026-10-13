"""
Task 4 - Spatial, seasonal and extreme-value error analysis.

Uses the proposed model's predictions (run via task2's seeded framework),
persistence (7-day-mean), and climatology.

Generates:
  - revision/results/table4_seasonal.csv
  - revision/results/table5_regional.csv
  - revision/results/table5_extremes.csv
  - revision/figures/  (RMSE maps, bias maps, lat/lon profiles, seasonal line plot)
"""

import os
import sys
import json
import csv

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from revision.utils import (
    load_split, load_norm_stats, denorm, compute_metrics, get_test_dates,
    get_train_dates, set_seed, RESULTS_DIR, FIGURES_DIR, PREDS_DIR, NLAT, NLON,
    LATS, LONS,
)

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

MEAN, STD = load_norm_stats()

# ── Load ground truth ─────────────────────────────────────────────────────────
train_X, train_y = load_split("train")
test_X, test_y = load_split("test")

test_y_C = denorm(test_y[:, 0], MEAN, STD)      # (358, 121, 141)
test_X_C = denorm(test_X[:, :, 0], MEAN, STD)    # (358, 7, 121, 141)
train_y_C = denorm(train_y[:, 0], MEAN, STD)     # (1819, 121, 141)

test_dates = get_test_dates()  # list of 358 date objects
train_dates = get_train_dates()  # 1819 dates

# ── Load or compute model predictions ─────────────────────────────────────────
print("Loading model predictions...")

# Try to load from saved predictions (task2/task3 should have saved them)
proposed_preds_path = os.path.join(PREDS_DIR, "proposed_model_mean_preds.npy")
if os.path.exists(proposed_preds_path):
    proposed_preds_C = np.load(proposed_preds_path)
    print(f"  Loaded proposed model predictions from {proposed_preds_path}")
else:
    # Generate using the trained Conv3D model
    print("  Running inference with trained Conv3D model (experiments/latest/model.pth)...")
    import yaml
    import torch
    from models.convlstm import ConvLSTMModel

    with open(os.path.join(PROJECT_ROOT, "config.yaml")) as f:
        cfg = yaml.safe_load(f)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ConvLSTMModel(cfg)
    model_path = os.path.join(PROJECT_ROOT, "experiments", "latest", "model.pth")
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    test_X_t = torch.tensor(test_X, dtype=torch.float32)
    preds_norm = []
    with torch.no_grad():
        for i in range(0, len(test_X_t), 16):
            xb = test_X_t[i:i + 16].to(device)
            preds_norm.append(model(xb).cpu().numpy())
    preds_norm = np.concatenate(preds_norm, axis=0)[:, 0]  # (358, 121, 141)
    proposed_preds_C = denorm(preds_norm, MEAN, STD)
    np.save(proposed_preds_path, proposed_preds_C.astype(np.float32))

# Persistence predictions
persist_path = os.path.join(PREDS_DIR, "persist_preds.npy")
if os.path.exists(persist_path):
    persist_preds_C = np.load(persist_path)
else:
    persist_preds_C = test_X_C.mean(axis=1)  # (358, 121, 141)
    np.save(persist_path, persist_preds_C.astype(np.float32))

# Climatology predictions
clim_path = os.path.join(PREDS_DIR, "clim_preds.npy")
if os.path.exists(clim_path):
    clim_preds_C = np.load(clim_path)
else:
    # Build climatology
    doy_sums = {}
    for i, d in enumerate(train_dates):
        doy = d.timetuple().tm_yday
        if doy not in doy_sums:
            doy_sums[doy] = (np.zeros((NLAT, NLON), dtype=np.float64), 0)
        doy_sums[doy] = (doy_sums[doy][0] + train_y_C[i], doy_sums[doy][1] + 1)
    doy_means = {doy: s / c for doy, (s, c) in doy_sums.items()}
    if 60 not in doy_means:
        doy_means[60] = 0.5 * (doy_means.get(59, doy_means.get(61, np.zeros((NLAT, NLON)))) +
                                doy_means.get(61, doy_means.get(59, np.zeros((NLAT, NLON)))))
    clim_preds_C = np.array([doy_means.get(d.timetuple().tm_yday, np.zeros((NLAT, NLON)))
                              for d in test_dates])
    np.save(clim_path, clim_preds_C.astype(np.float32))

print(f"  proposed_preds_C shape: {proposed_preds_C.shape}")
print(f"  persist_preds_C shape:  {persist_preds_C.shape}")
print(f"  clim_preds_C shape:     {clim_preds_C.shape}")


# ── Seasonal helpers ──────────────────────────────────────────────────────────
def get_season(d):
    m = d.month
    if m in (12, 1, 2):
        return "DJF"
    elif m in (3, 4, 5):
        return "MAM"
    elif m in (6, 7, 8, 9):
        return "JJAS"
    else:  # 10, 11
        return "ON"


def get_month(d):
    return d.strftime("%b")


SEASONS = ["DJF", "MAM", "JJAS", "ON"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

test_seasons = [get_season(d) for d in test_dates]
test_months = [d.month for d in test_dates]


def seasonal_metrics(preds, true, dates):
    """Returns dict: season -> {RMSE, MAE, count}"""
    out = {}
    seasons = [get_season(d) for d in dates]
    for s in SEASONS:
        idx = [i for i, ss in enumerate(seasons) if ss == s]
        if not idx:
            out[s] = {"RMSE": float("nan"), "MAE": float("nan"), "count": 0}
            continue
        m = compute_metrics(preds[idx], true[idx])
        m["count"] = len(idx)
        out[s] = m
    return out


def monthly_metrics(preds, true, dates):
    out = {}
    months = [d.month for d in dates]
    for mo in range(1, 13):
        idx = [i for i, mm in enumerate(months) if mm == mo]
        if not idx:
            out[mo] = {"RMSE": float("nan"), "MAE": float("nan"), "count": 0}
            continue
        m = compute_metrics(preds[idx], true[idx])
        m["count"] = len(idx)
        out[mo] = m
    return out


# ── Table 4: seasonal metrics ─────────────────────────────────────────────────
print("\n[T4a] Computing seasonal RMSE/MAE...")
seas_proposed = seasonal_metrics(proposed_preds_C, test_y_C, test_dates)
seas_persist = seasonal_metrics(persist_preds_C, test_y_C, test_dates)
seas_clim = seasonal_metrics(clim_preds_C, test_y_C, test_dates)

# Monthly for line plot
mon_proposed = monthly_metrics(proposed_preds_C, test_y_C, test_dates)
mon_persist = monthly_metrics(persist_preds_C, test_y_C, test_dates)
mon_clim = monthly_metrics(clim_preds_C, test_y_C, test_dates)

# Seasonal skill scores
def skill(rmse_model, rmse_ref):
    if rmse_ref == 0:
        return float("nan")
    return 1.0 - rmse_model / rmse_ref

# Write Table 4 CSV (seasonal)
csv4_path = os.path.join(RESULTS_DIR, "table4_seasonal.csv")
with open(csv4_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Season", "N_days",
                "RMSE_Conv3D", "MAE_Conv3D",
                "RMSE_Persist", "MAE_Persist", "Skill_vs_Persist",
                "RMSE_Clim", "MAE_Clim", "Skill_vs_Clim"])
    for s in SEASONS:
        sp = seas_proposed.get(s, {})
        sr = seas_persist.get(s, {})
        sc = seas_clim.get(s, {})
        sk_p = skill(sp.get("RMSE", float("nan")), sr.get("RMSE", float("nan")))
        sk_c = skill(sp.get("RMSE", float("nan")), sc.get("RMSE", float("nan")))
        w.writerow([
            s, sp.get("count", 0),
            f"{sp.get('RMSE', float('nan')):.4f}", f"{sp.get('MAE', float('nan')):.4f}",
            f"{sr.get('RMSE', float('nan')):.4f}", f"{sr.get('MAE', float('nan')):.4f}",
            f"{sk_p:.4f}",
            f"{sc.get('RMSE', float('nan')):.4f}", f"{sc.get('MAE', float('nan')):.4f}",
            f"{sk_c:.4f}",
        ])
print(f"  Saved -> {csv4_path}")

# Monthly line plot
fig, ax = plt.subplots(figsize=(11, 5))
mo_rmse_prop = [mon_proposed.get(m, {}).get("RMSE", float("nan")) for m in range(1, 13)]
mo_rmse_per = [mon_persist.get(m, {}).get("RMSE", float("nan")) for m in range(1, 13)]
mo_rmse_clim = [mon_clim.get(m, {}).get("RMSE", float("nan")) for m in range(1, 13)]
x = list(range(1, 13))
ax.plot(x, mo_rmse_prop, "b-o", label="Conv3D (proposed)", linewidth=2)
ax.plot(x, mo_rmse_per, "r--s", label="Persistence (7-day mean)", linewidth=2)
ax.plot(x, mo_rmse_clim, "g-.^", label="Climatology", linewidth=2)
ax.set_xticks(x)
ax.set_xticklabels(MONTHS)
ax.set_xlabel("Month (2025 test year)")
ax.set_ylabel("RMSE (°C)")
ax.set_title("Monthly RMSE on Test Set (2025) — Conv3D vs Baselines")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "fig_monthly_rmse.png"), dpi=150)
plt.close()
print(f"  Saved fig_monthly_rmse.png")


# ── Spatial error maps ────────────────────────────────────────────────────────
print("\n[T4b] Computing spatial RMSE and bias maps...")

# Time-averaged RMSE per pixel: (NLAT, NLON)
diff_prop = proposed_preds_C - test_y_C   # (358, 121, 141)
diff_per = persist_preds_C - test_y_C
diff_clim = clim_preds_C - test_y_C

rmse_map_prop = np.sqrt(np.mean(diff_prop ** 2, axis=0))   # (121, 141)
bias_map_prop = np.mean(diff_prop, axis=0)

rmse_map_per = np.sqrt(np.mean(diff_per ** 2, axis=0))
bias_map_per = np.mean(diff_per, axis=0)

rmse_map_clim = np.sqrt(np.mean(diff_clim ** 2, axis=0))
bias_map_clim = np.mean(diff_clim, axis=0)


def plot_map(data, title, fname, cmap="RdYlBu_r", vmin=None, vmax=None, cbar_label="°C"):
    fig, ax = plt.subplots(figsize=(9, 6))
    im = ax.imshow(data, extent=[LON_MIN, LON_MAX, LAT_MIN, LAT_MAX],
                   origin="upper", cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    plt.colorbar(im, ax=ax, label=cbar_label, shrink=0.8)
    ax.set_title(title)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, fname), dpi=150)
    plt.close()


vmax_rmse = max(np.nanmax(rmse_map_prop), np.nanmax(rmse_map_per))
plot_map(rmse_map_prop, "Conv3D: Time-avg RMSE (°C) — Test 2025",
         "fig_rmse_map_conv3d.png", cmap="YlOrRd", vmin=0, vmax=vmax_rmse, cbar_label="RMSE (°C)")
plot_map(bias_map_prop, "Conv3D: Mean Bias (°C) — Test 2025",
         "fig_bias_map_conv3d.png", cmap="RdBu_r", cbar_label="Bias (°C)")
plot_map(rmse_map_per, "Persistence: Time-avg RMSE (°C) — Test 2025",
         "fig_rmse_map_persist.png", cmap="YlOrRd", vmin=0, vmax=vmax_rmse, cbar_label="RMSE (°C)")
plot_map(rmse_map_clim, "Climatology: Time-avg RMSE (°C) — Test 2025",
         "fig_rmse_map_clim.png", cmap="YlOrRd", vmin=0, vmax=vmax_rmse, cbar_label="RMSE (°C)")
print("  Saved spatial RMSE and bias maps")


# ── RMSE by latitude and longitude ────────────────────────────────────────────
print("\n[T4c] RMSE profiles by lat and lon...")
rmse_by_lat_prop = np.sqrt(np.mean(diff_prop.reshape(358, NLAT, NLON) ** 2, axis=(0, 2)))  # (121,)
rmse_by_lon_prop = np.sqrt(np.mean(diff_prop.reshape(358, NLAT, NLON) ** 2, axis=(0, 1)))  # (141,)
rmse_by_lat_per = np.sqrt(np.mean(diff_per.reshape(358, NLAT, NLON) ** 2, axis=(0, 2)))
rmse_by_lon_per = np.sqrt(np.mean(diff_per.reshape(358, NLAT, NLON) ** 2, axis=(0, 1)))
rmse_by_lat_clim = np.sqrt(np.mean(diff_clim.reshape(358, NLAT, NLON) ** 2, axis=(0, 2)))
rmse_by_lon_clim = np.sqrt(np.mean(diff_clim.reshape(358, NLAT, NLON) ** 2, axis=(0, 1)))

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(rmse_by_lat_prop, LATS, "b-", label="Conv3D", linewidth=2)
axes[0].plot(rmse_by_lat_per, LATS, "r--", label="Persistence", linewidth=2)
axes[0].plot(rmse_by_lat_clim, LATS, "g-.", label="Climatology", linewidth=2)
axes[0].set_xlabel("RMSE (°C)")
axes[0].set_ylabel("Latitude (°N)")
axes[0].set_title("RMSE by Latitude")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(LONS, rmse_by_lon_prop, "b-", label="Conv3D", linewidth=2)
axes[1].plot(LONS, rmse_by_lon_per, "r--", label="Persistence", linewidth=2)
axes[1].plot(LONS, rmse_by_lon_clim, "g-.", label="Climatology", linewidth=2)
axes[1].set_xlabel("Longitude (°E)")
axes[1].set_ylabel("RMSE (°C)")
axes[1].set_title("RMSE by Longitude")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "fig_rmse_latlon.png"), dpi=150)
plt.close()
print("  Saved fig_rmse_latlon.png")


# ── Table 5: Regional breakdown ────────────────────────────────────────────────
print("\n[T5a] Regional breakdown...")

# Region masks defined by lat/lon boxes:
#   Himalaya  : lat 28-35N, lon 72-97E
#   IGP        : lat 22-30N, lon 73-88E
#   Deccan     : lat 12-22N, lon 74-82E
#   Ocean/Sea  : lat 5-15N, lon 65-80E (Arabian Sea + Bay of Bengal edges)
regions = {
    "Himalaya": {"lat": (28, 35), "lon": (72, 97)},
    "Indo-Gangetic Plain": {"lat": (22, 30), "lon": (73, 88)},
    "Deccan Plateau": {"lat": (12, 22), "lon": (74, 82)},
    "Ocean/Coastal": {"lat": (5, 15), "lon": (65, 80)},
}


def latlon_mask(lat_range, lon_range):
    lat_idx = np.where((LATS >= lat_range[0]) & (LATS <= lat_range[1]))[0]
    lon_idx = np.where((LONS >= lon_range[0]) & (LONS <= lon_range[1]))[0]
    return lat_idx, lon_idx


csv5r_path = os.path.join(RESULTS_DIR, "table5_regional.csv")
with open(csv5r_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Region", "Lat_box", "Lon_box", "N_pixels",
                "RMSE_Conv3D", "MAE_Conv3D",
                "RMSE_Persist", "RMSE_Clim"])
    for rname, rinfo in regions.items():
        li, loi = latlon_mask(rinfo["lat"], rinfo["lon"])
        if len(li) == 0 or len(loi) == 0:
            print(f"  WARNING: No pixels for region {rname}")
            continue
        # Extract subgrid
        prop_sub = proposed_preds_C[:, li[:, None], loi[None, :]]  # (358, n_lat, n_lon)
        per_sub = persist_preds_C[:, li[:, None], loi[None, :]]
        clim_sub = clim_preds_C[:, li[:, None], loi[None, :]]
        true_sub = test_y_C[:, li[:, None], loi[None, :]]
        n_px = len(li) * len(loi)
        mp = compute_metrics(prop_sub, true_sub)
        mr = compute_metrics(per_sub, true_sub)
        mc = compute_metrics(clim_sub, true_sub)
        w.writerow([
            rname,
            f"{rinfo['lat'][0]}-{rinfo['lat'][1]}N",
            f"{rinfo['lon'][0]}-{rinfo['lon'][1]}E",
            n_px,
            f"{mp['RMSE']:.4f}", f"{mp['MAE']:.4f}",
            f"{mr['RMSE']:.4f}", f"{mc['RMSE']:.4f}",
        ])
        print(f"  {rname}: RMSE_prop={mp['RMSE']:.4f}, RMSE_per={mr['RMSE']:.4f}, RMSE_clim={mc['RMSE']:.4f}")
print(f"  Saved -> {csv5r_path}")


# ── Table 5: Extremes ─────────────────────────────────────────────────────────
print("\n[T5b] Extreme-value error analysis...")

# Compute 95th and 5th percentiles from TRAINING temperatures (de-normalized)
train_flat = train_y_C.flatten()
p95 = float(np.percentile(train_flat, 95))
p5 = float(np.percentile(train_flat, 5))
print(f"  Training 95th pct={p95:.3f}C, 5th pct={p5:.3f}C")

# Pixel-day mask on test set
test_flat_true = test_y_C.flatten()
test_flat_prop = proposed_preds_C.flatten()
test_flat_per = persist_preds_C.flatten()
test_flat_clim = clim_preds_C.flatten()

mask_hot = test_flat_true > p95
mask_cold = test_flat_true < p5

def rmse_masked(pred, true, mask):
    if mask.sum() == 0:
        return float("nan"), float("nan"), 0
    d = pred[mask] - true[mask]
    return float(np.sqrt(np.mean(d ** 2))), float(np.mean(np.abs(d))), int(mask.sum())


def mae_masked(pred, true, mask):
    if mask.sum() == 0:
        return float("nan"), 0
    d = pred[mask] - true[mask]
    return float(np.mean(np.abs(d))), int(mask.sum())


csv5e_path = os.path.join(RESULTS_DIR, "table5_extremes.csv")
with open(csv5e_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Subset", "Threshold_C", "N_pixeldays",
                "RMSE_Conv3D", "RMSE_Persist", "RMSE_Clim",
                "MAE_Conv3D", "MAE_Persist", "MAE_Clim"])

    for label, mask, thr in [
        (f">p95 (hot, >{p95:.2f}C)", mask_hot, p95),
        (f"<p5 (cold, <{p5:.2f}C)", mask_cold, p5),
    ]:
        rmse_p, mae_p, n = rmse_masked(test_flat_prop, test_flat_true, mask)
        rmse_per, mae_per, _ = rmse_masked(test_flat_per, test_flat_true, mask)
        rmse_c, mae_c, _ = rmse_masked(test_flat_clim, test_flat_true, mask)
        w.writerow([label, f"{thr:.3f}", n,
                    f"{rmse_p:.4f}", f"{rmse_per:.4f}", f"{rmse_c:.4f}",
                    f"{mae_p:.4f}", f"{mae_per:.4f}", f"{mae_c:.4f}"])
        print(f"  {label}: N={n}, RMSE_prop={rmse_p:.4f}, RMSE_per={rmse_per:.4f}, RMSE_clim={rmse_c:.4f}")
print(f"  Saved -> {csv5e_path}")

print("\nTask 4 complete.")
