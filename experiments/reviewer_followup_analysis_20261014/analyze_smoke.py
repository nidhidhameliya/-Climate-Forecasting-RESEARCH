from __future__ import annotations
import json
import sys
from pathlib import Path
import numpy as np
import torch
import xarray as xr
import yaml
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from torch.utils.data import DataLoader, TensorDataset

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SEQ = 7
sys.path.insert(0, str(ROOT))
from models.convlstm import ConvLSTMModel

def metrics(pred, target):
    p, y = np.asarray(pred).reshape(-1), np.asarray(target).reshape(-1)
    return {
        'rmse_C': float(np.sqrt(mean_squared_error(y, p))),
        'mae_C': float(mean_absolute_error(y, p)),
        'r2': float(r2_score(y, p)),
        'pearson_r': float(np.corrcoef(p, y)[0, 1]),
        'n_grid_values': int(y.size),
    }

stats = json.loads((ROOT/'data/processed/mean_std.json').read_text())
mean, std = float(stats['mean']), float(stats['std'])
if not np.isfinite(mean) or not np.isfinite(std) or std <= 0:
    raise ValueError(f'Invalid training normalization stats: {mean=}, {std=}')
Xn = np.load(ROOT/'data/processed/tensors/test_X.npy', mmap_mode='r')
yn = np.load(ROOT/'data/processed/tensors/test_y.npy', mmap_mode='r')
if Xn.shape[0] != yn.shape[0] or Xn.shape[1] != SEQ:
    raise ValueError(f'Unexpected aligned tensor shapes: X={Xn.shape}, y={yn.shape}')
with xr.open_dataset(ROOT/'data/interim/test_daily.nc') as ds:
    dates = ds.time.values.astype('datetime64[D]')
    lat = ds.latitude.values.astype(float)
    lon = ds.longitude.values.astype(float)
if len(dates) - SEQ != len(yn):
    raise ValueError('Unexpected daily target-date alignment')
target_dates = dates[SEQ:]
if str(target_dates[0]) != '2025-01-08' or str(target_dates[-1]) != '2025-12-31':
    raise ValueError(f'Unexpected target dates {target_dates[0]}..{target_dates[-1]}')

config = yaml.safe_load((ROOT/'config.yaml').read_text())
model = ConvLSTMModel(config)
checkpoint = ROOT/'experiments/reviewer_baselines_verified_20261013_smoke_retry2/convlstm_best.pth'
model.load_state_dict(torch.load(checkpoint, map_location='cpu', weights_only=True))
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model.to(device).eval()
loader = DataLoader(TensorDataset(torch.from_numpy(np.asarray(Xn).copy()).float()), batch_size=16, shuffle=False)
preds = []
with torch.no_grad():
    for (xb,) in loader:
        out = model(xb.to(device)).cpu().numpy()[:, 0]
        preds.append(out)
pred_c = np.concatenate(preds) * std + mean
target_c = np.asarray(yn)[:, 0] * std + mean
if not np.isfinite(pred_c).all() or not np.isfinite(target_c).all():
    raise ValueError('Non-finite prediction or target')

# The 7-day persistence baseline is the final input day. Compare on identical 358 target dates.
persist_c = np.asarray(Xn)[:, -1, 0] * std + mean
smoke_metrics = metrics(pred_c, target_c)
persist_metrics = metrics(persist_c, target_c)
# Identical dates shared with the 14-day window experiment (days 15..365).
common_offset = 14 - SEQ
common_smoke = metrics(pred_c[common_offset:], target_c[common_offset:])
common_persist = metrics(persist_c[common_offset:], target_c[common_offset:])

# Additional persistence window counts and naturally aligned date spans, evaluated in normalized daily arrays.
daily = np.load(ROOT/'data/processed/test.npy', mmap_mode='r')
persistence_windows = {}
for window in (3, 7, 14):
    # target index t is paired with day t-1 as persistence prediction; t runs window..n_days-1.
    target_index = np.arange(window, len(daily))
    p = np.asarray(daily[target_index - 1]) * std + mean
    y = np.asarray(daily[target_index]) * std + mean
    persistence_windows[str(window)] = {
        'input_days': window,
        'sequences': int(len(target_index)),
        'target_start': str(dates[target_index[0]]),
        'target_end': str(dates[target_index[-1]]),
        'metrics': metrics(p, y),
    }

# Meteorological seasons for 7-day smoke model.
season_by_month = {12:'DJF', 1:'DJF', 2:'DJF', 3:'MAM', 4:'MAM', 5:'MAM', 6:'JJA', 7:'JJA', 8:'JJA', 9:'SON', 10:'SON', 11:'SON'}
seasons = {}
months = target_dates.astype('datetime64[M]').astype(int) % 12 + 1
for season in ('DJF','MAM','JJA','SON'):
    idx = np.array([season_by_month[int(m)] == season for m in months])
    seasons[season] = {'target_days': int(idx.sum()), 'start': str(target_dates[idx][0]), 'end': str(target_dates[idx][-1]), 'convlstm_smoke': metrics(pred_c[idx], target_c[idx]), 'persistence': metrics(persist_c[idx], target_c[idx])}

# Gridpoint RMSE and zonal summaries, in Celsius.
err = pred_c - target_c
rmse_map = np.sqrt(np.mean(err**2, axis=0))
worst = np.unravel_index(np.argmax(rmse_map), rmse_map.shape)
lat_rmse = np.sqrt(np.mean(err**2, axis=(0,2)))
lon_rmse = np.sqrt(np.mean(err**2, axis=(0,1)))
spatial = {
 'gridpoint_rmse_min_C': float(rmse_map.min()), 'gridpoint_rmse_mean_C': float(rmse_map.mean()), 'gridpoint_rmse_max_C': float(rmse_map.max()),
 'worst_gridpoint': {'latitude': float(lat[worst[0]]), 'longitude': float(lon[worst[1]]), 'rmse_C': float(rmse_map[worst])},
 'latitude_band_rmse_min_mean_C': float(lat_rmse.min()), 'latitude_band_rmse_max_mean_C': float(lat_rmse.max()),
 'longitude_band_rmse_min_mean_C': float(lon_rmse.min()), 'longitude_band_rmse_max_mean_C': float(lon_rmse.max()),
}
report = {
 'status': 'smoke-checkpoint diagnostic only; one epoch; not a final model result',
 'checkpoint': str(checkpoint.relative_to(ROOT)), 'device': str(device), 'dates': {'first_target': str(target_dates[0]), 'last_target': str(target_dates[-1]), 'samples': int(len(target_dates))},
 'normalization': {'mean_C': mean, 'std_C': std, 'inverse': 'normalized * std + mean_C'},
 'convlstm_smoke_aligned_test': smoke_metrics, 'persistence_same_358_targets': persist_metrics,
 'common_351_targets_for_7_vs_14_day_window': {'dates': [str(dates[14]),str(dates[-1])], 'convlstm_smoke': common_smoke, 'persistence': common_persist},
 'persistence_by_window': persistence_windows, 'seasonal_errors': seasons, 'spatial_errors': spatial,
 'protocol_note': 'All global metrics flatten identical aligned grid cells; 7-day model target dates align with test_X/test_y. Persistence uses the last input day. 3/7/14 persistence rows have different natural target ranges; common 351-date comparison is separately provided.'
}
(OUT/'followup_analysis.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
print(json.dumps(report, indent=2))
