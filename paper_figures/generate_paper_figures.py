"""Generate paper figures from the verified 2026-10-14 experiment artifacts.

Run from the repository root with .venv/Scripts/python.exe (Windows) or
python (Linux/macOS). No model is retrained; the test prediction figures are
computed from the saved selected checkpoint and the saved 2025 test tensors.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
EXP = ROOT / "experiments" / "reviewer_final_20261014"
ABL = EXP / "window_ablation_final"
torch.set_num_threads(min(4, torch.get_num_threads()))

COLORS = {
    "navy": "#17324D", "blue": "#2878A5", "teal": "#4D9A87",
    "orange": "#E39138", "red": "#C65353", "purple": "#8064A2",
    "gray": "#6B7280", "light": "#E7EDF2",
}
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.titlesize": 10, "axes.labelsize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 8, "figure.dpi": 140,
    "savefig.dpi": 600, "axes.spines.top": False,
    "axes.spines.right": False, "axes.edgecolor": "#9AA8B4",
    "axes.linewidth": 0.7, "grid.color": "#D9E1E8",
    "grid.linewidth": 0.6,
})


def save(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUT / f"{stem}.png", bbox_inches="tight", facecolor="white", dpi=600)
    plt.close(fig)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def comparison_figure() -> None:
    rows = read_csv(EXP / "comparison_results.csv")
    names = ["Persistence" if r["model"] == "Persistence" else
             "Conv3D" if r["model"] == "convlstm" else r["model"].replace("_", "-").upper()
             for r in rows]
    colors = [COLORS["gray"], COLORS["blue"], COLORS["teal"], COLORS["orange"], COLORS["purple"]]
    metrics = [("test_rmse", "RMSE (°C)", (0, 1.75)),
               ("test_mae", "MAE (°C)", (0, 1.15)),
               ("test_r2", "R²", (0.965, 0.99))]
    fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.15))
    for ax, (key, title, ylim) in zip(axes, metrics):
        values = [float(r[key]) for r in rows]
        bars = ax.bar(np.arange(len(values)), values, color=colors, width=0.72, edgecolor="white", linewidth=0.5)
        ax.set_title(title, loc="left", fontweight="bold", color=COLORS["navy"])
        ax.set_xticks(np.arange(len(names)), names, rotation=30, ha="right")
        ax.set_ylim(*ylim)
        ax.grid(axis="y", alpha=0.8)
        ax.set_axisbelow(True)
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (ylim[1]-ylim[0])*0.018,
                    f"{value:.3f}", ha="center", va="bottom", fontsize=7.5)
    fig.suptitle("Held-out 2025 performance by forecasting method", x=0.02, ha="left",
                 fontsize=12, fontweight="bold", color=COLORS["navy"])
    fig.text(0.02, 0.005, "358 aligned test dates · lower is better for RMSE/MAE; higher is better for R² · R² panel: 0.965–0.990",
             fontsize=8, color=COLORS["gray"])
    fig.tight_layout(rect=(0, 0.07, 1, 0.90), w_pad=1.4)
    save(fig, "fig1_model_comparison")


def ablation_figure() -> None:
    rows = read_csv(ABL / "window_ablation_results.csv")
    persistence = {"rmse_celsius": 1.395853, "mae_celsius": 0.892756}
    xs = [int(r["window_days"]) for r in rows]
    metrics = [("rmse_celsius", "RMSE (°C)"), ("mae_celsius", "MAE (°C)")]
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.15))
    for ax, (key, title) in zip(axes, metrics):
        ys = [float(r[key]) for r in rows]
        base = persistence[key]
        ax.plot(xs, ys, color=COLORS["blue"], linewidth=2, marker="o", markersize=6,
                markerfacecolor="white", markeredgewidth=1.7, label="Conv3D")
        ax.axhline(base, color=COLORS["gray"], linestyle="--", linewidth=1.2, label="Persistence")
        for x, y in zip(xs, ys):
            ax.annotate(f"{y:.3f}", (x, y), xytext=(0, 8), textcoords="offset points",
                        ha="center", fontsize=8)
        ax.set_xticks(xs)
        ax.set_xlabel("Input window (past days)")
        ax.set_ylabel(title)
        ax.set_title(title, loc="left", fontweight="bold", color=COLORS["navy"])
        ax.grid(axis="y", alpha=0.8)
        ax.legend(frameon=False, loc="best")
    fig.suptitle("Input-window ablation on matched 2025 dates", x=0.02, ha="left",
                 fontsize=12, fontweight="bold", color=COLORS["navy"])
    fig.text(0.02, 0.005, "351 common targets · each checkpoint selected using validation loss",
             fontsize=8, color=COLORS["gray"])
    fig.tight_layout(rect=(0, 0.07, 1, 0.90), w_pad=2)
    save(fig, "fig2_input_window_ablation")


def seasonal_figure(error: dict) -> None:
    seasons = ["DJF", "MAM", "JJA", "SON"]
    seasonal = error["seasonal"]
    rmse = [seasonal[s]["rmse_celsius"] for s in seasons]
    mae = [seasonal[s]["mae_celsius"] for s in seasons]
    counts = [seasonal[s]["target_days"] for s in seasons]
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    x = np.arange(4)
    w = 0.34
    b1 = ax.bar(x-w/2, rmse, width=w, color=COLORS["blue"], label="RMSE")
    b2 = ax.bar(x+w/2, mae, width=w, color=COLORS["orange"], label="MAE")
    ax.set_xticks(x, [f"{s}\n(n={n})" for s, n in zip(seasons, counts)])
    ax.set_ylabel("Error (°C)")
    ax.set_title("Seasonal test error", loc="left", fontweight="bold", color=COLORS["navy"])
    ax.grid(axis="y", alpha=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncol=2, loc="upper right")
    for bars in (b1, b2):
        for bar in bars:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.025,
                    f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=8)
    fig.text(0.02, 0.01, "Conv3D selected checkpoint · held-out 2025 forecast targets",
             fontsize=8, color=COLORS["gray"])
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    save(fig, "fig3_seasonal_errors")


class Conv3DModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv3d(1, 32, (3, 3, 3), padding=1), nn.ReLU(),
            nn.Conv3d(32, 32, (3, 3, 3), padding=1), nn.ReLU(),
        )
        self.decoder = nn.Conv3d(32, 1, (3, 3, 3), padding=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.permute(0, 2, 1, 3, 4)
        return self.decoder(self.encoder(x))[:, :, -1, :, :]


def get_test_outputs() -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float]:
    stats = json.loads((ROOT / "data" / "processed" / "mean_std.json").read_text(encoding="utf-8"))
    mean, std = float(stats["mean"]), float(stats["std"])
    x = np.load(ROOT / "data" / "processed" / "tensors" / "test_X.npy", mmap_mode="r")
    y = np.load(ROOT / "data" / "processed" / "tensors" / "test_y.npy", mmap_mode="r")
    model = Conv3DModel()
    model.load_state_dict(torch.load(EXP / "convlstm_best.pth", map_location="cpu", weights_only=True))
    model.eval()
    outputs = []
    with torch.inference_mode():
        for start in range(0, len(x), 4):
            batch = torch.from_numpy(np.array(x[start:start+4], copy=True))
            outputs.append(model(batch).numpy())
    pred_norm = np.concatenate(outputs, axis=0)
    target_norm = np.array(y, copy=True)
    pred_c = pred_norm * std + mean
    target_c = target_norm * std + mean
    input_c = np.array(x[:, -1], copy=True) * std + mean
    return input_c[:, 0], pred_c[:, 0], target_c[:, 0], mean, std


def spatial_and_example_figures(error: dict, inputs: np.ndarray,
                                pred: np.ndarray, target: np.ndarray) -> None:
    residual = pred - target
    grid_rmse = np.sqrt(np.mean(residual**2, axis=0))
    grid_mae = np.mean(np.abs(residual), axis=0)
    extent = (65, 100, 5, 35)
    fig, axes = plt.subplots(1, 2, figsize=(8.1, 3.8), sharex=True, sharey=True)
    panels = [(grid_rmse, "Gridpoint RMSE (°C)", "magma", 0, 5.6),
              (grid_mae, "Gridpoint MAE (°C)", "viridis", 0, float(np.percentile(grid_mae, 99)))]
    for ax, (arr, title, cmap, vmin, vmax) in zip(axes, panels):
        im = ax.imshow(arr, extent=extent, origin="upper", aspect="auto", cmap=cmap,
                       vmin=vmin, vmax=vmax, interpolation="nearest")
        ax.set_title(title, loc="left", fontweight="bold", color=COLORS["navy"])
        ax.set_xlabel("Longitude (°E)")
        ax.set_xticks([65, 70, 80, 90, 100])
        ax.set_yticks([5, 10, 20, 30, 35])
        ax.grid(color="white", alpha=0.28, linewidth=0.45)
        cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.035)
        cb.ax.tick_params(labelsize=7)
    axes[0].set_ylabel("Latitude (°N)")
    fig.suptitle("Spatial distribution of 2025 test errors", x=0.02, ha="left",
                 fontsize=12, fontweight="bold", color=COLORS["navy"])
    fig.text(0.02, 0.01,
             f"Computed from all {len(pred)} aligned test forecasts · grid cells shown without political boundaries",
             fontsize=8, color=COLORS["gray"])
    fig.tight_layout(rect=(0, 0.07, 1, 0.90), w_pad=1.3)
    save(fig, "fig4_spatial_test_errors")

    daily_rmse = np.sqrt(np.mean(residual**2, axis=(1, 2)))
    idx = int(np.argsort(daily_rmse)[len(daily_rmse)//2])
    abs_error = np.abs(pred[idx] - target[idx])
    vmin = float(min(np.min(inputs[idx]), np.min(target[idx]), np.min(pred[idx])))
    vmax = float(max(np.max(inputs[idx]), np.max(target[idx]), np.max(pred[idx])))
    fig, axes = plt.subplots(1, 4, figsize=(10.5, 3.25))
    maps = [(inputs[idx], "Previous-day Tmax"), (target[idx], "Observed target"),
            (pred[idx], "Conv3D prediction")]
    for ax, (arr, title) in zip(axes[:3], maps):
        im = ax.imshow(arr, extent=extent, origin="upper", aspect="auto", cmap="coolwarm",
                       vmin=vmin, vmax=vmax, interpolation="nearest")
        ax.set_title(title, fontsize=8.5, fontweight="bold", color=COLORS["navy"])
        ax.set_xlabel("Lon (°E)")
        ax.set_xticks([65, 80, 100])
        ax.set_yticks([5, 20, 35])
        ax.tick_params(labelsize=7)
    axes[0].set_ylabel("Lat (°N)")
    im2 = axes[3].imshow(abs_error, extent=extent, origin="upper", aspect="auto", cmap="magma",
                         vmin=0, vmax=max(1, float(np.percentile(abs_error, 99))), interpolation="nearest")
    axes[3].set_title("Absolute error", fontsize=8.5, fontweight="bold", color=COLORS["navy"])
    axes[3].set_xlabel("Lon (°E)")
    axes[3].set_xticks([65, 80, 100])
    axes[3].set_yticks([5, 20, 35])
    axes[3].tick_params(labelsize=7)
    fig.subplots_adjust(left=0.065, right=0.96, bottom=0.24, top=0.80, wspace=0.30)
    fig.colorbar(im, ax=axes[:3], location="bottom", fraction=0.075, pad=0.30,
                 orientation="horizontal", label="Temperature (°C)")
    fig.colorbar(im2, ax=axes[3], fraction=0.046, pad=0.035, label="Error (°C)")
    target_date = np.datetime64("2025-01-08") + np.timedelta64(idx, "D")
    fig.suptitle(f"Representative median-error test forecast · target {target_date}", x=0.02,
                 ha="left", fontsize=11, fontweight="bold", color=COLORS["navy"])
    save(fig, "fig5_representative_test_map")
    return grid_rmse, grid_mae


def training_history_figure() -> None:
    model_specs = [("convlstm", "Conv3D", COLORS["blue"]),
                   ("cnn_lstm", "CNN-LSTM", COLORS["teal"]),
                   ("transformer", "Transformer", COLORS["purple"]),
                   ("lstm", "LSTM", COLORS["orange"])]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for key, label, color in model_specs:
        history_dir = ROOT / "experiments" / "reviewer_lstm_repaired_20261014" if key == "lstm" else EXP
        data = json.loads((history_dir / f"{key}_history.json").read_text(encoding="utf-8"))
        hist = data["history"]
        ax.plot([r["epoch"] for r in hist], [r["validation_loss"] for r in hist],
                linewidth=1.6, color=color, label=label)
        best = int(data["best_epoch"])
        best_row = hist[best-1]
        ax.scatter([best], [best_row["validation_loss"]], s=22, color=color, zorder=3,
                   edgecolor="white", linewidth=0.5)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Validation loss (normalized weighted MSE)")
    ax.set_title("Validation loss during training", loc="left", fontweight="bold", color=COLORS["navy"])
    ax.grid(alpha=0.8)
    ax.legend(frameon=False, ncol=2)
    fig.text(0.02, 0.01, "Markers indicate each model's validation-selected checkpoint epoch",
             fontsize=8, color=COLORS["gray"])
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "fig6_training_validation_curves")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    error = json.loads((EXP / "error_analysis.json").read_text(encoding="utf-8"))
    comparison_figure()
    ablation_figure()
    seasonal_figure(error)
    inputs, pred, target, mean, std = get_test_outputs()
    grid_rmse, grid_mae = spatial_and_example_figures(error, inputs, pred, target)
    training_history_figure()
    print(f"Figures written to: {OUT}")
    print(f"Prediction data: checkpoint={EXP / 'convlstm_best.pth'}; test samples={len(target)}")
    print(f"Denormalization: mean={mean:.9f} C; std={std:.9f} C")
    print(f"Recomputed gridpoint RMSE range={grid_rmse.min():.6f}..{grid_rmse.max():.6f} C; mean={grid_rmse.mean():.6f} C")
    print(f"Recomputed gridpoint MAE range={grid_mae.min():.6f}..{grid_mae.max():.6f} C")


if __name__ == "__main__":
    main()
