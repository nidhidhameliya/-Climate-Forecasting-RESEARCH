"""Train and compare the requested next-day forecasting baselines.

All learned models use the same saved train/validation/test tensors, sequence
length, forecast horizon, optimizer, loss, and evaluation protocol. Persistence
uses the final input day as the prediction and requires no training.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import os
import random
import time
from pathlib import Path

import numpy as np
import torch
import yaml
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from torch.utils.data import DataLoader, TensorDataset

from models.model_utils import get_model
from training.losses import get_loss


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / "experiments" / "reviewer_baselines"
MODEL_NAMES = ("persistence", "lstm", "cnn_lstm", "convlstm", "transformer")


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def load_config() -> dict:
    with (ROOT / "config.yaml").open() as handle:
        return yaml.safe_load(handle)


def load_data() -> dict[str, np.ndarray]:
    base = ROOT / "data" / "processed" / "tensors"
    return {
        f"{split}_{kind}": np.load(base / f"{split}_{kind}.npy")
        for split in ("train", "val", "test")
        for kind in ("X", "y")
    }


def calculate_metrics(prediction: np.ndarray, target: np.ndarray) -> dict[str, float]:
    if prediction.shape != target.shape:
        raise ValueError(f"Metric arrays are not aligned: prediction={prediction.shape}, target={target.shape}")
    if not np.isfinite(prediction).all() or not np.isfinite(target).all():
        raise FloatingPointError("Metrics require finite predictions and targets")
    prediction_flat = prediction.reshape(-1)
    target_flat = target.reshape(-1)
    correlation = float(np.corrcoef(prediction_flat, target_flat)[0, 1])
    return {
        "rmse": float(np.sqrt(mean_squared_error(target_flat, prediction_flat))),
        "mae": float(mean_absolute_error(target_flat, prediction_flat)),
        "r2": float(r2_score(target_flat, prediction_flat)),
        "correlation": correlation if np.isfinite(correlation) else None,
    }


def denormalize(array: np.ndarray, mean: float, std: float) -> np.ndarray:
    return array * std + mean


def predict_model(model, loader, device, mean: float, std: float) -> tuple[np.ndarray, np.ndarray]:
    predictions, targets = [], []
    model.eval()
    with torch.no_grad():
        for inputs, batch_targets in loader:
            inputs = inputs.to(device)
            batch_targets = batch_targets.to(device)
            output_tensor = model(inputs)
            if output_tensor.shape != batch_targets.shape:
                raise ValueError(f"Prediction/target shape mismatch: {output_tensor.shape} vs {batch_targets.shape}")
            if output_tensor.device != device or batch_targets.device != device:
                raise RuntimeError("Model, inputs, and targets are not on the selected device")
            output = output_tensor.cpu().numpy()[:, 0]
            predictions.append(output)
            targets.append(batch_targets.cpu().numpy()[:, 0])
    return denormalize(np.concatenate(predictions), mean, std), denormalize(np.concatenate(targets), mean, std)


def run_persistence(data: dict[str, np.ndarray], mean: float, std: float) -> dict:
    prediction = denormalize(data["test_X"][:, -1, 0], mean, std)
    target = denormalize(data["test_y"][:, 0], mean, std)
    return {
        "model": "Persistence",
        "class": "last-input-day",
        "trainable_parameters": 0,
        "epochs": 0,
        "validation": calculate_metrics(
            denormalize(data["val_X"][:, -1, 0], mean, std),
            denormalize(data["val_y"][:, 0], mean, std),
        ),
        "test": calculate_metrics(prediction, target),
    }


def run_learned_model(name: str, config: dict, data: dict[str, np.ndarray], mean: float, std: float, device, epochs: int, batch_size: int, output_dir: Path) -> dict:
    model_config = {**config, "model": {**config["model"], "name": name}}
    model = get_model(model_config).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config["training"]["learning_rate"])
    loss_fn = get_loss(config["training"])
    train_loader = DataLoader(
        TensorDataset(torch.from_numpy(data["train_X"]).float(), torch.from_numpy(data["train_y"]).float()),
        batch_size=batch_size,
        shuffle=True,
    )
    val_loader = DataLoader(
        TensorDataset(torch.from_numpy(data["val_X"]).float(), torch.from_numpy(data["val_y"]).float()),
        batch_size=batch_size,
        shuffle=False,
    )
    test_loader = DataLoader(
        TensorDataset(torch.from_numpy(data["test_X"]).float(), torch.from_numpy(data["test_y"]).float()),
        batch_size=batch_size,
        shuffle=False,
    )
    history = []
    best_loss = float("inf")
    best_epoch = 0
    best_state = None
    checkpoint = output_dir / f"{name}_best.pth"
    history_path = output_dir / f"{name}_history.json"

    def save_history(status: str) -> None:
        payload = {
            "model": name,
            "status": status,
            "requested_epochs": epochs,
            "completed_epochs": len(history),
            "best_epoch": best_epoch,
            "best_validation_loss": best_loss if np.isfinite(best_loss) else None,
            "batch_size": batch_size,
            "optimizer": "Adam",
            "learning_rate": config["training"]["learning_rate"],
            "loss": "ExtremeWeightedMSE",
            "history": history,
        }
        temp = history_path.with_suffix(".json.tmp")
        temp.write_text(json.dumps(payload, indent=2, allow_nan=False), encoding="utf-8")
        os.replace(temp, history_path)

    start = time.perf_counter()
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            output = model(inputs.to(device))
            targets_device = targets.to(device)
            if output.device != device or targets_device.device != device:
                raise RuntimeError("Model, inputs, and targets are not on the selected device")
            loss = loss_fn(output, targets_device)
            if not torch.isfinite(loss):
                raise FloatingPointError(f"{name} training loss is non-finite at epoch {epoch + 1}")
            loss.backward()
            optimizer.step()
            running_loss += float(loss.item())
        model.eval()
        validation_loss = 0.0
        with torch.no_grad():
            for inputs, targets in val_loader:
                val_output = model(inputs.to(device))
                val_targets = targets.to(device)
                if val_output.device != device or val_targets.device != device:
                    raise RuntimeError("Model, inputs, and targets are not on the selected device")
                loss = loss_fn(val_output, val_targets)
                if not torch.isfinite(loss):
                    raise FloatingPointError(f"{name} validation loss is non-finite at epoch {epoch + 1}")
                validation_loss += float(loss.item())
        validation_loss /= len(val_loader)
        epoch_loss = running_loss / len(train_loader)
        history.append({"epoch": epoch + 1, "train_loss": epoch_loss, "validation_loss": validation_loss})
        print(f"{name} epoch {epoch + 1}/{epochs}: train_loss={epoch_loss:.6f}, val_loss={validation_loss:.6f}", flush=True)
        if validation_loss < best_loss:
            best_loss = validation_loss
            best_epoch = epoch + 1
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
            torch.save(best_state, checkpoint)
        save_history("running")

    if best_state is None:
        raise RuntimeError(f"{name} training did not produce a best validation checkpoint")
    model.load_state_dict(best_state)
    model.to(device)

    validation_prediction, validation_target = predict_model(model, val_loader, device, mean, std)
    test_prediction, test_target = predict_model(model, test_loader, device, mean, std)
    training_seconds = round(time.perf_counter() - start, 3)
    save_history("complete")
    return {
        "model": name,
        "class": model.__class__.__name__,
        "trainable_parameters": sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad),
        "epochs": len(history),
        "epochs_requested": epochs,
        "epochs_completed": len(history),
        "batch_size": batch_size,
        "optimizer": "Adam",
        "learning_rate": config["training"]["learning_rate"],
        "loss": "ExtremeWeightedMSE",
        "training_seconds": training_seconds,
        "best_epoch": best_epoch,
        "best_validation_loss": best_loss,
        "history": history,
        "validation": calculate_metrics(validation_prediction, validation_target),
        "test": calculate_metrics(test_prediction, test_target),
        "checkpoint": str(checkpoint.relative_to(ROOT)) if checkpoint.is_relative_to(ROOT) else str(checkpoint),
        "history_file": str(history_path.relative_to(ROOT)) if history_path.is_relative_to(ROOT) else str(history_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", choices=("cpu", "cuda"), default=None)
    parser.add_argument("--models", default=",".join(MODEL_NAMES))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    set_seed(args.seed)
    config = load_config()
    data = load_data()
    stats = json.loads((ROOT / "data" / "processed" / "mean_std.json").read_text())
    mean, std = float(stats["mean"]), float(stats["std"])
    if stats.get("unit") != "degrees_Celsius" or not np.isfinite(mean) or not np.isfinite(std) or std <= 0:
        raise ValueError("Expected finite training-only Celsius normalization stats with std > 0")
    threshold_path = ROOT / "data" / "processed" / "extreme_thresholds.json"
    threshold_info = json.loads(threshold_path.read_text(encoding="utf-8"))
    if not np.isfinite(float(threshold_info["top_5_percent_celsius"])):
        raise ValueError("Training-only 95th percentile threshold must be finite")
    device = torch.device(args.device or ("cuda" if torch.cuda.is_available() else "cpu"))
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was explicitly requested but is unavailable")
    if device.type == "cuda" and device.index is None:
        device = torch.device("cuda", torch.cuda.current_device())
    print(f"Selected device: {device}", flush=True)
    if device.type == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(device)}; PyTorch {torch.__version__}; CUDA runtime {torch.version.cuda}", flush=True)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / "comparison_results.json"
    if result_path.exists():
        raise FileExistsError(f"Refusing to merge or overwrite existing results: {result_path}")

    results = []
    requested = [name.strip().lower() for name in args.models.split(",") if name.strip()]
    if "persistence" in requested:
        results.append(run_persistence(data, mean, std))
        (output_dir / "completed_results.json").write_text(
            json.dumps({"completed_results": results}, indent=2, allow_nan=False), encoding="utf-8"
        )
    for name in requested:
        if name == "persistence":
            continue
        if name not in MODEL_NAMES:
            raise ValueError(f"Unknown model '{name}'. Choose from {', '.join(MODEL_NAMES)}.")
        model_result = run_learned_model(name, config, data, mean, std, device, args.epochs, args.batch_size, output_dir)
        results.append(model_result)
        completed_path = output_dir / "completed_results.json"
        completed_path.write_text(json.dumps({"completed_results": results}, indent=2, allow_nan=False), encoding="utf-8")

    report = {
        "protocol": {
            "sequence_length": config["sequence_length"],
            "forecast_horizon_days": 1,
            "train_samples": int(data["train_X"].shape[0]),
            "validation_samples": int(data["val_X"].shape[0]),
            "test_samples": int(data["test_X"].shape[0]),
            "spatial_shape": list(data["test_y"].shape[-2:]),
            "device": str(device),
            "seed": args.seed,
            "metric_space": "same denormalized stored temperature scale for every model",
            "normalization_unit": "degrees_Celsius",
            "normalization_mean_celsius": mean,
            "normalization_std_celsius": std,
            "loss_threshold_celsius": float(threshold_info["top_5_percent_celsius"]),
            "loss_threshold_normalized": (float(threshold_info["top_5_percent_celsius"]) - mean) / std,
            "loss_threshold_metadata": threshold_info,
            "pytorch_version": torch.__version__,
            "cuda_runtime": torch.version.cuda,
            "run_timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "epochs_requested": args.epochs,
            "output_directory": str(output_dir),
        },
        "results": results,
    }
    result_path.write_text(json.dumps(report, indent=2))
    rows = []
    for result in results:
        row = {
            "model": result["model"],
            "trainable_parameters": result["trainable_parameters"],
            "epochs_completed": result.get("epochs_completed", 0),
            "best_epoch": result.get("best_epoch"),
            "best_validation_loss": result.get("best_validation_loss"),
            "training_seconds": result.get("training_seconds", 0.0),
        }
        for split in ("validation", "test"):
            for key in ("rmse", "mae", "r2", "correlation"):
                row[f"{split}_{key}"] = result[split][key]
        rows.append(row)
    import csv
    with (output_dir / "comparison_results.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
