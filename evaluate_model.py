import numpy as np
import torch
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from models.convlstm import ConvLSTMModel
from training.metrics import rmse
import yaml
import xarray as xr
from sklearn.metrics import r2_score


class ClimateModelEvaluator:
    def __init__(self, model_path="experiments/latest/model.pth", output_dir="outputs/evaluation_corrected", visualization_dir="outputs/visualizations_corrected"):
        """Initialize evaluator with trained model"""
        self.model_path = model_path
        self.output_dir = output_dir
        self.visualization_dir = visualization_dir
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load config
        with open("config.yaml") as f:
            self.config = yaml.safe_load(f)
        
        # Load normalization stats
        self.load_normalization_stats()
        
        # Load model
        self.model = self.load_model()
        
    def load_normalization_stats(self):
        """Load finite stats and record the canonical inverse mean in Celsius."""
        with open("data/processed/mean_std.json", encoding="utf-8") as f:
            stats = json.load(f)
        self.mean = float(stats["mean"])
        self.std = float(stats["std"])
        unit = stats.get("unit", "kelvin")
        if not np.isfinite(self.mean) or not np.isfinite(self.std) or self.std <= 0:
            raise ValueError(f"Invalid normalization stats: mean={self.mean}, std={self.std}")
        if unit in ("degrees_Celsius", "C", "celsius"):
            self.mean_celsius = self.mean
        elif unit in ("K", "kelvin"):
            self.mean_celsius = self.mean - 273.15
        else:
            raise ValueError(f"Unsupported normalization unit: {unit!r}")
        print(f"Normalization stats: mean={self.mean_celsius:.6f} C, std={self.std:.6f} C")

    def load_model(self):
        """Load trained model weights"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        model = ConvLSTMModel(self.config)
        model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        model.to(self.device)
        model.eval()
        print(f"✓ Model loaded from {self.model_path}")
        return model
    
    def denormalize(self, normalized_data):
        """Inverse z-score to Celsius, matching the current stats metadata."""
        return normalized_data * self.std + self.mean_celsius

    def denormalize_celsius(self, normalized_data):
        """Compatibility alias for inverse normalization into Celsius."""
        return self.denormalize(normalized_data)

    def evaluate(self, split="test", save=True, visualize=True):
        """Evaluate a split after verifying every target matches its daily date."""
        if split not in ("train", "val", "test"):
            raise ValueError(f"Unknown split {split!r}")
        X_path = f"data/processed/tensors/{split}_X.npy"
        y_path = f"data/processed/tensors/{split}_y.npy"
        X_norm = np.load(X_path)
        y_norm = np.load(y_path)
        if X_norm.ndim != 5 or y_norm.ndim != 4 or X_norm.shape[0] != y_norm.shape[0]:
            raise ValueError(f"Unaligned input/target shapes: X={X_norm.shape}, y={y_norm.shape}")
        seq_len = int(self.config["sequence_length"])
        daily_norm = np.load(f"data/processed/{split}.npy", mmap_mode="r")
        if len(X_norm) != len(daily_norm) - seq_len:
            raise ValueError(f"{split}: sequence count disagrees with daily data and sequence length")
        for start in range(0, len(y_norm), 64):
            end = min(start + 64, len(y_norm))
            expected = daily_norm[start + seq_len:end + seq_len]
            if not np.allclose(y_norm[start:end, 0], expected, rtol=0.0, atol=1e-6):
                raise ValueError(f"{split}: target tensor misaligned at sample {start}")
        with xr.open_dataset(f"data/interim/{split}_daily.nc") as daily_ds:
            target_dates = daily_ds.time.values[seq_len:]
            if len(target_dates) != len(y_norm):
                raise ValueError(f"{split}: daily target timestamps do not match target tensor")

        X_tensor = torch.from_numpy(X_norm).float()
        y_tensor = torch.from_numpy(y_norm).float()
        batch_size = 8
        all_preds_norm, all_targets_norm = [], []
        self.model.eval()
        with torch.no_grad():
            for start in range(0, len(X_tensor), batch_size):
                xb = X_tensor[start:start + batch_size].to(self.device)
                yb = y_tensor[start:start + batch_size].to(self.device)
                pred = self.model(xb)
                if pred.shape != yb.shape:
                    raise ValueError(f"Prediction shape {tuple(pred.shape)} != target shape {tuple(yb.shape)}")
                if not torch.isfinite(pred).all() or not torch.isfinite(yb).all():
                    raise ValueError(f"Non-finite prediction/target in {split} batch {start}")
                all_preds_norm.append(pred.cpu().numpy())
                all_targets_norm.append(yb.cpu().numpy())

        preds_norm = np.concatenate(all_preds_norm, axis=0)
        targets_norm = np.concatenate(all_targets_norm, axis=0)
        preds_C = self.denormalize_celsius(preds_norm)
        targets_C = self.denormalize_celsius(targets_norm)
        preds_K, targets_K = preds_C + 273.15, targets_C + 273.15
        pred_flat, target_flat = preds_C.reshape(-1), targets_C.reshape(-1)
        pred_norm_flat, target_norm_flat = preds_norm.reshape(-1), targets_norm.reshape(-1)
        rmse_C = float(np.sqrt(np.mean((pred_flat - target_flat) ** 2)))
        mae_C = float(np.mean(np.abs(pred_flat - target_flat)))
        correlation = float(np.corrcoef(pred_flat, target_flat)[0, 1])
        spatial_rmse = np.sqrt(np.mean((preds_C - targets_C) ** 2, axis=0))
        spatial_mae = np.mean(np.abs(preds_C - targets_C), axis=0)
        temporal_rmse = np.sqrt(np.mean((preds_C - targets_C) ** 2, axis=(2, 3)))
        _, _, H, W = preds_C.shape
        results = {
            "split": split,
            "num_samples": int(len(X_norm)),
            "spatial_shape": [int(H), int(W)],
            "alignment": {
                "verified_against_daily_targets": True,
                "first_target_date": str(target_dates[0]),
                "last_target_date": str(target_dates[-1]),
                "samples": int(len(target_dates)),
            },
            "metrics": {
                "rmse_normalized": float(np.sqrt(np.mean((pred_norm_flat - target_norm_flat) ** 2))),
                "mae_normalized": float(np.mean(np.abs(pred_norm_flat - target_norm_flat))),
                "rmse_kelvin": rmse_C,
                "mae_kelvin": mae_C,
                "rmse_celsius": rmse_C,
                "mae_celsius": mae_C,
                "r2": float(r2_score(target_flat, pred_flat)),
                "pearson_r": correlation,
            },
            "spatial_metrics": {
                "spatial_rmse_min_celsius": float(spatial_rmse.min()),
                "spatial_rmse_mean_celsius": float(spatial_rmse.mean()),
                "spatial_rmse_max_celsius": float(spatial_rmse.max()),
                "spatial_rmse_std_celsius": float(spatial_rmse.std()),
            },
            "value_ranges_celsius": {
                "pred_min": float(pred_flat.min()), "pred_max": float(pred_flat.max()),
                "target_min": float(target_flat.min()), "target_max": float(target_flat.max()),
                "pred_mean": float(pred_flat.mean()), "target_mean": float(target_flat.mean()),
            },
            "temporal_rmse_celsius": temporal_rmse[:, 0].tolist(),
        }
        self.print_results(results)
        if save:
            self.save_results(results)
        if visualize:
            self.create_visualizations(preds_norm, targets_norm, preds_C, targets_C, spatial_rmse, split)
        return results, preds_C, targets_C

    def print_results(self, results):
        metrics = results["metrics"]
        print(f"\nEvaluation {results['split']}: {results['num_samples']} aligned samples")
        print(f"Target dates: {results['alignment']['first_target_date']} to {results['alignment']['last_target_date']}")
        print(f"RMSE={metrics['rmse_celsius']:.6f} C; MAE={metrics['mae_celsius']:.6f} C; R2={metrics['r2']:.6f}; Pearson r={metrics['pearson_r']:.6f}")

    def save_results(self, results):
        """Save results to JSON"""
        os.makedirs(self.output_dir, exist_ok=True)

        output_path = os.path.join(self.output_dir, f"{results['split']}_results.json")
        if os.path.exists(output_path):
            raise FileExistsError(f"Refusing to overwrite existing evaluation result: {output_path}")
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"✓ Results saved to {output_path}")
    
    def create_visualizations(self, preds_norm, targets_norm, preds_C, targets_C, spatial_rmse, split):
        """Create evaluation visualizations"""
        os.makedirs(self.visualization_dir, exist_ok=True)
        
        # 1. Error distribution
        errors_C = preds_C - targets_C
        errors_C_flat = errors_C.flatten()
        
        # Handle NaN values
        valid_errors = errors_C_flat[~np.isnan(errors_C_flat)]
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f"Model Evaluation - {split.upper()} Set", fontsize=16, fontweight='bold')
        
        if len(valid_errors) > 0:
            # Error histogram
            axes[0, 0].hist(valid_errors, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
            axes[0, 0].set_xlabel('Prediction Error (°C)')
            axes[0, 0].set_ylabel('Frequency')
            axes[0, 0].set_title('Error Distribution')
            mean_err = np.mean(valid_errors)
            axes[0, 0].axvline(mean_err, color='red', linestyle='--', label=f'Mean: {mean_err:.3f}°C')
            axes[0, 0].legend()
        
        # Prediction vs Actual scatter (use normalized data which is valid)
        preds_flat = preds_norm.flatten()
        targets_flat = targets_norm.flatten()
        valid_idx = ~(np.isnan(preds_flat) | np.isnan(targets_flat))
        
        if np.sum(valid_idx) > 0:
            sample_idx = np.random.choice(np.where(valid_idx)[0], min(1000, np.sum(valid_idx)), replace=False)
            axes[0, 1].scatter(targets_flat[sample_idx], preds_flat[sample_idx], alpha=0.5, s=10)
            min_val = min(targets_flat[valid_idx].min(), preds_flat[valid_idx].min())
            max_val = max(targets_flat[valid_idx].max(), preds_flat[valid_idx].max())
            axes[0, 1].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect')
            axes[0, 1].set_xlabel('Actual (Normalized)')
            axes[0, 1].set_ylabel('Predicted (Normalized)')
            axes[0, 1].set_title('Prediction Accuracy')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
        
        # Spatial RMSE heatmap
        spatial_rmse_flat = spatial_rmse[0] if spatial_rmse.ndim == 3 else spatial_rmse
        valid_spatial = spatial_rmse_flat[~np.isnan(spatial_rmse_flat)]
        
        if len(valid_spatial) > 0:
            im = axes[1, 0].imshow(np.nan_to_num(spatial_rmse_flat), cmap='RdYlGn_r', aspect='auto')
            axes[1, 0].set_title('Spatial RMSE Distribution')
            axes[1, 0].set_xlabel('Longitude')
            axes[1, 0].set_ylabel('Latitude')
            plt.colorbar(im, ax=axes[1, 0], label='RMSE')
        
        # Error by location
        if spatial_rmse_flat.ndim == 2:
            mean_spatial = np.nanmean(spatial_rmse_flat, axis=0)
        else:
            mean_spatial = spatial_rmse_flat
        
        valid_spatial_idx = ~np.isnan(mean_spatial)
        if np.sum(valid_spatial_idx) > 0:
            axes[1, 1].plot(mean_spatial[valid_spatial_idx], linewidth=2, color='steelblue')
            axes[1, 1].set_xlabel('Longitude Index')
            axes[1, 1].set_ylabel('Mean RMSE')
            axes[1, 1].set_title('RMSE by Longitude')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        fig_path = f"outputs/visualizations/{split}_evaluation.png"
        plt.savefig(fig_path, dpi=150, bbox_inches='tight')
        print(f"✓ Visualization saved to {fig_path}")
        plt.close()
        
        # 2. Sample predictions map
        sample_idx = 0
        pred_map = preds_C[sample_idx, 0]
        target_map = targets_C[sample_idx, 0]
        error_map = pred_map - target_map
        
        fig, axes = plt.subplots(1, 3, figsize=(16, 4))
        fig.suptitle(f"Sample Prediction - {split.upper()} (Sample {sample_idx})", fontsize=14, fontweight='bold')
        
        # Handle NaN values in maps
        vmin, vmax = np.nanpercentile(target_map, [2, 98])
        
        im1 = axes[0].imshow(np.nan_to_num(target_map), cmap='coolwarm', aspect='auto', vmin=vmin, vmax=vmax)
        axes[0].set_title('Actual Temperature')
        axes[0].set_xlabel('Longitude')
        axes[0].set_ylabel('Latitude')
        plt.colorbar(im1, ax=axes[0], label='Value')
        
        im2 = axes[1].imshow(np.nan_to_num(pred_map), cmap='coolwarm', aspect='auto', vmin=vmin, vmax=vmax)
        axes[1].set_title('Predicted Temperature')
        axes[1].set_xlabel('Longitude')
        axes[1].set_ylabel('Latitude')
        plt.colorbar(im2, ax=axes[1], label='Value')
        
        error_max = np.nanmax(np.abs(error_map))
        im3 = axes[2].imshow(np.nan_to_num(error_map), cmap='RdBu_r', aspect='auto', vmin=-error_max, vmax=error_max)
        axes[2].set_title('Prediction Error')
        axes[2].set_xlabel('Longitude')
        axes[2].set_ylabel('Latitude')
        plt.colorbar(im3, ax=axes[2], label='Error')
        
        plt.tight_layout()
        map_path = os.path.join(self.visualization_dir, f"{split}_prediction_map.png")
        plt.savefig(map_path, dpi=150, bbox_inches='tight')
        print(f"✓ Map visualization saved to {map_path}")
        plt.close()


if __name__ == "__main__":
    evaluator = ClimateModelEvaluator()
    
    # Evaluate on all splits
    print("\n" + "="*60)
    print("EVALUATING ALL SPLITS")
    print("="*60)
    
    for split in ["train", "val", "test"]:
        print(f"\n🔍 Evaluating {split.upper()} split...")
        results, preds, targets = evaluator.evaluate(split=split)
    
    print("\n" + "="*60)
    print("✅ EVALUATION COMPLETE - All splits evaluated!")
    print("="*60)
